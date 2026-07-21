#include <algorithm>
#include <array>
#include <atomic>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

namespace {

constexpr std::uint64_t kPrime = 2'147'483'647ULL;
constexpr int kDimension = 64;
constexpr std::uint64_t kLeftCount = 243'984'384ULL;
constexpr std::uint64_t kRightSupports = 38'122'560ULL;
constexpr std::uint64_t kRightCount = 1'219'921'920ULL;
constexpr std::uint64_t kBloomBits = 1ULL << 32U;
constexpr std::uint64_t kBloomMask = kBloomBits - 1ULL;

std::uint64_t normalize(std::int64_t value) {
  value %= static_cast<std::int64_t>(kPrime);
  if (value < 0) value += static_cast<std::int64_t>(kPrime);
  return static_cast<std::uint64_t>(value);
}

std::uint64_t pack(std::uint64_t first, std::uint64_t third) {
  return (first << 31U) | third;
}

std::uint64_t opposite(std::uint64_t key) {
  const std::uint64_t first = key >> 31U;
  const std::uint64_t third = key & ((1ULL << 31U) - 1ULL);
  return pack(first == 0 ? 0 : kPrime - first, third == 0 ? 0 : kPrime - third);
}

std::uint64_t cube(std::uint64_t value) {
  return value * value % kPrime * value % kPrime;
}

std::uint64_t mix(std::uint64_t value) {
  value += 0x9e3779b97f4a7c15ULL;
  value = (value ^ (value >> 30U)) * 0xbf58476d1ce4e5b9ULL;
  value = (value ^ (value >> 27U)) * 0x94d049bb133111ebULL;
  return value ^ (value >> 31U);
}

std::uint64_t encode_job(const std::array<int, 5>& indices) {
  std::uint64_t code = 0;
  for (int position = 0; position < 5; ++position) {
    code |= static_cast<std::uint64_t>(indices[position]) << (6 * position);
  }
  return code;
}

std::array<int, 5> decode_job(std::uint64_t code) {
  std::array<int, 5> indices{};
  for (int position = 0; position < 5; ++position) {
    indices[position] = static_cast<int>((code >> (6 * position)) & 63ULL);
  }
  return indices;
}

template <class Callback>
void enumerate_signs(const std::array<int, 5>& indices,
                     const std::array<int, 5>& magnitudes,
                     const std::array<std::uint64_t, kDimension>& first,
                     const std::array<std::uint64_t, kDimension>& third,
                     Callback&& callback) {
  std::array<std::int64_t, 5> weighted_first{};
  std::array<std::int64_t, 5> weighted_third{};
  std::int64_t first_sum = 0;
  std::int64_t third_sum = 0;
  for (int position = 0; position < 5; ++position) {
    weighted_first[position] =
        magnitudes[position] * static_cast<std::int64_t>(first[indices[position]]);
    weighted_third[position] =
        magnitudes[position] * static_cast<std::int64_t>(third[indices[position]]);
    first_sum -= weighted_first[position];
    third_sum -= weighted_third[position];
  }

  unsigned gray = 0;
  for (unsigned step = 0; step < 32; ++step) {
    callback(pack(normalize(first_sum), normalize(third_sum)));
    if (step == 31) break;
    const unsigned next_gray = (step + 1U) ^ ((step + 1U) >> 1U);
    const unsigned changed = gray ^ next_gray;
    const int position = std::countr_zero(changed);
    if ((next_gray >> position) & 1U) {
      first_sum += 2 * weighted_first[position];
      third_sum += 2 * weighted_third[position];
    } else {
      first_sum -= 2 * weighted_first[position];
      third_sum -= 2 * weighted_third[position];
    }
    gray = next_gray;
  }
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 4) {
    std::cerr << "usage: " << argv[0] << " CERTIFICATE THREADS OUTPUT_JSON\n";
    return 2;
  }
  const int threads = std::stoi(argv[2]);
  if (threads < 1 || threads > 256) throw std::runtime_error("invalid thread count");

  std::ifstream input(argv[1]);
  if (!input) throw std::runtime_error("could not open certificate");
  std::string magic;
  std::uint64_t prime = 0;
  int blocks = 0;
  int even_rank = 0;
  int odd_rank = 0;
  int even_radius = 0;
  int odd_radius = 0;
  input >> magic >> prime >> blocks >> even_rank >> odd_rank >> even_radius >> odd_radius;
  if (magic != "D128_ANTIPODAL_SECTOR_CERT_V1" || prime != kPrime ||
      blocks != 32 || even_rank != 32 || odd_rank != kDimension) {
    throw std::runtime_error("unexpected certificate header");
  }
  std::array<std::uint64_t, kDimension> representatives{};
  std::array<std::uint64_t, kDimension> cubes{};
  for (auto& value : representatives) input >> value;
  if (!input) throw std::runtime_error("could not read representatives");
  for (int i = 0; i < kDimension; ++i) cubes[i] = cube(representatives[i]);

  const auto started = std::chrono::steady_clock::now();
  std::vector<std::uint64_t> left_keys;
  left_keys.reserve(kLeftCount);
  const std::array<int, 5> unit_magnitudes = {1, 1, 1, 1, 1};
  for (int a = 0; a < kDimension; ++a) {
    for (int b = a + 1; b < kDimension; ++b) {
      for (int c = b + 1; c < kDimension; ++c) {
        for (int d = c + 1; d < kDimension; ++d) {
          for (int e = d + 1; e < kDimension; ++e) {
            const std::array<int, 5> indices = {a, b, c, d, e};
            enumerate_signs(indices, unit_magnitudes, representatives, cubes,
                            [&](std::uint64_t key) { left_keys.push_back(key); });
          }
        }
      }
    }
  }
  if (left_keys.size() != kLeftCount) throw std::runtime_error("left census incomplete");

