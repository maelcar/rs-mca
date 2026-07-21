//! Exhaustive first-three-moment classification for four- and five-subsets
//! of the active D128 Chebyshev domain.

use std::collections::{BTreeMap, HashMap};
use std::env;
use std::fs::{create_dir_all, remove_dir, remove_file, File};
use std::io::{Read, Write};
use std::path::{Path, PathBuf};
use std::time::Instant;

const P: u64 = 2_147_483_647;
const ROOTS: usize = 128;
const E4_SUBSETS: u64 = 10_668_000;
const E5_SUBSETS: u64 = 264_566_400;
const BUCKET_BITS: usize = 5;
const BUCKETS: usize = 1 << BUCKET_BITS;
const BUFFER_WORDS: usize = 1 << 16;
const PREFIX_BITS: usize = 24;

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Key(u32, u32, u32);

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Mask(u64, u64);

impl Mask {
    fn from_indices(indices: &[usize]) -> Self {
        let mut answer = Self(0, 0);
        for &index in indices {
            if index < 64 {
                answer.0 |= 1u64 << index;
            } else {
                answer.1 |= 1u64 << (index - 64);
            }
        }
        answer
    }

    fn cardinality(self) -> u32 {
        self.0.count_ones() + self.1.count_ones()
    }

    fn disjoint(self, other: Self) -> bool {
        (self.0 & other.0) == 0 && (self.1 & other.1) == 0
    }

    fn intersection(self, other: Self) -> Self {
        Self(self.0 & other.0, self.1 & other.1)
    }

