#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

constexpr std::int64_t P = 2147483647LL;
constexpr std::int64_t X_ONE = 1556867790LL;
constexpr std::uint32_t SKETCH_BITS = 24;
constexpr std::uint32_t SKETCH_SIZE = 1U << SKETCH_BITS;
constexpr std::uint32_t SKETCH_MASK = SKETCH_SIZE - 1U;

std::int64_t add(std::int64_t a, std::int64_t b) {
  const auto z = a + b;
  return z >= P ? z - P : z;
}
std::int64_t sub(std::int64_t a, std::int64_t b) {
  const auto z = a - b;
  return z < 0 ? z + P : z;
}
std::int64_t mul(std::int64_t a, std::int64_t b) {
  return static_cast<std::int64_t>((static_cast<__int128>(a) * b) % P);
}
std::int64_t power(std::int64_t a, std::int64_t e) {
  std::int64_t z = 1;
  while (e) {
    if (e & 1) z = mul(z, a);
    a = mul(a, a);
    e >>= 1;
  }
  return z;
}
std::int64_t cheb(int n, std::int64_t x) {
  if (n == 0) return 1;
  if (n == 1) return x;
  std::int64_t a = 1, b = x;
  for (int i = 1; i < n; ++i) {
    const auto c = sub(2 * mul(x, b) % P, a);
    a = b;
    b = c;
  }
  return b;
}

std::vector<std::int64_t> direct_D128() {
  const auto root = cheb(8, X_ONE);
  const auto step = cheb(2, root);
  std::int64_t previous = root;
  std::int64_t current = root;
  std::vector<std::int64_t> out;
  out.reserve(128);
  out.push_back(root);
  for (int i = 1; i < 128; ++i) {
    const auto next = sub(2 * mul(step, current) % P, previous);
    out.push_back(next);
    previous = current;
    current = next;
  }
  std::sort(out.begin(), out.end());
  if (std::unique(out.begin(), out.end()) != out.end()) {
    throw std::runtime_error("direct D128 recurrence repeated a root");
  }
  for (const auto x : out) {
    if (cheb(128, x) != 0) throw std::runtime_error("bad direct D128 root");
  }
  return out;
}

struct Point {
  std::uint32_t e1, e2, e3, e4;
  bool operator<(const Point& o) const {
    return std::array{e1, e2, e3, e4} < std::array{o.e1, o.e2, o.e3, o.e4};
  }
};

struct Line {
  std::array<std::uint32_t, 6> a{};
  bool operator==(const Line& o) const { return a == o.a; }
};

std::uint64_t mix(std::uint64_t x) {
  x += 0x9e3779b97f4a7c15ULL;
  x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
  x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
  return x ^ (x >> 31);
}

std::uint64_t hash_line(const Line& line, std::uint64_t seed) {
  std::uint64_t h = seed;
  for (const auto x : line.a) h = mix(h ^ x);
  return h;
}

struct LineHash {
  std::size_t operator()(const Line& line) const {
    return static_cast<std::size_t>(hash_line(line, 0x243f6a8885a308d3ULL));
  }
};

template <class Callback>
std::uint64_t quartets(const std::vector<std::int64_t>& d, Callback callback) {
  std::uint64_t count = 0;
  for (int l = 127; l >= 3; --l) {
    const auto x4 = d[l];
    for (int k = l - 1; k >= 2; --k) {
      const auto x3 = d[k];
      for (int j = k - 1; j >= 1; --j) {
        const auto x2 = d[j];
        for (int i = j - 1; i >= 0; --i) {
          if (cheb(4, d[i]) == cheb(4, x2) &&
              cheb(4, d[i]) == cheb(4, x3) &&
              cheb(4, d[i]) == cheb(4, x4)) {
            continue;
          }
          const auto x1 = d[i];
          const auto s12 = add(x1, x2);
          const auto p12 = mul(x1, x2);
          const auto s123 = add(s12, x3);
          const auto e2_123 = add(p12, mul(x3, s12));
          const auto e3_123 = mul(p12, x3);
          callback(Point{
              static_cast<std::uint32_t>(add(s123, x4)),
              static_cast<std::uint32_t>(add(e2_123, mul(x4, s123))),
              static_cast<std::uint32_t>(add(e3_123, mul(x4, e2_123))),
              static_cast<std::uint32_t>(mul(e3_123, x4))});
          ++count;
        }
      }
    }
  }
  return count;
}

Line normalized_line(const Point& x, const Point& y, std::int64_t inv) {
  const auto dx = sub(y.e2, x.e2);
  const auto dy = sub(y.e3, x.e3);
  const auto dz = sub(y.e4, x.e4);
  Line line;
  if (dx != 0) {
    const auto a = mul(dy, inv);
    const auto b = mul(dz, inv);
    line.a = {0, x.e1, static_cast<std::uint32_t>(a), static_cast<std::uint32_t>(b),
              static_cast<std::uint32_t>(sub(x.e3, mul(a, x.e2))),
              static_cast<std::uint32_t>(sub(x.e4, mul(b, x.e2)))};
  } else {
    if (dy == 0) throw std::runtime_error("constant-direction collision");
    const auto b = mul(dz, inv);
    line.a = {1, x.e1, static_cast<std::uint32_t>(b), x.e2,
              static_cast<std::uint32_t>(sub(x.e4, mul(b, x.e3))), 0};
  }
  return line;
}

