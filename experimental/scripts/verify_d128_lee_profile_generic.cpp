#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr std::uint64_t kPrime = 2'147'483'647ULL;
constexpr int kDimension = 64;

struct Record {
  std::uint64_t key;
  std::uint64_t support;

  bool operator<(const Record& other) const {
    if (key != other.key) return key < other.key;
    return support < other.support;
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

std::uint64_t cube(std::uint64_t value) {
  return value * value % kPrime * value % kPrime;
}

std::uint64_t binomial(int n, int k) {
  if (k < 0 || k > n) return 0;
  k = std::min(k, n - k);
  std::uint64_t answer = 1;
  for (int i = 1; i <= k; ++i) {
    answer = answer * static_cast<std::uint64_t>(n - k + i) /
             static_cast<std::uint64_t>(i);
  }
  return answer;
}

std::uint64_t expected_assignments(int twos, int ones) {
  const int support = twos + ones;
  return binomial(kDimension, support) * binomial(support, twos) *
         (1ULL << support);
}

class AssignmentGenerator {
 public:
  using Callback = std::function<bool(std::uint64_t, std::uint64_t, std::uint64_t)>;

  AssignmentGenerator(const std::array<std::uint64_t, kDimension>& first,
                      const std::array<std::uint64_t, kDimension>& third,
                      int twos, int ones, Callback callback)
      : first_(first), third_(third), twos_(twos), ones_(ones),
        callback_(std::move(callback)) {
    selected_.reserve(twos + ones);
  }

  bool run() { return choose_twos(0, twos_); }
  std::uint64_t count() const { return count_; }

 private:
  bool choose_twos(int start, int remaining) {
    if (remaining == 0) return choose_ones(0, ones_);
    for (int index = start; index <= kDimension - remaining; ++index) {
      used_[index] = true;
      selected_.push_back(index);
      if (choose_twos(index + 1, remaining - 1)) return true;
      selected_.pop_back();
      used_[index] = false;
    }
    return false;
  }

  bool choose_ones(int start, int remaining) {
    if (remaining == 0) return emit_signs();
    for (int index = start; index < kDimension; ++index) {
      if (used_[index]) continue;
      int available_after = 0;
      for (int later = index + 1; later < kDimension; ++later) {
        if (!used_[later]) ++available_after;
      }
      if (available_after < remaining - 1) break;
      used_[index] = true;
      selected_.push_back(index);
      if (choose_ones(index + 1, remaining - 1)) return true;
      selected_.pop_back();
      used_[index] = false;
    }
    return false;
  }

  bool emit_signs() {
    const int support_size = twos_ + ones_;
    const int sign_patterns = 1 << support_size;
    for (int sign_bits = 0; sign_bits < sign_patterns; ++sign_bits) {
      std::int64_t first_sum = 0;
      std::int64_t third_sum = 0;
      std::uint64_t support = 0;
      std::uint64_t code = 0;
      for (int position = 0; position < support_size; ++position) {
        const int index = selected_[position];
        const int magnitude = position < twos_ ? 2 : 1;
        const int sign = (sign_bits >> position) & 1 ? 1 : -1;
        first_sum += sign * magnitude * static_cast<std::int64_t>(first_[index]);
        third_sum += sign * magnitude * static_cast<std::int64_t>(third_[index]);
        support |= 1ULL << index;
        const std::uint64_t encoded = static_cast<std::uint64_t>(index) |
                                      (static_cast<std::uint64_t>(sign > 0) << 6U);
        code |= encoded << (7 * position);
      }
      ++count_;
      if (callback_(pack(normalize(first_sum), normalize(third_sum)), support, code)) {
        return true;
      }
    }
    return false;
  }

  const std::array<std::uint64_t, kDimension>& first_;
  const std::array<std::uint64_t, kDimension>& third_;
  int twos_;
  int ones_;
  Callback callback_;
  std::array<bool, kDimension> used_{};
  std::vector<int> selected_;
  std::uint64_t count_ = 0;
};

void decode(std::uint64_t code, int twos, int ones, std::vector<int>& witness) {
  for (int position = 0; position < twos + ones; ++position) {
    const std::uint64_t encoded = (code >> (7 * position)) & 127ULL;
    const int index = static_cast<int>(encoded & 63ULL);
    const int sign = (encoded >> 6U) & 1ULL ? 1 : -1;
    const int magnitude = position < twos ? 2 : 1;
    if (witness[index] != 0) throw std::runtime_error("overlapping decoded witness");
    witness[index] = sign * magnitude;
  }
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 7) {
    std::cerr << "usage: " << argv[0]
              << " CERT TOTAL_TWOS TOTAL_ONES LEFT_TWOS LEFT_ONES OUTPUT_JSON\n";
    return 2;
  }
  const int total_twos = std::stoi(argv[2]);
  const int total_ones = std::stoi(argv[3]);
  const int left_twos = std::stoi(argv[4]);
  const int left_ones = std::stoi(argv[5]);
  const int right_twos = total_twos - left_twos;
  const int right_ones = total_ones - left_ones;
  if (total_twos < 0 || total_ones < 0 || left_twos < 0 || left_ones < 0 ||
      right_twos < 0 || right_ones < 0 || total_twos + total_ones > 9 ||
      left_twos + left_ones == 0 || right_twos + right_ones == 0) {
    throw std::runtime_error("invalid profile or split");
  }

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

  const std::uint64_t expected_left = expected_assignments(left_twos, left_ones);
  const std::uint64_t expected_right = expected_assignments(right_twos, right_ones);
  const auto started = std::chrono::steady_clock::now();

  std::vector<Record> left_records;
  if (expected_left > static_cast<std::uint64_t>(std::numeric_limits<std::size_t>::max())) {
    throw std::runtime_error("left list does not fit address space");
  }
  left_records.reserve(static_cast<std::size_t>(expected_left));
  AssignmentGenerator left_generator(
      representatives, cubes, left_twos, left_ones,
      [&](std::uint64_t key, std::uint64_t support, std::uint64_t code) {
        static_cast<void>(code);
        left_records.push_back(Record{key, support});
        return false;
      });
  left_generator.run();
  if (left_generator.count() != expected_left || left_records.size() != expected_left) {
    throw std::runtime_error("left census incomplete");
  }
  std::sort(left_records.begin(), left_records.end());

  std::uint64_t raw_syndrome_matches = 0;
  std::uint64_t right_count = 0;
  bool found = false;
  std::uint64_t left_code = 0;
  std::uint64_t right_code = 0;
  std::uint64_t matched_left_key = 0;
  std::uint64_t matched_left_support = 0;
  AssignmentGenerator right_generator(
      representatives, cubes, right_twos, right_ones,
      [&](std::uint64_t key, std::uint64_t support, std::uint64_t code) {
        ++right_count;
        const std::uint64_t first = key >> 31U;
        const std::uint64_t third = key & ((1ULL << 31U) - 1ULL);
        const std::uint64_t target =
            pack(first == 0 ? 0 : kPrime - first, third == 0 ? 0 : kPrime - third);
        const auto lower = std::lower_bound(
            left_records.begin(), left_records.end(), target,
            [](const Record& record, std::uint64_t sought) { return record.key < sought; });
        for (auto iterator = lower;
             iterator != left_records.end() && iterator->key == target; ++iterator) {
          ++raw_syndrome_matches;
          if ((iterator->support & support) != 0) continue;
          matched_left_key = iterator->key;
          matched_left_support = iterator->support;
          right_code = code;
          found = true;
          return true;
        }
        return false;
      });
  right_generator.run();
  if (!found && (right_generator.count() != expected_right || right_count != expected_right)) {
    throw std::runtime_error("right census incomplete");
  }

  std::vector<int> witness(kDimension, 0);
  if (found) {
    AssignmentGenerator reconstruction_generator(
        representatives, cubes, left_twos, left_ones,
        [&](std::uint64_t key, std::uint64_t support, std::uint64_t code) {
          if (key != matched_left_key || support != matched_left_support) return false;
          left_code = code;
          return true;
        });
    const bool reconstructed = reconstruction_generator.run();
    if (!reconstructed) throw std::runtime_error("could not reconstruct left assignment");
    decode(left_code, left_twos, left_ones, witness);
    decode(right_code, right_twos, right_ones, witness);
    int twos = 0;
    int ones = 0;
    std::uint64_t first = 0;
    std::uint64_t third = 0;
    for (int i = 0; i < kDimension; ++i) {
      if (std::abs(witness[i]) == 2) ++twos;
      if (std::abs(witness[i]) == 1) ++ones;
      const std::uint64_t coefficient = normalize(witness[i]);
      first = (first + coefficient * representatives[i]) % kPrime;
      third = (third + coefficient * cubes[i]) % kPrime;
    }
    if (twos != total_twos || ones != total_ones || first != 0 || third != 0) {
      throw std::runtime_error("invalid reconstructed witness");
    }
  }

  const double seconds = std::chrono::duration<double>(
                             std::chrono::steady_clock::now() - started)
                             .count();
  std::ofstream output(argv[6]);
  if (!output) throw std::runtime_error("could not open output");
  output << "{\n";
  output << "  \"verdict\": \""
         << (found ? "COUNTEREXAMPLE_LEE_PROFILE" : "PASS_EXCLUDE_LEE_PROFILE")
         << "\",\n";
  output << "  \"total_twos\": " << total_twos << ",\n";
  output << "  \"total_ones\": " << total_ones << ",\n";
  output << "  \"left_twos\": " << left_twos << ",\n";
  output << "  \"left_ones\": " << left_ones << ",\n";
  output << "  \"left_records\": " << left_generator.count() << ",\n";
  output << "  \"right_records\": " << right_count << ",\n";
  output << "  \"raw_syndrome_matches\": " << raw_syndrome_matches << ",\n";
  output << "  \"disjoint_relation_found\": " << (found ? "true" : "false") << ",\n";
  output << "  \"wall_seconds\": " << seconds << ",\n";
  output << "  \"witness\": [";
  for (int i = 0; i < kDimension; ++i) {
    if (i) output << ", ";
    output << witness[i];
  }
  output << "]\n}\n";

  std::cout << (found ? "COUNTEREXAMPLE_LEE_PROFILE" : "PASS_EXCLUDE_LEE_PROFILE")
            << " profile=" << total_twos << ',' << total_ones
            << " left=" << left_generator.count() << " right=" << right_count
            << " raw_matches=" << raw_syndrome_matches << " seconds=" << seconds << '\n';
  return found ? 1 : 0;
}