  std::vector<std::uint64_t> bloom(kBloomBits / 64ULL, 0);
  for (const std::uint64_t key : left_keys) {
    const std::uint64_t hash = mix(key);
    const std::uint64_t first_bit = hash & kBloomMask;
    const std::uint64_t second_bit = (hash >> 32U) & kBloomMask;
    bloom[first_bit >> 6U] |= 1ULL << (first_bit & 63ULL);
    bloom[second_bit >> 6U] |= 1ULL << (second_bit & 63ULL);
  }
  std::sort(left_keys.begin(), left_keys.end());

  std::vector<std::uint64_t> jobs;
  jobs.reserve(kRightSupports);
  for (int a = 0; a < kDimension; ++a) {
    for (int b = a + 1; b < kDimension; ++b) {
      for (int c = b + 1; c < kDimension; ++c) {
        for (int d = c + 1; d < kDimension; ++d) {
          for (int e = 0; e < kDimension; ++e) {
            if (e == a || e == b || e == c || e == d) continue;
            jobs.push_back(encode_job({a, b, c, d, e}));
          }
        }
      }
    }
  }
  if (jobs.size() != kRightSupports) throw std::runtime_error("right support census incomplete");

  std::atomic<bool> found = false;
  std::atomic<std::uint64_t> found_key = 0;
  std::vector<std::thread> workers;
  std::vector<std::uint64_t> local_assignments(threads, 0);
  std::vector<std::uint64_t> local_bloom_passes(threads, 0);
  const std::array<int, 5> right_magnitudes = {2, 2, 2, 2, 1};
  for (int thread = 0; thread < threads; ++thread) {
    const std::size_t begin = jobs.size() * static_cast<std::size_t>(thread) / threads;
    const std::size_t end = jobs.size() * static_cast<std::size_t>(thread + 1) / threads;
    workers.emplace_back([&, thread, begin, end] {
      for (std::size_t job = begin; job < end && !found.load(std::memory_order_relaxed); ++job) {
        const std::array<int, 5> indices = decode_job(jobs[job]);
        enumerate_signs(indices, right_magnitudes, representatives, cubes,
                        [&](std::uint64_t key) {
          ++local_assignments[thread];
          if (found.load(std::memory_order_relaxed)) return;
          const std::uint64_t target = opposite(key);
          const std::uint64_t hash = mix(target);
          const std::uint64_t first_bit = hash & kBloomMask;
          const std::uint64_t second_bit = (hash >> 32U) & kBloomMask;
          if (((bloom[first_bit >> 6U] >> (first_bit & 63ULL)) & 1ULL) == 0 ||
              ((bloom[second_bit >> 6U] >> (second_bit & 63ULL)) & 1ULL) == 0) {
            return;
          }
          ++local_bloom_passes[thread];
          if (std::binary_search(left_keys.begin(), left_keys.end(), target)) {
            found_key.store(target, std::memory_order_relaxed);
            found.store(true, std::memory_order_relaxed);
          }
        });
      }
    });
  }
  for (auto& worker : workers) worker.join();

  std::uint64_t right_assignments = 0;
  std::uint64_t bloom_passes = 0;
  for (int thread = 0; thread < threads; ++thread) {
    right_assignments += local_assignments[thread];
    bloom_passes += local_bloom_passes[thread];
  }
  if (!found && right_assignments != kRightCount) {
    throw std::runtime_error("right sign census incomplete");
  }

  const double seconds = std::chrono::duration<double>(
                             std::chrono::steady_clock::now() - started)
                             .count();
  std::ofstream output(argv[3]);
  if (!output) throw std::runtime_error("could not open output");
  output << "{\n";
  output << "  \"verdict\": \""
         << (found ? "RAW_SYNDROME_MATCH_REQUIRES_DISJOINT_AUDIT"
                   : "PASS_EXCLUDE_PROFILE_4_6_BY_RAW_SYNDROME")
         << "\",\n";
  output << "  \"left_records\": " << left_keys.size() << ",\n";
  output << "  \"right_supports\": " << jobs.size() << ",\n";
  output << "  \"right_assignments\": " << right_assignments << ",\n";
  output << "  \"bloom_bits\": " << kBloomBits << ",\n";
  output << "  \"bloom_passes\": " << bloom_passes << ",\n";
  output << "  \"raw_syndrome_match_found\": " << (found ? "true" : "false") << ",\n";
  output << "  \"matched_key\": " << found_key.load() << ",\n";
  output << "  \"threads\": " << threads << ",\n";
  output << "  \"wall_seconds\": " << seconds << "\n";
  output << "}\n";

  std::cout << (found ? "RAW_SYNDROME_MATCH_REQUIRES_DISJOINT_AUDIT"
                      : "PASS_EXCLUDE_PROFILE_4_6_BY_RAW_SYNDROME")
            << " left=" << left_keys.size() << " right=" << right_assignments
            << " bloom_passes=" << bloom_passes << " threads=" << threads
            << " seconds=" << seconds << '\n';
  return found ? 1 : 0;
}
