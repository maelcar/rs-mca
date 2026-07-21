//! Exhaustively classify equal-three-moment six-subsets using exact
//! 64-bit fingerprints followed by exact-key recovery.

use std::collections::{BTreeMap, HashMap};
use std::env;
use std::fs::{create_dir_all, remove_dir, remove_file, File};
use std::io::{Read, Write};
use std::path::{Path, PathBuf};
use std::time::Instant;

const P: u64 = 2_147_483_647;
const ROOTS: usize = 128;
const SUBSETS: u64 = 5_423_611_200;
const BUCKET_BITS: usize = 6;
const BUCKETS: usize = 1 << BUCKET_BITS;
const BUFFER_WORDS: usize = 1 << 16;
const PREFIX_BITS: usize = 24;

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Key(u32, u32, u32);

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Mask(u64, u64);

impl Mask {
    fn from_indices(indices: [usize; 6]) -> Self {
        let mut answer = Self(0, 0);
        for index in indices {
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
    if sum >= P {
        (sum - P) as u32
    } else {
        sum as u32
    }
}

fn add(left: Key, right: Key) -> Key {
    Key(
        add_coordinate(left.0, right.0),
        add_coordinate(left.1, right.1),
        add_coordinate(left.2, right.2),
    )
}

fn fingerprint(key: Key) -> u64 {
    let mut value = (key.0 as u64).wrapping_mul(0x9e37_79b1_85eb_ca87);
    value ^= (key.1 as u64)
        .wrapping_mul(0xc2b2_ae3d_27d4_eb4f)
        .rotate_left(21);
    value ^= (key.2 as u64)
        .wrapping_mul(0x1656_67b1_9e37_79f9)
        .rotate_left(42);
    value ^= value >> 30;
    value = value.wrapping_mul(0xbf58_476d_1ce4_e5b9);
    value ^= value >> 27;
    value = value.wrapping_mul(0x94d0_49bb_1331_11eb);
    value ^ (value >> 31)
}

fn domain() -> ([u32; ROOTS], [Key; ROOTS], Vec<Mask>) {
    let eta = power(cayley(2), 1u64 << 22);
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
    roots
        .windows(2)
        .for_each(|pair| assert_ne!(pair[0], pair[1]));
    roots
        .iter()
        .for_each(|&root| assert_eq!(chebyshev(128, root), 0));

    let mut moments = [Key(0, 0, 0); ROOTS];
    let mut blocks = BTreeMap::<u32, Vec<usize>>::new();
    for (index, &root) in roots.iter().enumerate() {
        let square = root as u64 * root as u64 % P;
        moments[index] = Key(root, square as u32, (square * root as u64 % P) as u32);
        blocks.entry(chebyshev(4, root)).or_default().push(index);
    }
    assert_eq!(blocks.len(), 32);
    let block_masks: Vec<Mask> = blocks
        .into_values()
        .map(|indices| {
            assert_eq!(indices.len(), 4);
            let mut mask = Mask(0, 0);
            for index in indices {
                if index < 64 {
                    mask.0 |= 1u64 << index;
                } else {
                    mask.1 |= 1u64 << (index - 64);
                }
            }
            mask
        })
        .collect();
    (roots, moments, block_masks)
}

fn enumerate_keys<F>(moments: &[Key; ROOTS], mut callback: F) -> u64
where
    F: FnMut(Key),
{
    let mut count = 0u64;
    for a in 0..123 {
        for b in a + 1..124 {
            let ab = add(moments[a], moments[b]);
            for c in b + 1..125 {
                let abc = add(ab, moments[c]);
                for d in c + 1..126 {
                    let abcd = add(abc, moments[d]);
                    for e in d + 1..127 {
                        let abcde = add(abcd, moments[e]);
                        for &last in moments.iter().skip(e + 1) {
                            callback(add(abcde, last));
                            count += 1;
                        }
                    }
                }
            }
        }
    }
    count
}

fn enumerate_keys_and_masks<F>(moments: &[Key; ROOTS], mut callback: F) -> u64
where
    F: FnMut(Key, Mask),
{
    let mut count = 0u64;
    for a in 0..123 {
        for b in a + 1..124 {
            let ab = add(moments[a], moments[b]);
            for c in b + 1..125 {
                let abc = add(ab, moments[c]);
                for d in c + 1..126 {
                    let abcd = add(abc, moments[d]);
                    for e in d + 1..127 {
                        let abcde = add(abcd, moments[e]);
                        for (f, &last) in moments.iter().enumerate().skip(e + 1) {
                            callback(add(abcde, last), Mask::from_indices([a, b, c, d, e, f]));
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
    written: u64,
}

impl BucketWriter {
    fn new(path: &Path) -> Self {
        Self {
            file: File::create(path).expect("cannot create fingerprint bucket"),
            words: Vec::with_capacity(BUFFER_WORDS),
            written: 0,
        }
    }

    fn push(&mut self, value: u64) {
        self.words.push(value);
        if self.words.len() == BUFFER_WORDS {
            self.flush();
        }
    }

    fn flush(&mut self) {
        if self.words.is_empty() {
            return;
        }
        let bytes = unsafe {
            std::slice::from_raw_parts(
                self.words.as_ptr() as *const u8,
                self.words.len() * std::mem::size_of::<u64>(),
            )
        };
        self.file
            .write_all(bytes)
            .expect("cannot write fingerprint bucket");
        self.written += self.words.len() as u64;
        self.words.clear();
    }
}

fn read_words(path: &Path) -> Vec<u64> {
    let mut file = File::open(path).expect("cannot open fingerprint bucket");
    let bytes = file.metadata().unwrap().len() as usize;
    assert_eq!(bytes % 8, 0);
    let mut words = Vec::<u64>::with_capacity(bytes / 8);
    unsafe {
        words.set_len(bytes / 8);
        let target = std::slice::from_raw_parts_mut(words.as_mut_ptr() as *mut u8, bytes);
        file.read_exact(target)
            .expect("cannot read fingerprint bucket");
    }
    words
}

fn sort_fingerprints(values: &mut [u64]) {
    values.sort_unstable();
}

fn main() {
    let output_path = env::args()
        .nth(1)
        .unwrap_or_else(|| "O_exhaustive_e6_moment_collision_output.json".to_string());
    let temporary_directory = env::args()
        .nth(2)
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from("d128_e6_fingerprint_buckets"));
    assert!(
        !temporary_directory.exists(),
        "temporary directory already exists"
    );
    create_dir_all(&temporary_directory).expect("cannot create temporary directory");

    let started = Instant::now();
    let (roots, moments, block_masks) = domain();
    let mut writers: Vec<BucketWriter> = (0..BUCKETS)
        .map(|bucket| BucketWriter::new(&bucket_path(&temporary_directory, bucket)))
        .collect();
    let generated_subsets = enumerate_keys(&moments, |key| {
        let value = fingerprint(key);
        writers[value as usize >> (64 - BUCKET_BITS)].push(value);
    });
    assert_eq!(generated_subsets, SUBSETS);
    for writer in &mut writers {
        writer.flush();
    }
    assert_eq!(
        writers.iter().map(|writer| writer.written).sum::<u64>(),
        SUBSETS
    );
    drop(writers);
    let generated = Instant::now();
    eprintln!(
        "generated fingerprints in {:.3}s",
        (generated - started).as_secs_f64()
    );

    let mut duplicate_fingerprints = Vec::<u64>::new();
    let mut fingerprint_group_histogram = BTreeMap::<usize, u64>::new();
    let mut peak_bucket_records = 0usize;
    let mut fingerprints_read = 0u64;
    for bucket in 0..BUCKETS {
        let path = bucket_path(&temporary_directory, bucket);
        let mut values = read_words(&path);
        fingerprints_read += values.len() as u64;
        peak_bucket_records = peak_bucket_records.max(values.len());
        sort_fingerprints(&mut values);
        let mut begin = 0usize;
        while begin < values.len() {
            let mut end = begin + 1;
            while end < values.len() && values[end] == values[begin] {
                end += 1;
            }
            let size = end - begin;
            *fingerprint_group_histogram.entry(size).or_insert(0) += 1;
            if size > 1 {
                duplicate_fingerprints.push(values[begin]);
            }
            begin = end;
        }
        drop(values);
        remove_file(path).expect("cannot remove fingerprint bucket");
        if (bucket + 1) % 8 == 0 {
            eprintln!("classified {} of {BUCKETS} buckets", bucket + 1);
        }
    }
    assert_eq!(fingerprints_read, SUBSETS);
    duplicate_fingerprints.sort_unstable();
    let classified_fingerprints = Instant::now();

    let mut active_prefixes = vec![false; 1 << PREFIX_BITS];
    for &value in &duplicate_fingerprints {
        active_prefixes[(value >> (64 - PREFIX_BITS)) as usize] = true;
    }
    let mut recovered = HashMap::<Key, Vec<Mask>>::new();
    let recovery_subsets = enumerate_keys_and_masks(&moments, |key, mask| {
        let value = fingerprint(key);
        if active_prefixes[(value >> (64 - PREFIX_BITS)) as usize]
            && duplicate_fingerprints.binary_search(&value).is_ok()
        {
            recovered.entry(key).or_default().push(mask);
        }
    });
    assert_eq!(recovery_subsets, SUBSETS);
    let recovered_at = Instant::now();
    eprintln!(
        "recovered exact candidates in {:.3}s",
        (recovered_at - classified_fingerprints).as_secs_f64()
    );

    let mut exact_collision_groups = 0u64;
    let mut exact_colliding_subsets = 0u64;
    let mut exact_distinct_keys = SUBSETS;
    let mut maximum_exact_group = 1usize;
    let mut exact_group_histogram = BTreeMap::<usize, u64>::new();
    let mut fixed_pair_plus_blocks_groups = 0u64;
    let mut other_collision_groups = 0u64;
    let mut disjoint_collision_pairs = 0u64;
    let mut common_intersection_histogram = BTreeMap::<u32, u64>::new();
    let mut first_noncarrier_group = Vec::<Mask>::new();

    for group in recovered.values().filter(|group| group.len() > 1) {
        exact_collision_groups += 1;
        exact_colliding_subsets += group.len() as u64;
        exact_distinct_keys -= (group.len() - 1) as u64;
        maximum_exact_group = maximum_exact_group.max(group.len());
        *exact_group_histogram.entry(group.len()).or_insert(0) += 1;

        let common = group.iter().copied().reduce(Mask::intersection).unwrap();
        *common_intersection_histogram
            .entry(common.cardinality())
            .or_insert(0) += 1;
        for left in 0..group.len() {
            for right in left + 1..group.len() {
                disjoint_collision_pairs += u64::from(group[left].disjoint(group[right]));
            }
        }

        let mut residuals: Vec<Mask> = group
            .iter()
            .copied()
            .map(|mask| mask.difference(common))
            .collect();
        residuals.sort_unstable();
        let mut expected: Vec<Mask> = block_masks
            .iter()
            .copied()
            .filter(|block| block.disjoint(common))
            .collect();
        expected.sort_unstable();
        if common.cardinality() == 2 && residuals == expected {
            fixed_pair_plus_blocks_groups += 1;
        } else {
            other_collision_groups += 1;
            if first_noncarrier_group.is_empty() {
                first_noncarrier_group.extend_from_slice(group);
            }
        }
    }
    remove_dir(&temporary_directory).expect("cannot remove temporary directory");
    let finished = Instant::now();

    let verdict = if other_collision_groups == 0 && disjoint_collision_pairs == 0 {
        "PASS_ALL_E6_COLLISIONS_ARE_FIXED_PAIR_PLUS_T4_BLOCKS"
    } else {
        "NONCARRIER_E6_COLLISION_FOUND"
    };
    let file = File::create(output_path).expect("cannot create output");
    let mut output = std::io::BufWriter::new(file);
    writeln!(output, "{{").unwrap();
    writeln!(output, "  \"verdict\": \"{verdict}\",").unwrap();
    writeln!(output, "  \"field\": {P},").unwrap();
    writeln!(output, "  \"torus_generator_parameter\": 2,").unwrap();
    writeln!(output, "  \"root_count\": {},", roots.len()).unwrap();
    writeln!(output, "  \"T4_block_count\": {},", block_masks.len()).unwrap();
    writeln!(output, "  \"six_subsets_checked\": {SUBSETS},").unwrap();
    writeln!(
        output,
        "  \"exact_distinct_moment_keys\": {exact_distinct_keys},"
    )
    .unwrap();
    writeln!(
        output,
        "  \"exact_collision_groups\": {exact_collision_groups},"
    )
    .unwrap();
    writeln!(
        output,
        "  \"exact_colliding_subsets\": {exact_colliding_subsets},"
    )
    .unwrap();
    writeln!(
        output,
        "  \"maximum_exact_group_size\": {maximum_exact_group},"
    )
    .unwrap();
    writeln!(
        output,
        "  \"fixed_pair_plus_T4_blocks_groups\": {fixed_pair_plus_blocks_groups},"
    )
    .unwrap();
    writeln!(
        output,
        "  \"other_collision_groups\": {other_collision_groups},"
    )
    .unwrap();
    writeln!(
        output,
        "  \"disjoint_collision_pairs\": {disjoint_collision_pairs},"
    )
    .unwrap();
    write!(output, "  \"exact_group_size_histogram\": {{").unwrap();
    for (position, (size, count)) in exact_group_histogram.iter().enumerate() {
        write!(
            output,
            "{}\"{}\": {}",
            if position == 0 { "" } else { ", " },
            size,
            count
        )
        .unwrap();
    }
    writeln!(output, "}},").unwrap();
    write!(output, "  \"common_intersection_size_histogram\": {{").unwrap();
    for (position, (size, count)) in common_intersection_histogram.iter().enumerate() {
        write!(
            output,
            "{}\"{}\": {}",
            if position == 0 { "" } else { ", " },
            size,
            count
        )
        .unwrap();
    }
    writeln!(output, "}},").unwrap();
    writeln!(
        output,
        "  \"duplicate_fingerprints_recovered\": {},",
        duplicate_fingerprints.len()
    )
    .unwrap();
    writeln!(output, "  \"fingerprint_collision_safety\": \"Equal exact keys have equal fingerprints; every repeated fingerprint is recovered and regrouped by the full 96-bit key. Hash collisions can add candidates but cannot hide exact collisions.\",").unwrap();
    writeln!(output, "  \"bucket_count\": {BUCKETS},").unwrap();
    writeln!(output, "  \"external_fingerprint_bytes\": {},", SUBSETS * 8).unwrap();
    writeln!(output, "  \"peak_bucket_records\": {peak_bucket_records},").unwrap();
    if first_noncarrier_group.is_empty() {
        writeln!(output, "  \"first_noncarrier_group\": null,").unwrap();
    } else {
        writeln!(output, "  \"first_noncarrier_group\": [").unwrap();
        for (position, mask) in first_noncarrier_group.iter().enumerate() {
            writeln!(
                output,
                "    {{\"mask_low\": {}, \"mask_high\": {}}}{}",
                mask.0,
                mask.1,
                if position + 1 == first_noncarrier_group.len() {
                    ""
                } else {
                    ","
                }
            )
            .unwrap();
        }
        writeln!(output, "  ],").unwrap();
    }
    writeln!(
        output,
        "  \"generation_seconds\": {:.6},",
        (generated - started).as_secs_f64()
    )
    .unwrap();
    writeln!(
        output,
        "  \"fingerprint_classification_seconds\": {:.6},",
        (classified_fingerprints - generated).as_secs_f64()
    )
    .unwrap();
    writeln!(
        output,
        "  \"exact_recovery_seconds\": {:.6},",
        (recovered_at - classified_fingerprints).as_secs_f64()
    )
    .unwrap();
    writeln!(
        output,
        "  \"exact_group_audit_seconds\": {:.6},",
        (finished - recovered_at).as_secs_f64()
    )
    .unwrap();
    writeln!(
        output,
        "  \"total_seconds\": {:.6},",
        (finished - started).as_secs_f64()
    )
    .unwrap();
    writeln!(output, "  \"temporary_directory_removed\": true,").unwrap();
    writeln!(output, "  \"scope_guard\": \"Exhaustive active-field classification of all equal-first-three-moment six-subsets. The seven-support consequence is a separate exact deduction.\"").unwrap();
    writeln!(output, "}}").unwrap();
}