template <class Callback>
std::uint64_t pairs_by_e1(const std::vector<Point>& points, Callback callback) {
  std::uint64_t total = 0;
  for (std::size_t first = 0; first < points.size();) {
    std::size_t last = first + 1;
    while (last < points.size() && points[last].e1 == points[first].e1) ++last;
    std::vector<std::int64_t> den;
    den.reserve((last - first) * (last - first - 1) / 2);
    for (std::size_t i = first; i < last; ++i) {
      for (std::size_t j = i + 1; j < last; ++j) {
        const auto dx = sub(points[j].e2, points[i].e2);
        const auto dy = sub(points[j].e3, points[i].e3);
        if (dx == 0 && dy == 0) throw std::runtime_error("same e1,e2,e3");
        den.push_back(dx != 0 ? dx : dy);
      }
    }
    std::vector<std::int64_t> inv(den.size());
    std::int64_t product = 1;
    for (std::size_t i = 0; i < den.size(); ++i) {
      inv[i] = product;
      product = mul(product, den[i]);
    }
    auto tail = power(product, P - 2);
    for (std::size_t i = den.size(); i-- > 0;) {
      const auto prefix = inv[i];
      inv[i] = mul(tail, prefix);
      tail = mul(tail, den[i]);
    }
    std::size_t at = 0;
    for (std::size_t i = first; i < last; ++i) {
      for (std::size_t j = i + 1; j < last; ++j) {
        callback(normalized_line(points[i], points[j], inv[at++]));
      }
    }
    total += den.size();
    first = last;
  }
  return total;
}

bool opposite_carrier(const Line& line) {
  if (line.a[0] != 0 || line.a[2] != line.a[1]) return false;
  const auto s = line.a[1];
  const auto p = line.a[3];
  return line.a[4] == sub(0, mul(s, p)) &&
         line.a[5] == sub(0, mul(p, p));
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const std::string output = argc >= 2 ? argv[1] : "I_D128_line_audit_output.json";
    const auto domain = direct_D128();
    std::vector<Point> points;
    points.reserve(10667968);
    const auto quartet_count = quartets(domain, [&](const Point& p) { points.push_back(p); });
    if (quartet_count != 10667968ULL) throw std::runtime_error("quartet total mismatch");
    std::sort(points.begin(), points.end());

    std::vector<std::uint8_t> sketch1(SKETCH_SIZE, 0), sketch2(SKETCH_SIZE, 0);
    const auto pair_count = pairs_by_e1(points, [&](const Line& line) {
      auto& a = sketch1[hash_line(line, 0x13198a2e03707344ULL) & SKETCH_MASK];
      auto& b = sketch2[hash_line(line, 0xa4093822299f31d0ULL) & SKETCH_MASK];
      if (a != 255) ++a;
      if (b != 255) ++b;
    });
    if (pair_count != 17244778ULL) throw std::runtime_error("pair total mismatch");

    std::unordered_map<Line, std::uint32_t, LineHash> candidates;
    candidates.reserve(200000);
    const auto replay_pairs = pairs_by_e1(points, [&](const Line& line) {
      if (sketch1[hash_line(line, 0x13198a2e03707344ULL) & SKETCH_MASK] >= 3 &&
          sketch2[hash_line(line, 0xa4093822299f31d0ULL) & SKETCH_MASK] >= 3) {
        ++candidates[line];
      }
    });
    if (replay_pairs != pair_count) throw std::runtime_error("pair replay mismatch");

    std::uint64_t heavy = 0, heavy_carrier = 0, noncarrier_at_least_three = 0;
    std::uint32_t maximum = 0;
    for (const auto& [line, count] : candidates) {
      maximum = std::max(maximum, count);
      if (count >= 231) {
        ++heavy;
        if (opposite_carrier(line)) ++heavy_carrier;
      }
      if (count >= 3 && !opposite_carrier(line)) ++noncarrier_at_least_three;
    }
    if (heavy != 8128 || heavy_carrier != heavy ||
        noncarrier_at_least_three != 0 || maximum != 1891) {
      throw std::runtime_error("line classification mismatch");
    }

    std::ofstream out(output, std::ios::binary);
    out << "{\n"
        << "  \"status\": \"PASS_INDEPENDENT_D128_QUARTIC_LINE_AUDIT\",\n"
        << "  \"domain_construction\": \"direct_D128_recurrence\",\n"
        << "  \"canonical_quartets\": " << quartet_count << ",\n"
        << "  \"pairs_with_common_e1\": " << pair_count << ",\n"
        << "  \"sketch_bits_per_filter\": " << SKETCH_BITS << ",\n"
        << "  \"exact_candidate_lines\": " << candidates.size() << ",\n"
        << "  \"maximum_pair_multiplicity\": " << maximum << ",\n"
        << "  \"heavy_lines_at_least_22_points\": " << heavy << ",\n"
        << "  \"heavy_opposite_pair_carriers\": " << heavy_carrier << ",\n"
        << "  \"noncarrier_lines_with_at_least_3_points\": 0,\n"
        << "  \"maximum_noncarrier_points\": 2,\n"
        << "  \"no_false_negative_argument\": \"A line with at least three pairs increments one bucket in each saturating sketch at least three times; the second full pass counts every key passing both filters exactly.\"\n"
        << "}\n";
    out.close();
    if (!out) throw std::runtime_error("output write failed");
    std::cout << "PASS_INDEPENDENT_D128_QUARTIC_LINE_AUDIT\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "FAIL: " << error.what() << '\n';
    return 1;
  }
}
