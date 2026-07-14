#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <set>
#include <tuple>
#include <vector>

using i64 = std::int64_t;

static constexpr int ELL = 19;
static constexpr std::array<int, 44> PRIMES = {
    191, 229, 419, 457, 571, 647, 1103, 1217, 1559, 2243, 2357,
    2927, 3041, 3079, 4409, 4637, 7639, 7867, 9767, 10223, 12959,
    14821, 23561, 23827, 26297, 27551, 28843, 32909, 37013, 40471,
    43853, 47387, 53353, 78167, 95419, 137941, 228989, 352489,
    362027, 510683, 797051, 1340071, 3833707, 8494331};

i64 mod_pow(i64 base, i64 exponent, int prime) {
    i64 output = 1;
    while (exponent) {
        if (exponent & 1) output = output * base % prime;
        base = base * base % prime;
        exponent >>= 1;
    }
    return output;
}

std::vector<int> prime_factors(int value) {
    std::vector<int> output;
    for (int divisor = 2; i64(divisor) * divisor <= value; ++divisor) {
        if (value % divisor == 0) {
            output.push_back(divisor);
            while (value % divisor == 0) value /= divisor;
        }
    }
    if (value > 1) output.push_back(value);
    return output;
}

int primitive_root(int prime) {
    const auto factors = prime_factors(prime - 1);
    for (int candidate = 2; candidate < prime; ++candidate) {
        bool valid = true;
        for (int factor : factors) {
            if (mod_pow(candidate, (prime - 1) / factor, prime) == 1) {
                valid = false;
                break;
            }
        }
        if (valid) return candidate;
    }
    return -1;
}

int determinant3(const std::array<std::array<int, 3>, 3>& a, int p) {
    i64 value =
        i64(a[0][0]) * (i64(a[1][1]) * a[2][2] - i64(a[1][2]) * a[2][1])
        - i64(a[0][1]) * (i64(a[1][0]) * a[2][2] - i64(a[1][2]) * a[2][0])
        + i64(a[0][2]) * (i64(a[1][0]) * a[2][1] - i64(a[1][1]) * a[2][0]);
    value %= p;
    if (value < 0) value += p;
    return int(value);
}

int determinant4(const std::array<std::array<int, 4>, 4>& matrix, int p) {
    i64 output = 0;
    for (int omitted = 0; omitted < 4; ++omitted) {
        std::array<std::array<int, 3>, 3> minor;
        for (int row = 1; row < 4; ++row) {
            int target = 0;
            for (int col = 0; col < 4; ++col) {
                if (col != omitted) minor[row - 1][target++] = matrix[row][col];
            }
        }
        const i64 term = i64(matrix[0][omitted]) * determinant3(minor, p);
        output += (omitted & 1) ? -term : term;
    }
    output %= p;
    if (output < 0) output += p;
    return int(output);
}

std::vector<std::array<int, 4>> root_translation_representatives() {
    std::set<std::array<int, 4>> representatives;
    for (int a = 0; a < ELL; ++a)
        for (int b = a + 1; b < ELL; ++b)
            for (int c = b + 1; c < ELL; ++c)
                for (int d = c + 1; d < ELL; ++d) {
                    std::array<int, 4> best = {ELL, ELL, ELL, ELL};
                    const std::array<int, 4> support = {a, b, c, d};
                    for (int shift = 0; shift < ELL; ++shift) {
                        std::array<int, 4> candidate;
                        for (int index = 0; index < 4; ++index)
                            candidate[index] = (support[index] + shift) % ELL;
                        std::sort(candidate.begin(), candidate.end());
                        best = std::min(best, candidate);
                    }
                    representatives.insert(best);
                }
    return {representatives.begin(), representatives.end()};
}

struct State {
    std::array<int, 3> support;
    std::array<int, 3> gamma;
    bool operator<(const State& other) const {
        return std::tie(support, gamma) < std::tie(other.support, other.gamma);
    }
};

struct SpectrumResult {
    std::array<int, 12> sums;
    int maximum_fiber;
};

