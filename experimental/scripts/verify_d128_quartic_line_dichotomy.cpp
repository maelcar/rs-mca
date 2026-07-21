#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr std::int64_t P = 2147483647LL;
constexpr std::int64_t X_ONE = 1556867790LL;

std::int64_t add_mod(std::int64_t a, std::int64_t b) {
  const std::int64_t value = a + b;
  return value >= P ? value - P : value;
}

std::int64_t sub_mod(std::int64_t a, std::int64_t b) {
  const std::int64_t value = a - b;
  return value < 0 ? value + P : value;
}

std::int64_t mul_mod(std::int64_t a, std::int64_t b) {
  return static_cast<std::int64_t>((static_cast<__int128>(a) * b) % P);
}

std::int64_t pow_mod(std::int64_t a, std::int64_t e) {
  std::int64_t out = 1;
  while (e > 0) {
    if (e & 1) out = mul_mod(out, a);
    a = mul_mod(a, a);
    e >>= 1;
  }
  return out;
}

std::int64_t chebyshev(int degree, std::int64_t x) {
  if (degree == 0) return 1;
  if (degree == 1) return x;
  std::int64_t previous = 1;
  std::int64_t current = x;
  for (int i = 1; i < degree; ++i) {
    std::int64_t following = sub_mod(2 * mul_mod(x, current) % P, previous);
    previous = current;
    current = following;
  }
  return current;
}

std::vector<std::int64_t> domain_D128(bool punctured,
                                      std::int64_t& puncture_value) {
  const std::int64_t step_real = chebyshev(2, X_ONE);
  std::int64_t previous = X_ONE;
  std::int64_t current = X_ONE;
  std::vector<std::int64_t> d1024;
  d1024.reserve(1024);
  d1024.push_back(current);
  for (int i = 1; i < 1024; ++i) {
    const std::int64_t following = sub_mod(2 * mul_mod(step_real, current) % P, previous);
    d1024.push_back(following);
    previous = current;
    current = following;
  }
  std::sort(d1024.begin(), d1024.end());
  if (std::unique(d1024.begin(), d1024.end()) != d1024.end()) {
    throw std::runtime_error("D1024 recurrence is not injective");
  }
  std::vector<std::int64_t> out;
  out.reserve(128);
  for (const auto x : d1024) out.push_back(chebyshev(8, x));
  std::sort(out.begin(), out.end());
  out.erase(std::unique(out.begin(), out.end()), out.end());
  if (out.size() != 128) throw std::runtime_error("wrong D128 size");
  puncture_value = chebyshev(8, X_ONE);
  if (punctured) {
    const auto it = std::lower_bound(out.begin(), out.end(), puncture_value);
    if (it == out.end() || *it != puncture_value) throw std::runtime_error("missing puncture");
    out.erase(it);
  }
  return out;
}

struct Point {
  std::uint32_t e1;
  std::uint32_t e2;
  std::uint32_t e3;
  std::uint32_t e4;
  bool operator<(const Point& other) const {
    if (e1 != other.e1) return e1 < other.e1;
    if (e2 != other.e2) return e2 < other.e2;
    if (e3 != other.e3) return e3 < other.e3;
    return e4 < other.e4;
  }
};

struct LineKey {
  std::array<std::uint32_t, 6> v{};
  bool operator<(const LineKey& other) const { return v < other.v; }
  bool operator==(const LineKey& other) const { return v == other.v; }
};

template <class Callback>
std::uint64_t enumerate_quartets(const std::vector<std::int64_t>& domain,
                                 const std::vector<std::int64_t>& t4,
                                 Callback callback) {
  std::uint64_t count = 0;
  const int n = static_cast<int>(domain.size());
  for (int i = 0; i < n - 3; ++i) {
    const auto x1 = domain[i];
    for (int j = i + 1; j < n - 2; ++j) {
      const auto x2 = domain[j];
      const auto e1_2 = add_mod(x1, x2);
      const auto e2_2 = mul_mod(x1, x2);
      for (int k = j + 1; k < n - 1; ++k) {
        const auto x3 = domain[k];
        const auto e1_3 = add_mod(e1_2, x3);
        const auto e2_3 = add_mod(e2_2, mul_mod(x3, e1_2));
        const auto e3_3 = mul_mod(e2_2, x3);
        for (int l = k + 1; l < n; ++l) {
          if (t4[i] == t4[j] && t4[i] == t4[k] && t4[i] == t4[l]) continue;
          const auto x4 = domain[l];
          const Point point{
              static_cast<std::uint32_t>(add_mod(e1_3, x4)),
              static_cast<std::uint32_t>(add_mod(e2_3, mul_mod(x4, e1_3))),
              static_cast<std::uint32_t>(add_mod(e3_3, mul_mod(x4, e2_3))),
              static_cast<std::uint32_t>(mul_mod(e3_3, x4)),
          };
          callback(point, std::array<int, 4>{i, j, k, l});
          ++count;
        }
      }
    }
  }
  return count;
}

