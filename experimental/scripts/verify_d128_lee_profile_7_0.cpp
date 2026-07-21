#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

constexpr std::uint64_t kPrime = 2'147'483'647ULL;
constexpr int kDimension = 64;

struct Triple {
  std::uint64_t support;
  std::uint32_t code;
};

std::uint64_t normalize(std::int64_t value) {
  value %= static_cast<std::int64_t>(kPrime);
  if (value < 0) value += static_cast<std::int64_t>(kPrime);
  return static_cast<std::uint64_t>(value);
}

std::uint64_t pack(std::uint64_t first, std::uint64_t third) {
  if (first >= kPrime || third >= kPrime) {
    throw std::runtime_error("residue outside field");
  }
  return (first << 31U) | third;
}

std::uint64_t cube(std::uint64_t value) {
  return value * value % kPrime * value % kPrime;
}

std::uint32_t encode_triple(int i, int j, int k, int signs) {
  return static_cast<std::uint32_t>(i | (j << 6) | (k << 12) | (signs << 18));
}

void decode_triple(std::uint32_t code, std::array<int, 3>& indices,
                   std::array<int, 3>& signs) {
  indices = {static_cast<int>(code & 63U), static_cast<int>((code >> 6) & 63U),
             static_cast<int>((code >> 12) & 63U)};
  const int sign_bits = static_cast<int>((code >> 18) & 7U);
  for (int q = 0; q < 3; ++q) signs[q] = (sign_bits >> q) & 1 ? 1 : -1;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 3) {
    std::cerr << "usage: " << argv[0] << " SECTOR_CERTIFICATE OUTPUT_JSON\n";
    return 2;
  }

  std::ifstream input(argv[1]);
  if (!input) throw std::runtime_error("could not open sector certificate");
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
    throw std::runtime_error("unexpected sector certificate header");
  }

  std::array<std::uint64_t, kDimension> representatives{};
  std::array<std::uint64_t, kDimension> cubes{};
  for (auto& value : representatives) input >> value;
  if (!input) throw std::runtime_error("could not read representatives");
  for (int i = 0; i < kDimension; ++i) cubes[i] = cube(representatives[i]);

  const auto started = std::chrono::steady_clock::now();
  std::unordered_multimap<std::uint64_t, Triple> triples;
  triples.reserve(400'000);
  std::uint64_t triple_count = 0;
  for (int i = 0; i < kDimension; ++i) {
    for (int j = i + 1; j < kDimension; ++j) {
      for (int k = j + 1; k < kDimension; ++k) {
        for (int sign_bits = 0; sign_bits < 8; ++sign_bits) {
          std::int64_t first = 0;
          std::int64_t third = 0;
          const int indices[3] = {i, j, k};
          for (int q = 0; q < 3; ++q) {
            const int sign = (sign_bits >> q) & 1 ? 1 : -1;
            first += sign * static_cast<std::int64_t>(representatives[indices[q]]);
            third += sign * static_cast<std::int64_t>(cubes[indices[q]]);
          }
          const std::uint64_t support = (1ULL << i) | (1ULL << j) | (1ULL << k);
          triples.emplace(pack(normalize(first), normalize(third)),
                          Triple{support, encode_triple(i, j, k, sign_bits)});
          ++triple_count;
        }
      }
    }
  }

  std::uint64_t quadruple_count = 0;
  std::uint64_t syndrome_matches = 0;
  std::vector<int> witness(kDimension, 0);
  bool found = false;
  for (int i = 0; i < kDimension && !found; ++i) {
    for (int j = i + 1; j < kDimension && !found; ++j) {
      for (int k = j + 1; k < kDimension && !found; ++k) {
        for (int l = k + 1; l < kDimension && !found; ++l) {
          const int indices[4] = {i, j, k, l};
          const std::uint64_t support =
              (1ULL << i) | (1ULL << j) | (1ULL << k) | (1ULL << l);
          for (int sign_bits = 0; sign_bits < 16 && !found; ++sign_bits) {
            ++quadruple_count;
            std::int64_t first = 0;
            std::int64_t third = 0;
            for (int q = 0; q < 4; ++q) {
              const int sign = (sign_bits >> q) & 1 ? 1 : -1;
              first += sign * static_cast<std::int64_t>(representatives[indices[q]]);
              third += sign * static_cast<std::int64_t>(cubes[indices[q]]);
            }
            const std::uint64_t first_residue = normalize(first);
            const std::uint64_t third_residue = normalize(third);
            const std::uint64_t target = pack(first_residue == 0 ? 0 : kPrime - first_residue,
                                              third_residue == 0 ? 0 : kPrime - third_residue);
            const auto range = triples.equal_range(target);
            for (auto iterator = range.first; iterator != range.second; ++iterator) {
              ++syndrome_matches;
              if ((iterator->second.support & support) != 0) continue;
              std::array<int, 3> triple_indices{};
              std::array<int, 3> triple_signs{};
              decode_triple(iterator->second.code, triple_indices, triple_signs);
              for (int q = 0; q < 3; ++q) witness[triple_indices[q]] = triple_signs[q];
              for (int q = 0; q < 4; ++q) {
                witness[indices[q]] = (sign_bits >> q) & 1 ? 1 : -1;
              }
              found = true;
              break;
            }
          }
        }
      }
    }
  }

  if (!found && quadruple_count != 10'166'016ULL) {
    throw std::runtime_error("quadruple census incomplete");
  }
  if (triple_count != 333'312ULL) {
    throw std::runtime_error("triple census incomplete");
  }

  if (found) {
    std::uint64_t first = 0;
    std::uint64_t third = 0;
    int support = 0;
    for (int i = 0; i < kDimension; ++i) {
      if (witness[i] == 0) continue;
      ++support;
      const std::uint64_t coefficient = witness[i] > 0 ? 1 : kPrime - 1;
      first = (first + coefficient * representatives[i]) % kPrime;
      third = (third + coefficient * cubes[i]) % kPrime;
    }
    if (support != 7 || first != 0 || third != 0) {
      throw std::runtime_error("invalid reconstructed witness");
    }
  }

  const double seconds = std::chrono::duration<double>(
                             std::chrono::steady_clock::now() - started)
                             .count();
  std::ofstream output(argv[2]);
  if (!output) throw std::runtime_error("could not open output");
  output << "{\n";
  output << "  \"verdict\": \""
         << (found ? "COUNTEREXAMPLE_PROFILE_7_0" : "PASS_EXCLUDE_PROFILE_7_0")
         << "\",\n";
  output << "  \"triple_records\": " << triple_count << ",\n";
  output << "  \"quadruple_records\": " << quadruple_count << ",\n";
  output << "  \"raw_syndrome_matches\": " << syndrome_matches << ",\n";
  output << "  \"disjoint_relation_found\": " << (found ? "true" : "false") << ",\n";
  output << "  \"wall_seconds\": " << seconds << ",\n";
  output << "  \"witness\": [";
  for (int i = 0; i < kDimension; ++i) {
    if (i) output << ", ";
    output << witness[i];
  }
  output << "]\n}\n";

  std::cout << (found ? "COUNTEREXAMPLE_PROFILE_7_0" : "PASS_EXCLUDE_PROFILE_7_0")
            << " triples=" << triple_count << " quadruples=" << quadruple_count
            << " raw_matches=" << syndrome_matches << " seconds=" << seconds << '\n';
  return found ? 1 : 0;
}
