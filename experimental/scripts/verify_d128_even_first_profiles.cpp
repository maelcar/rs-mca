#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr std::uint64_t kPrime = 2'147'483'647ULL;
constexpr int kDimension = 64;

struct EvenRecord {
  std::uint64_t sum;
  std::uint64_t support;

  bool operator<(const EvenRecord& other) const {
    if (sum != other.sum) return sum < other.sum;
    return support < other.support;
  }
};

struct OddRecord {
  std::uint64_t key;
  std::uint64_t support;
  std::uint64_t code;

  bool operator<(const OddRecord& other) const {
    if (key != other.key) return key < other.key;
    if (support != other.support) return support < other.support;
    return code < other.code;
  }
};

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

std::uint64_t binomial(int n, int k) {
  k = std::min(k, n - k);
  std::uint64_t answer = 1;
  for (int i = 1; i <= k; ++i) {
    answer = answer * static_cast<std::uint64_t>(n - k + i) /
             static_cast<std::uint64_t>(i);
  }
  return answer;
}

void decode_odd_code(std::uint64_t code, int count, std::vector<int>& coefficients) {
  for (int position = 0; position < count; ++position) {
    const std::uint64_t encoded = (code >> (7 * position)) & 127ULL;
    const int index = static_cast<int>(encoded & 63ULL);
    const int sign = (encoded >> 6U) & 1ULL ? 1 : -1;
    coefficients[index] = 2 * sign;
  }
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 4) {
    std::cerr << "usage: " << argv[0] << " CERTIFICATE NUMBER_OF_TWOS OUTPUT_JSON\n";
    return 2;
  }
  const int twos = std::stoi(argv[2]);
  if (twos < 2 || twos > 4) throw std::runtime_error("NUMBER_OF_TWOS must be 2, 3, or 4");
  const int half_singletons = 7 - twos;
  const int singletons = 2 * half_singletons;

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
  std::array<std::uint64_t, kDimension> squares{};
  std::array<std::uint64_t, kDimension> cubes{};
  for (auto& value : representatives) input >> value;
  if (!input) throw std::runtime_error("could not read representatives");
  for (int i = 0; i < kDimension; ++i) {
    squares[i] = representatives[i] * representatives[i] % kPrime;
    cubes[i] = squares[i] * representatives[i] % kPrime;
  }

  const auto started = std::chrono::steady_clock::now();
  std::vector<EvenRecord> even_records;
  const std::uint64_t expected_even_records = binomial(kDimension, half_singletons);
  even_records.reserve(expected_even_records);
  std::vector<int> selected;
  selected.reserve(half_singletons);
  std::function<void(int, int, std::uint64_t, std::uint64_t)> choose_even =
      [&](int start, int remaining, std::uint64_t sum, std::uint64_t support) {
        if (remaining == 0) {
          even_records.push_back(EvenRecord{sum, support});
          return;
        }
        for (int index = start; index <= kDimension - remaining; ++index) {
          choose_even(index + 1, remaining - 1, (sum + squares[index]) % kPrime,
                      support | (1ULL << index));
        }
      };
  choose_even(0, half_singletons, 0, 0);
  if (even_records.size() != expected_even_records) {
    throw std::runtime_error("even subset census incomplete");
  }
  std::sort(even_records.begin(), even_records.end());

  std::vector<OddRecord> odd_records;
  const std::uint64_t expected_odd_records = binomial(kDimension, twos) * (1ULL << twos);
  odd_records.reserve(expected_odd_records);
  selected.clear();
  selected.reserve(twos);
  std::function<void(int, int)> choose_twos = [&](int start, int remaining) {
    if (remaining != 0) {
      for (int index = start; index <= kDimension - remaining; ++index) {
        selected.push_back(index);
        choose_twos(index + 1, remaining - 1);
        selected.pop_back();
      }
      return;
    }
    for (int sign_bits = 0; sign_bits < (1 << twos); ++sign_bits) {
      std::int64_t first = 0;
      std::int64_t third = 0;
      std::uint64_t support = 0;
      std::uint64_t code = 0;
      for (int position = 0; position < twos; ++position) {
        const int index = selected[position];
        const int sign = (sign_bits >> position) & 1 ? 1 : -1;
        first += 2 * sign * static_cast<std::int64_t>(representatives[index]);
        third += 2 * sign * static_cast<std::int64_t>(cubes[index]);
        support |= 1ULL << index;
        const std::uint64_t encoded = static_cast<std::uint64_t>(index) |
                                      (static_cast<std::uint64_t>(sign > 0) << 6U);
        code |= encoded << (7 * position);
      }
      odd_records.push_back(OddRecord{pack(normalize(first), normalize(third)), support, code});
    }
  };
  choose_twos(0, twos);
  if (odd_records.size() != expected_odd_records) {
    throw std::runtime_error("odd doubled-coordinate census incomplete");
  }
  std::sort(odd_records.begin(), odd_records.end());

  std::uint64_t even_equal_sum_pairs = 0;
  std::uint64_t even_disjoint_relations = 0;
  std::uint64_t singleton_sign_patterns = 0;
  std::uint64_t raw_odd_syndrome_matches = 0;
  bool found = false;
  std::uint64_t found_positive_half = 0;
  std::uint64_t found_negative_half = 0;
  std::uint64_t found_odd_code = 0;
  int found_beta_bits = 0;

  for (std::size_t group_begin = 0; group_begin < even_records.size() && !found;) {
    std::size_t group_end = group_begin + 1;
    while (group_end < even_records.size() &&
           even_records[group_end].sum == even_records[group_begin].sum) {
      ++group_end;
    }
    for (std::size_t left = group_begin; left < group_end && !found; ++left) {
      for (std::size_t right = left + 1; right < group_end && !found; ++right) {
        ++even_equal_sum_pairs;
        const std::uint64_t positive_half = even_records[left].support;
        const std::uint64_t negative_half = even_records[right].support;
        if ((positive_half & negative_half) != 0) continue;
        ++even_disjoint_relations;
        const std::uint64_t singleton_support = positive_half | negative_half;
        std::array<int, 10> singleton_indices{};
        int singleton_count = 0;
        for (int index = 0; index < kDimension; ++index) {
          if ((singleton_support >> index) & 1ULL) singleton_indices[singleton_count++] = index;
        }
        if (singleton_count != singletons) throw std::runtime_error("bad singleton support");

        for (int beta_bits = 0; beta_bits < (1 << singletons) && !found; ++beta_bits) {
          ++singleton_sign_patterns;
          std::int64_t first = 0;
          std::int64_t third = 0;
          for (int position = 0; position < singletons; ++position) {
            const int sign = (beta_bits >> position) & 1 ? 1 : -1;
            const int index = singleton_indices[position];
            first += sign * static_cast<std::int64_t>(representatives[index]);
            third += sign * static_cast<std::int64_t>(cubes[index]);
          }
          const std::uint64_t target = opposite(pack(normalize(first), normalize(third)));
          const auto lower = std::lower_bound(
              odd_records.begin(), odd_records.end(), target,
              [](const OddRecord& record, std::uint64_t sought) { return record.key < sought; });
          for (auto iterator = lower;
               iterator != odd_records.end() && iterator->key == target; ++iterator) {
            ++raw_odd_syndrome_matches;
            if ((iterator->support & singleton_support) != 0) continue;
            found = true;
            found_positive_half = positive_half;
            found_negative_half = negative_half;
            found_odd_code = iterator->code;
            found_beta_bits = beta_bits;
            break;
          }
        }
      }
    }
    group_begin = group_end;
  }

  std::vector<int> odd_coefficients(kDimension, 0);
  std::vector<std::uint64_t> positive_roots;
  std::vector<std::uint64_t> negative_roots;
  std::array<int, 32> positive_block_counts{};
  std::array<int, 32> negative_block_counts{};
  if (found) {
    decode_odd_code(found_odd_code, twos, odd_coefficients);
    const std::uint64_t singleton_support = found_positive_half | found_negative_half;
    std::array<int, 10> singleton_indices{};
    int singleton_count = 0;
    for (int index = 0; index < kDimension; ++index) {
      if ((singleton_support >> index) & 1ULL) singleton_indices[singleton_count++] = index;
    }
    for (int position = 0; position < singleton_count; ++position) {
      const int index = singleton_indices[position];
      odd_coefficients[index] = (found_beta_bits >> position) & 1 ? 1 : -1;
    }

    for (int index = 0; index < kDimension; ++index) {
      const int coefficient = odd_coefficients[index];
      if (std::abs(coefficient) == 2) {
        const int alpha = coefficient / 2;
        positive_roots.push_back(alpha > 0 ? representatives[index]
                                           : kPrime - representatives[index]);
        negative_roots.push_back(alpha > 0 ? kPrime - representatives[index]
                                           : representatives[index]);
        ++positive_block_counts[index / 2];
        ++negative_block_counts[index / 2];
      } else if (std::abs(coefficient) == 1) {
        const int tau = (found_positive_half >> index) & 1ULL ? 1 : -1;
        const int relative_root_sign = coefficient * tau;
        const std::uint64_t root = relative_root_sign > 0
                                       ? representatives[index]
                                       : kPrime - representatives[index];
        if (tau > 0) {
          positive_roots.push_back(root);
          ++positive_block_counts[index / 2];
        } else {
          negative_roots.push_back(root);
          ++negative_block_counts[index / 2];
        }
      }
    }
    if (positive_roots.size() != 7 || negative_roots.size() != 7) {
      throw std::runtime_error("reconstructed collision has wrong cardinalities");
    }
    if (*std::max_element(positive_block_counts.begin(), positive_block_counts.end()) >= 4 ||
        *std::max_element(negative_block_counts.begin(), negative_block_counts.end()) >= 4) {
      throw std::runtime_error("reconstructed collision is not block-free");
    }
    for (int degree = 1; degree <= 3; ++degree) {
      std::uint64_t positive_moment = 0;
      std::uint64_t negative_moment = 0;
      for (const std::uint64_t root : positive_roots) {
        std::uint64_t power = 1;
        for (int exponent = 0; exponent < degree; ++exponent) power = power * root % kPrime;
        positive_moment = (positive_moment + power) % kPrime;
      }
      for (const std::uint64_t root : negative_roots) {
        std::uint64_t power = 1;
        for (int exponent = 0; exponent < degree; ++exponent) power = power * root % kPrime;
        negative_moment = (negative_moment + power) % kPrime;
      }
      if (positive_moment != negative_moment) {
        throw std::runtime_error("reconstructed collision fails a moment check");
      }
    }
  }

  const double seconds = std::chrono::duration<double>(
                             std::chrono::steady_clock::now() - started)
                             .count();
  std::ofstream output(argv[3]);
  if (!output) throw std::runtime_error("could not open output");
  output << "{\n";
  output << "  \"verdict\": \""
         << (found ? "COUNTEREXAMPLE_BLOCKFREE_7_VS_7"
                   : "PASS_EXCLUDE_EVEN_FIRST_PROFILE")
         << "\",\n";
  output << "  \"twos\": " << twos << ",\n";
  output << "  \"singletons\": " << singletons << ",\n";
  output << "  \"even_half_subset_records\": " << even_records.size() << ",\n";
  output << "  \"even_equal_sum_pairs\": " << even_equal_sum_pairs << ",\n";
  output << "  \"even_disjoint_relations\": " << even_disjoint_relations << ",\n";
  output << "  \"doubled_odd_records\": " << odd_records.size() << ",\n";
  output << "  \"singleton_sign_patterns\": " << singleton_sign_patterns << ",\n";
  output << "  \"raw_odd_syndrome_matches\": " << raw_odd_syndrome_matches << ",\n";
  output << "  \"collision_found\": " << (found ? "true" : "false") << ",\n";
  output << "  \"positive_roots\": [";
  for (std::size_t i = 0; i < positive_roots.size(); ++i) {
    if (i) output << ", ";
    output << positive_roots[i];
  }
  output << "],\n";
  output << "  \"negative_roots\": [";
  for (std::size_t i = 0; i < negative_roots.size(); ++i) {
    if (i) output << ", ";
    output << negative_roots[i];
  }
  output << "],\n";
  output << "  \"wall_seconds\": " << seconds << "\n";
  output << "}\n";

  std::cout << (found ? "COUNTEREXAMPLE_BLOCKFREE_7_VS_7"
                      : "PASS_EXCLUDE_EVEN_FIRST_PROFILE")
            << " profile=" << twos << ',' << singletons
            << " even_records=" << even_records.size()
            << " even_relations=" << even_disjoint_relations
            << " odd_patterns=" << singleton_sign_patterns
            << " odd_matches=" << raw_odd_syndrome_matches
            << " seconds=" << seconds << '\n';
  return found ? 1 : 0;
}