LineKey make_line(const Point& x, const Point& y, std::int64_t inverse) {
  const auto d2 = sub_mod(y.e2, x.e2);
  const auto d3 = sub_mod(y.e3, x.e3);
  const auto d4 = sub_mod(y.e4, x.e4);
  LineKey key;
  if (d2 != 0) {
    const auto a = mul_mod(d3, inverse);
    const auto b = mul_mod(d4, inverse);
    const auto c = sub_mod(x.e3, mul_mod(a, x.e2));
    const auto d = sub_mod(x.e4, mul_mod(b, x.e2));
    key.v = {0, x.e1, static_cast<std::uint32_t>(a), static_cast<std::uint32_t>(b),
             static_cast<std::uint32_t>(c), static_cast<std::uint32_t>(d)};
  } else {
    if (d3 == 0) throw std::runtime_error("two canonical quartets share e1,e2,e3");
    const auto b = mul_mod(d4, inverse);
    const auto c = sub_mod(x.e4, mul_mod(b, x.e3));
    key.v = {1, x.e1, static_cast<std::uint32_t>(b), x.e2,
             static_cast<std::uint32_t>(c), 0};
  }
  return key;
}

bool point_on_line(const Point& x, const LineKey& key) {
  if (x.e1 != key.v[1]) return false;
  if (key.v[0] == 0) {
    return x.e3 == add_mod(mul_mod(key.v[2], x.e2), key.v[4]) &&
           x.e4 == add_mod(mul_mod(key.v[3], x.e2), key.v[5]);
  }
  return x.e2 == key.v[3] &&
         x.e4 == add_mod(mul_mod(key.v[2], x.e3), key.v[4]);
}

bool is_opposite_pair_carrier(const LineKey& key) {
  if (key.v[0] != 0) return false;
  const auto s = key.v[1];
  const auto p = key.v[3];
  return key.v[2] == s &&
         key.v[4] == sub_mod(0, mul_mod(s, p)) &&
         key.v[5] == sub_mod(0, mul_mod(p, p));
}

std::uint64_t triangular_root(std::uint64_t pairs) {
  const long double disc = 1.0L + 8.0L * static_cast<long double>(pairs);
  std::uint64_t r = static_cast<std::uint64_t>((1.0L + std::sqrt(disc)) / 2.0L);
  while (r * (r - 1) / 2 < pairs) ++r;
  while (r > 0 && r * (r - 1) / 2 > pairs) --r;
  if (r * (r - 1) / 2 != pairs) throw std::runtime_error("line pair count is not triangular");
  return r;
}