    fn difference(self, other: Self) -> Self {
        Self(self.0 ^ other.0, self.1 ^ other.1)
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Fp2(u64, u64);

fn multiply(x: Fp2, y: Fp2) -> Fp2 {
    Fp2(
        (x.0 * y.0 + P - x.1 * y.1 % P) % P,
        (x.0 * y.1 + x.1 * y.0) % P,
    )
}

fn power(mut base: Fp2, mut exponent: u64) -> Fp2 {
    let mut answer = Fp2(1, 0);
    while exponent != 0 {
        if exponent & 1 != 0 {
            answer = multiply(answer, base);
        }
        base = multiply(base, base);
        exponent >>= 1;
    }
    answer
}

fn inverse(mut base: u64) -> u64 {
    let mut exponent = P - 2;
    let mut answer = 1u64;
    while exponent != 0 {
        if exponent & 1 != 0 {
            answer = answer * base % P;
        }
        base = base * base % P;
        exponent >>= 1;
    }
    answer
}

fn cayley(parameter: u64) -> Fp2 {
    let square = parameter * parameter % P;
    let scale = inverse((square + 1) % P);
    Fp2(
        (square + P - 1) % P * scale % P,
        2 * parameter % P * scale % P,
    )
}

fn chebyshev(degree: usize, x: u32) -> u32 {
    let mut value = x as u64;
    let mut current = 1usize;
    while current < degree {
        value = (2 * value * value + P - 1) % P;
        current *= 2;
    }
    value as u32
}

fn add_coordinate(left: u32, right: u32) -> u32 {
    let sum = left as u64 + right as u64;
    if sum >= P { (sum - P) as u32 } else { sum as u32 }
}

fn add(left: Key, right: Key) -> Key {
    Key(
        add_coordinate(left.0, right.0),
        add_coordinate(left.1, right.1),
        add_coordinate(left.2, right.2),
    )
}

fn fingerprint(key: Key) -> u64 {
    let mut value = (key.0 as u64).wrapping_mul(0x517c_c1b7_2722_0a95);
    value ^= (key.1 as u64)
        .wrapping_mul(0x9e37_79b9_7f4a_7c15)
        .rotate_left(19);
    value ^= (key.2 as u64)
        .wrapping_mul(0x94d0_49bb_1331_11eb)
        .rotate_left(43);
    value ^= value >> 30;
    value = value.wrapping_mul(0xbf58_476d_1ce4_e5b9);
    value ^= value >> 27;
    value = value.wrapping_mul(0x94d0_49bb_1331_11eb);
    value ^ (value >> 31)
}

fn domain() -> ([Key; ROOTS], Vec<Mask>) {
    let eta = power(cayley(3), 1u64 << 22);
    assert_eq!(power(eta, 512), Fp2(1, 0));
    assert_ne!(power(eta, 256), Fp2(1, 0));
    let mut roots = [0u32; ROOTS];
    let mut point = eta;
    let step = multiply(eta, eta);
    for root in roots.iter_mut() {
        *root = point.0 as u32;
        point = multiply(point, step);
    }
    roots.sort_unstable();
    roots.windows(2).for_each(|pair| assert_ne!(pair[0], pair[1]));
    roots.iter().for_each(|&root| assert_eq!(chebyshev(128, root), 0));

    let mut moments = [Key(0, 0, 0); ROOTS];
    let mut blocks = BTreeMap::<u32, Vec<usize>>::new();
    for (index, &root) in roots.iter().enumerate() {
        let square = root as u64 * root as u64 % P;
        moments[index] = Key(root, square as u32, (square * root as u64 % P) as u32);
        blocks.entry(chebyshev(4, root)).or_default().push(index);
    }
    assert_eq!(blocks.len(), 32);
    let block_masks = blocks
        .into_values()
        .map(|indices| {
            assert_eq!(indices.len(), 4);
            Mask::from_indices(&indices)
        })
        .collect();
    (moments, block_masks)
}

fn enumerate<F>(size: usize, moments: &[Key; ROOTS], mut callback: F) -> u64
where
    F: FnMut(Key, Mask),
{
    let mut count = 0u64;
    if size == 4 {
        for a in 0..125 {
            for b in a + 1..126 {
                let ab = add(moments[a], moments[b]);
                for c in b + 1..127 {
                    let abc = add(ab, moments[c]);
                    for d in c + 1..128 {
                        callback(add(abc, moments[d]), Mask::from_indices(&[a, b, c, d]));
                        count += 1;
                    }
                }
            }
        }
    } else {
        assert_eq!(size, 5);
        for a in 0..124 {
            for b in a + 1..125 {
                let ab = add(moments[a], moments[b]);
                for c in b + 1..126 {
                    let abc = add(ab, moments[c]);
                    for d in c + 1..127 {
                        let abcd = add(abc, moments[d]);
                        for e in d + 1..128 {
                            callback(
                                add(abcd, moments[e]),
                                Mask::from_indices(&[a, b, c, d, e]),
                            );
                            count += 1;
                        }
                    }
                }
            }
        }
    }
    count
}

fn bucket_path(directory: &Path, bucket: usize) -> PathBuf {
    directory.join(format!("bucket_{bucket:02}.bin"))
}

struct BucketWriter {
    file: File,
    words: Vec<u64>,
}

impl BucketWriter {
    fn new(path: &Path) -> Self {
        Self { file: File::create(path).unwrap(), words: Vec::with_capacity(BUFFER_WORDS) }
    }

    fn push(&mut self, value: u64) {
        self.words.push(value);
        if self.words.len() == BUFFER_WORDS { self.flush(); }
    }

    fn flush(&mut self) {
        if self.words.is_empty() { return; }
        let bytes = unsafe {
            std::slice::from_raw_parts(self.words.as_ptr() as *const u8, self.words.len() * 8)
        };
        self.file.write_all(bytes).unwrap();
        self.words.clear();
    }
}

fn read_words(path: &Path) -> Vec<u64> {
    let mut file = File::open(path).unwrap();
    let bytes = file.metadata().unwrap().len() as usize;
    assert_eq!(bytes % 8, 0);
    let mut words = Vec::<u64>::with_capacity(bytes / 8);
    unsafe {
        words.set_len(bytes / 8);
        let target = std::slice::from_raw_parts_mut(words.as_mut_ptr() as *mut u8, bytes);
        file.read_exact(target).unwrap();
    }
    words
}

#[derive(Debug)]
struct ResultRow {
    size: usize,
    subsets: u64,
    distinct_keys: u64,
    collision_groups: u64,
    colliding_subsets: u64,
    maximum_group: usize,
    classified_groups: u64,
    other_groups: u64,
    disjoint_pairs: u64,
    group_histogram: BTreeMap<usize, u64>,
    common_histogram: BTreeMap<u32, u64>,
    peak_bucket_records: usize,
}

fn classify(size: usize, moments: &[Key; ROOTS], blocks: &[Mask], directory: &Path) -> ResultRow {
    create_dir_all(directory).unwrap();
    let expected_subsets = if size == 4 { E4_SUBSETS } else { E5_SUBSETS };
    let mut writers: Vec<BucketWriter> = (0..BUCKETS)
        .map(|bucket| BucketWriter::new(&bucket_path(directory, bucket)))
        .collect();
    let subsets = enumerate(size, moments, |key, _| {
        let value = fingerprint(key);
        writers[value as usize >> (64 - BUCKET_BITS)].push(value);
    });
    assert_eq!(subsets, expected_subsets);
    for writer in &mut writers { writer.flush(); }
    drop(writers);

    let mut duplicates = Vec::<u64>::new();
    let mut peak_bucket_records = 0usize;
    for bucket in 0..BUCKETS {
        let path = bucket_path(directory, bucket);
        let mut values = read_words(&path);
        peak_bucket_records = peak_bucket_records.max(values.len());
        values.sort_unstable();
        let mut begin = 0usize;
        while begin < values.len() {
            let mut end = begin + 1;
            while end < values.len() && values[end] == values[begin] { end += 1; }
            if end - begin > 1 { duplicates.push(values[begin]); }
            begin = end;
        }
        remove_file(path).unwrap();
    }
    duplicates.sort_unstable();

    let mut active_prefixes = vec![false; 1 << PREFIX_BITS];
    for &value in &duplicates {
        active_prefixes[(value >> (64 - PREFIX_BITS)) as usize] = true;
    }
    let mut recovered = HashMap::<Key, Vec<Mask>>::new();
    let recovered_count = enumerate(size, moments, |key, mask| {
        let value = fingerprint(key);
        if active_prefixes[(value >> (64 - PREFIX_BITS)) as usize]
            && duplicates.binary_search(&value).is_ok()
        {
            recovered.entry(key).or_default().push(mask);
        }
    });
    assert_eq!(recovered_count, expected_subsets);

    let mut collision_groups = 0u64;
    let mut colliding_subsets = 0u64;
    let mut distinct_keys = expected_subsets;
    let mut maximum_group = 1usize;
    let mut classified_groups = 0u64;
    let mut other_groups = 0u64;
    let mut disjoint_pairs = 0u64;
    let mut group_histogram = BTreeMap::new();
    let mut common_histogram = BTreeMap::new();
    let mut sorted_blocks = blocks.to_vec();
    sorted_blocks.sort_unstable();

    for group in recovered.values().filter(|group| group.len() > 1) {
        collision_groups += 1;
        colliding_subsets += group.len() as u64;
        distinct_keys -= (group.len() - 1) as u64;
        maximum_group = maximum_group.max(group.len());
        *group_histogram.entry(group.len()).or_insert(0) += 1;
        let common = group.iter().copied().reduce(Mask::intersection).unwrap();
        *common_histogram.entry(common.cardinality()).or_insert(0) += 1;
        for left in 0..group.len() {
            for right in left + 1..group.len() {
                disjoint_pairs += u64::from(group[left].disjoint(group[right]));
            }
        }

        let classified = if size == 4 {
            let mut actual = group.clone();
            actual.sort_unstable();
            common.cardinality() == 0 && actual == sorted_blocks
        } else {
            let mut residuals: Vec<Mask> = group
                .iter().copied().map(|mask| mask.difference(common)).collect();
            residuals.sort_unstable();
            let mut expected: Vec<Mask> = blocks
                .iter().copied().filter(|block| block.disjoint(common)).collect();
            expected.sort_unstable();
            common.cardinality() == 1 && residuals == expected
        };
        if classified { classified_groups += 1; } else { other_groups += 1; }
    }
    remove_dir(directory).unwrap();
    ResultRow {
        size,
        subsets: expected_subsets,
        distinct_keys,
        collision_groups,
        colliding_subsets,
        maximum_group,
        classified_groups,
        other_groups,
        disjoint_pairs,
        group_histogram,
        common_histogram,
        peak_bucket_records,
    }
}

fn write_map<K: std::fmt::Display>(out: &mut impl Write, map: &BTreeMap<K, u64>) {
    for (position, (key, value)) in map.iter().enumerate() {
        write!(out, "{}\"{}\": {}", if position == 0 { "" } else { ", " }, key, value).unwrap();
    }
}

fn write_row(out: &mut impl Write, name: &str, row: &ResultRow, final_row: bool) {
    writeln!(out, "  \"{name}\": {{").unwrap();
    writeln!(out, "    \"subset_size\": {},", row.size).unwrap();
    writeln!(out, "    \"subsets_checked\": {},", row.subsets).unwrap();
    writeln!(out, "    \"exact_distinct_moment_keys\": {},", row.distinct_keys).unwrap();
    writeln!(out, "    \"exact_collision_groups\": {},", row.collision_groups).unwrap();
    writeln!(out, "    \"exact_colliding_subsets\": {},", row.colliding_subsets).unwrap();
    writeln!(out, "    \"maximum_exact_group_size\": {},", row.maximum_group).unwrap();
    writeln!(out, "    \"classified_groups\": {},", row.classified_groups).unwrap();
    writeln!(out, "    \"other_collision_groups\": {},", row.other_groups).unwrap();
    writeln!(out, "    \"disjoint_collision_pairs\": {},", row.disjoint_pairs).unwrap();
    write!(out, "    \"exact_group_size_histogram\": {{").unwrap();
    write_map(out, &row.group_histogram);
    writeln!(out, "}},").unwrap();
    write!(out, "    \"common_intersection_size_histogram\": {{").unwrap();
    write_map(out, &row.common_histogram);
    writeln!(out, "}},").unwrap();
    writeln!(out, "    \"peak_bucket_records\": {}", row.peak_bucket_records).unwrap();
    writeln!(out, "  }}{}", if final_row { "" } else { "," }).unwrap();
}

fn main() {
    let output_path = env::args().nth(1).unwrap_or_else(|| {
        "d128_small_set_moment_collision_output.json".to_string()
    });
    let temporary_directory = env::args().nth(2).map(PathBuf::from).unwrap_or_else(|| {
        PathBuf::from("d128_small_set_moment_collision_buckets")
    });
    assert!(!temporary_directory.exists());
    let started = Instant::now();
    let (moments, blocks) = domain();
    let e4 = classify(4, &moments, &blocks, &temporary_directory.join("e4"));
    let e5 = classify(5, &moments, &blocks, &temporary_directory.join("e5"));
    remove_dir(&temporary_directory).unwrap();

    assert_eq!((e4.distinct_keys, e4.collision_groups, e4.maximum_group), (10_667_969, 1, 32));
    assert_eq!((e4.classified_groups, e4.other_groups, e4.disjoint_pairs), (1, 0, 496));
    assert_eq!((e5.distinct_keys, e5.collision_groups, e5.maximum_group), (264_562_560, 128, 31));
    assert_eq!((e5.classified_groups, e5.other_groups, e5.disjoint_pairs), (128, 0, 0));

    let mut out = std::io::BufWriter::new(File::create(output_path).unwrap());
    writeln!(out, "{{").unwrap();
    writeln!(out, "  \"verdict\": \"PASS_D128_SMALL_SET_MOMENT_CLASSIFICATION\",").unwrap();
    writeln!(out, "  \"field\": {P},").unwrap();
    writeln!(out, "  \"torus_generator_parameter\": 3,").unwrap();
    writeln!(out, "  \"root_count\": 128,").unwrap();
    writeln!(out, "  \"T4_block_count\": 32,").unwrap();
    write_row(&mut out, "e4", &e4, false);
    write_row(&mut out, "e5", &e5, false);
    writeln!(out, "  \"fingerprint_collision_safety\": \"Equal exact keys have equal fingerprints; every repeated fingerprint is recovered and regrouped by the full 96-bit key. Hash collisions can add candidates but cannot hide exact collisions.\",").unwrap();
    writeln!(out, "  \"total_seconds\": {:.6}", started.elapsed().as_secs_f64()).unwrap();
    writeln!(out, "}}").unwrap();
}