SpectrumResult top_sums(
    const State& state, int prime, int generator, int quotient_size,
    const std::array<int, ELL>& zeta_power) {
    std::vector<int> spectrum;
    spectrum.reserve(quotient_size);
    std::array<int, 3> coefficients = state.gamma;
    std::array<int, 3> steps;
    for (int index = 0; index < 3; ++index)
        steps[index] = int(mod_pow(generator, state.support[index], prime));

    for (int label = 0; label < quotient_size; ++label) {
        std::array<int, ELL> values;
        for (int root = 0; root < ELL; ++root) {
            i64 value = 0;
            for (int index = 0; index < 3; ++index) {
                value += i64(coefficients[index])
                    * zeta_power[(root * state.support[index]) % ELL];
            }
            values[root] = int(value % prime);
        }
        for (std::size_t index = 1; index < values.size(); ++index) {
            const int value = values[index];
            std::size_t position = index;
            while (position > 0 && values[position - 1] > value) {
                values[position] = values[position - 1];
                --position;
            }
            values[position] = value;
        }
        int maximum = 1;
        int run = 1;
        for (int index = 1; index < ELL; ++index) {
            if (values[index] == values[index - 1]) {
                maximum = std::max(maximum, ++run);
            } else {
                run = 1;
            }
        }
        spectrum.push_back(maximum);
        for (int index = 0; index < 3; ++index)
            coefficients[index] = int(i64(coefficients[index]) * steps[index] % prime);
    }
    std::sort(spectrum.begin(), spectrum.end(), std::greater<int>());
    std::array<int, 12> output{};
    int running = 0;
    for (int h = 1; h <= 17; ++h) {
        if (h <= int(spectrum.size())) running += spectrum[h - 1];
        if (h >= 6) output[h - 6] = running;
    }
    return {output, spectrum.empty() ? 0 : spectrum.front()};
}

int main() {
    const auto roots = root_translation_representatives();
    if (roots.size() != 204) return 2;
    std::cout << "ELL19_THREE_SECTOR_SPECTRUM_V1\n";
    for (int prime : PRIMES) {
        const int generator = primitive_root(prime);
        const int quotient_size = (prime - 1) / ELL;
        const int zeta = int(mod_pow(generator, quotient_size, prime));
        std::array<int, ELL> zeta_power;
        zeta_power[0] = 1;
        for (int index = 1; index < ELL; ++index)
            zeta_power[index] = int(i64(zeta_power[index - 1]) * zeta % prime);

        int singular_rows = 0;
        std::set<State> states;
        for (int a = 1; a < ELL; ++a)
            for (int b = a + 1; b < ELL; ++b)
                for (int c = b + 1; c < ELL; ++c) {
                    const std::array<int, 4> exponents = {0, a, b, c};
                    for (const auto& root_set : roots) {
                        std::array<std::array<int, 4>, 4> matrix;
                        for (int row = 0; row < 4; ++row)
                            for (int col = 0; col < 4; ++col)
                                matrix[row][col] = zeta_power[
                                    (root_set[row] * exponents[col]) % ELL];
                        if (determinant4(matrix, prime) != 0) continue;
                        ++singular_rows;
                        std::array<int, 4> kernel;
                        bool rank_three = false;
                        for (int omitted_row = 0; omitted_row < 4 && !rank_three;
                             ++omitted_row) {
                            std::array<std::array<int, 4>, 3> three_rows;
                            int target_row = 0;
                            for (int row = 0; row < 4; ++row) {
                                if (row != omitted_row)
                                    three_rows[target_row++] = matrix[row];
                            }
                            for (int omitted = 0; omitted < 4; ++omitted) {
                                std::array<std::array<int, 3>, 3> minor;
                                for (int row = 0; row < 3; ++row) {
                                    int target = 0;
                                    for (int col = 0; col < 4; ++col) {
                                        if (col != omitted)
                                            minor[row][target++] = three_rows[row][col];
                                    }
                                }
                                int value = determinant3(minor, prime);
                                if (omitted & 1) value = value ? prime - value : 0;
                                kernel[omitted] = value;
                            }
                            rank_three = std::any_of(
                                kernel.begin(), kernel.end(), [](int value) {
                                    return value != 0;
                                });
                        }
                        if (!rank_three) return 3;
                        if (!kernel[1] || !kernel[2] || !kernel[3]) continue;
                        const int inverse = int(mod_pow(kernel[1], prime - 2, prime));
                        states.insert(State{{a, b, c}, {
                            1,
                            int(i64(kernel[2]) * inverse % prime),
                            int(i64(kernel[3]) * inverse % prime)}});
                    }
                }

        std::array<int, 12> maxima{};
        int maximum_fiber = 3;
        for (const auto& state : states) {
            const auto result = top_sums(
                state, prime, generator, quotient_size, zeta_power);
            for (int index = 0; index < 12; ++index)
                maxima[index] = std::max(maxima[index], result.sums[index]);
            maximum_fiber = std::max(maximum_fiber, result.maximum_fiber);
        }
        // Full-support coefficient vectors without a four-fiber have cap 3.
        for (int h = 6; h <= 17; ++h)
            maxima[h - 6] = std::max(maxima[h - 6], 3 * std::min(h, quotient_size));

        std::cout << prime << ' ' << quotient_size << ' ' << singular_rows
                  << ' ' << states.size() << ' ' << maximum_fiber;
        for (int value : maxima) std::cout << ' ' << value;
        std::cout << '\n';
    }
    std::cout << "PASS_ELL19_THREE_SECTOR_SPECTRUM\n";
    return 0;
}