void print_line(const LineKey& key) {
  std::cout << '[';
  for (int i = 0; i < 6; ++i) {
    if (i) std::cout << ',';
    std::cout << key.v[i];
  }
  std::cout << ']';
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const bool punctured = !(argc >= 2 && std::string(argv[1]) == "--full");
    std::int64_t puncture_value = 0;
    const auto domain = domain_D128(punctured, puncture_value);
    std::vector<std::int64_t> t4;
    t4.reserve(domain.size());
    for (const auto x : domain) t4.push_back(chebyshev(4, x));

    std::vector<Point> points;
    points.reserve(11000000);
    const auto generated = enumerate_quartets(
        domain, t4, [&](const Point& point, const std::array<int, 4>&) {
          points.push_back(point);
        });
    const std::uint64_t quartet_count = generated;
    const std::uint64_t expected_quartets =
        punctured ? 10334594ULL : 10667968ULL;
    if (quartet_count != expected_quartets) {
      throw std::runtime_error("quartet count mismatch");
    }
    std::sort(points.begin(), points.end());

    std::vector<LineKey> lines;
    lines.reserve(18000000);
    std::uint64_t pair_count = 0;
    for (std::size_t begin = 0; begin < points.size();) {
      std::size_t end = begin + 1;
      while (end < points.size() && points[end].e1 == points[begin].e1) ++end;
      const std::size_t group_size = end - begin;
      const std::size_t group_pairs = group_size * (group_size - 1) / 2;
      std::vector<std::int64_t> denominators;
      denominators.reserve(group_pairs);
      for (std::size_t i = begin; i < end; ++i) {
        for (std::size_t j = i + 1; j < end; ++j) {
          const auto d2 = sub_mod(points[j].e2, points[i].e2);
          const auto d3 = sub_mod(points[j].e3, points[i].e3);
          if (d2 == 0 && d3 == 0) {
            throw std::runtime_error("constant-direction canonical collision");
          }
          denominators.push_back(d2 != 0 ? d2 : d3);
        }
      }
      std::vector<std::int64_t> inverses(denominators.size());
      std::int64_t product = 1;
      for (std::size_t i = 0; i < denominators.size(); ++i) {
        inverses[i] = product;
        product = mul_mod(product, denominators[i]);
      }
      std::int64_t inverse_product = pow_mod(product, P - 2);
      for (std::size_t i = denominators.size(); i-- > 0;) {
        const auto prefix = inverses[i];
        inverses[i] = mul_mod(inverse_product, prefix);
        inverse_product = mul_mod(inverse_product, denominators[i]);
      }
      std::size_t at = 0;
      for (std::size_t i = begin; i < end; ++i) {
        for (std::size_t j = i + 1; j < end; ++j) {
          lines.push_back(make_line(points[i], points[j], inverses[at++]));
        }
      }
      if (at != group_pairs) throw std::runtime_error("pair replay mismatch");
      pair_count += group_pairs;
      begin = end;
    }
    if (lines.size() != pair_count) throw std::runtime_error("fixed-e1 pair count mismatch");

    std::sort(lines.begin(), lines.end());
    std::uint64_t maximum_pair_multiplicity = 0;
    std::uint64_t maximum_noncarrier_pair_multiplicity = 0;
    std::uint64_t lines_with_at_least_22_points = 0;
    std::uint64_t heavy_opposite_pair_carriers = 0;
    LineKey maximum_line;
    for (std::size_t i = 0; i < lines.size();) {
      std::size_t j = i + 1;
      while (j < lines.size() && lines[j] == lines[i]) ++j;
      const std::uint64_t multiplicity = j - i;
      const bool opposite_carrier = is_opposite_pair_carrier(lines[i]);
      if (multiplicity >= 231) {
        ++lines_with_at_least_22_points;
        if (opposite_carrier) ++heavy_opposite_pair_carriers;
      }
      if (!opposite_carrier) {
        maximum_noncarrier_pair_multiplicity =
            std::max(maximum_noncarrier_pair_multiplicity, multiplicity);
      }
      if (multiplicity > maximum_pair_multiplicity) {
        maximum_pair_multiplicity = multiplicity;
        maximum_line = lines[i];
      }
      i = j;
    }
    const std::uint64_t expected_heavy_lines = punctured ? 8001ULL : 8128ULL;
    if (lines_with_at_least_22_points != expected_heavy_lines ||
        heavy_opposite_pair_carriers != lines_with_at_least_22_points) {
      throw std::runtime_error("heavy-line opposite-pair classification mismatch");
    }
    const auto maximum_points = triangular_root(maximum_pair_multiplicity);
    const auto maximum_noncarrier_points =
        triangular_root(maximum_noncarrier_pair_multiplicity);
    std::vector<Point> maximum_point_list;
    for (const auto& point : points) {
      if (point_on_line(point, maximum_line)) maximum_point_list.push_back(point);
    }
    if (maximum_point_list.size() != maximum_points) {
      throw std::runtime_error("maximum line point replay mismatch");
    }

    std::vector<std::array<int, 4>> witness_quartets;
    const auto replay = enumerate_quartets(
        domain, t4, [&](const Point& point, const std::array<int, 4>& indices) {
          if (point_on_line(point, maximum_line)) witness_quartets.push_back(indices);
        });
    if (replay != quartet_count || witness_quartets.size() != maximum_points) {
      throw std::runtime_error("quartet witness replay mismatch");
    }

    std::cout << "{\n";
    std::cout << "  \"status\": \"PASS\",\n";
    std::cout << "  \"scope\": \"" << (punctured ? "representative_puncture" : "full_D128_uniform_over_all_punctures") << "\",\n";
    std::cout << "  \"field\": " << P << ",\n";
    std::cout << "  \"D128_size\": " << domain.size() << ",\n";
    std::cout << "  \"puncture_theta_value\": " << puncture_value << ",\n";
    std::cout << "  \"canonical_quartets\": " << quartet_count << ",\n";
    std::cout << "  \"pairs_with_common_e1\": " << pair_count << ",\n";
    std::cout << "  \"maximum_points_on_degree_at_most_2_direction_line\": "
              << maximum_points << ",\n";
    std::cout << "  \"maximum_line_pair_multiplicity\": " << maximum_pair_multiplicity << ",\n";
    std::cout << "  \"lines_with_at_least_22_points\": " << lines_with_at_least_22_points << ",\n";
    std::cout << "  \"heavy_opposite_pair_carriers\": " << heavy_opposite_pair_carriers << ",\n";
    std::cout << "  \"maximum_points_off_opposite_pair_carriers\": "
              << maximum_noncarrier_points << ",\n";
    std::cout << "  \"maximum_line_key\": ";
    print_line(maximum_line);
    std::cout << ",\n  \"maximum_line_quartets\": [";
    for (std::size_t i = 0; i < witness_quartets.size(); ++i) {
      if (i) std::cout << ',';
      std::cout << "{\"indices\":[";
      for (int j = 0; j < 4; ++j) {
        if (j) std::cout << ',';
        std::cout << witness_quartets[i][j];
      }
      std::cout << "],\"values\":[";
      for (int j = 0; j < 4; ++j) {
        if (j) std::cout << ',';
        std::cout << domain[witness_quartets[i][j]];
      }
      std::cout << "]}";
    }
    std::cout << "]\n}\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "FAIL: " << error.what() << '\n';
    return 1;
  }
}
