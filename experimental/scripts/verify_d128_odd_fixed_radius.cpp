#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

#include <fplll/fplll.h>

namespace {

class FixedRadiusExactEvaluator : public fplll::ExactErrorBoundedEvaluator {
 public:
  FixedRadiusExactEvaluator(
      int dimension,
      fplll::MatGSOInterface<fplll::Z_NR<mpz_t>, fplll::FP_NR<mpfr_t>>& gso,
      fplll::ZZ_mat<mpz_t>& basis,
      long radius_squared,
      bool stop_on_hit)
      : fplll::ExactErrorBoundedEvaluator(
            dimension, gso, fplll::EVALMODE_SV, 1,
            fplll::EVALSTRATEGY_BEST_N_SOLUTIONS, false),
        gso_(gso),
        basis_(basis),
        stop_on_hit_(stop_on_hit) {
    radius_ = radius_squared;
    first_norm_ = 0;
  }

  void eval_sol(const std::vector<fplll::FP_NR<mpfr_t>>& coordinates,
                const fplll::enumf& /*partial_distance*/,
                fplll::enumf& max_distance) override {
    ++leaf_callbacks;
    std::vector<fplll::Z_NR<mpz_t>> integer_coordinates(coordinates.size());
    for (std::size_t i = 0; i < coordinates.size(); ++i) {
      integer_coordinates[i].set_f(coordinates[i]);
    }
    fplll::Z_NR<mpz_t> exact_norm;
    gso_.sqnorm_coordinates(exact_norm, integer_coordinates);
    if (exact_norm == 0) {
      ++zero_callbacks;
      return;
    }
    if (exact_norm > radius_) {
      ++outside_radius_callbacks;
      return;
    }

    ++nonzero_hits;
    std::vector<long> integer_enumeration_coordinates;
    integer_enumeration_coordinates.reserve(coordinates.size());
    for (const auto& coordinate : coordinates) {
      integer_enumeration_coordinates.push_back(coordinate.get_si());
    }
    std::vector<long long> lattice_vector(coordinates.size(), 0);
    for (std::size_t row = 0; row < coordinates.size(); ++row) {
      const long coefficient = integer_enumeration_coordinates[row];
      for (std::size_t column = 0; column < coordinates.size(); ++column) {
        lattice_vector[column] += coefficient * basis_[row][column].get_si();
      }
    }

    long long reconstructed_norm = 0;
    long long lee_weight = 0;
    int twos = 0;
    int ones = 0;
    for (const long long coordinate : lattice_vector) {
      reconstructed_norm += coordinate * coordinate;
      lee_weight += std::abs(coordinate);
      if (std::abs(coordinate) == 2) ++twos;
      if (std::abs(coordinate) == 1) ++ones;
    }
    if (reconstructed_norm != exact_norm.get_si()) {
      throw std::runtime_error("exact norm and reconstructed norm disagree");
    }
    ++profile_histogram[std::make_tuple(reconstructed_norm, twos, ones)];
    minimum_lee_weight = std::min(minimum_lee_weight, lee_weight);

    if (first_coordinates.empty()) {
      first_norm_ = exact_norm;
      first_coordinates = std::move(integer_enumeration_coordinates);
      first_lattice_vector = std::move(lattice_vector);
    }

    if (stop_on_hit_) {
      max_distance = 0.0;
    }
  }

  const fplll::Z_NR<mpz_t>& first_norm() const { return first_norm_; }

  std::size_t leaf_callbacks = 0;
  std::size_t zero_callbacks = 0;
  std::size_t outside_radius_callbacks = 0;
  std::size_t nonzero_hits = 0;
  long long minimum_lee_weight = std::numeric_limits<long long>::max();
  std::map<std::tuple<long long, int, int>, std::size_t> profile_histogram;
  std::vector<long> first_coordinates;
  std::vector<long long> first_lattice_vector;

 private:
  fplll::Z_NR<mpz_t> radius_;
  fplll::Z_NR<mpz_t> first_norm_;
  fplll::MatGSOInterface<fplll::Z_NR<mpz_t>, fplll::FP_NR<mpfr_t>>& gso_;
  fplll::ZZ_mat<mpz_t>& basis_;
  bool stop_on_hit_;
};

}  // namespace

int main(int argc, char** argv) {
  if (argc != 4 && argc != 5) {
    std::cerr << "usage: " << argv[0]
              << " BASIS RADIUS_SQUARED OUTPUT [collect]\n";
    return 2;
  }

  fplll::ZZ_mat<mpz_t> basis;
  std::ifstream input(argv[1]);
  input >> basis;
  if (!input || basis.get_rows() != 64 || basis.get_cols() != 64) {
    throw std::runtime_error("could not read a 64 by 64 basis");
  }

  const int threads = fplll::set_threads(-1);
  const int lll_status = fplll::lll_reduction(basis);
  if (lll_status != fplll::RED_SUCCESS) {
    throw std::runtime_error("LLL preprocessing failed: " +
                             std::string(fplll::get_red_status_str(lll_status)));
  }

  constexpr int dimension = 64;
  const long radius_squared = std::stol(argv[2]);
  if (radius_squared < 1 || radius_squared > 16) {
    throw std::runtime_error("RADIUS_SQUARED must be between 1 and 16");
  }
  const bool collect_all = argc == 5 && std::string(argv[4]) == "collect";
  if (argc == 5 && !collect_all) {
    throw std::runtime_error("the optional mode must be collect");
  }
  double rho = 0.0;
  const int minimum_precision =
      fplll::gso_min_prec(rho, dimension, fplll::LLL_DEF_DELTA, fplll::LLL_DEF_ETA);
  const int precision = std::max(53, minimum_precision + 10);
  const int old_precision = fplll::FP_NR<mpfr_t>::set_prec(precision);

  fplll::ZZ_mat<mpz_t> empty;
  fplll::MatGSO<fplll::Z_NR<mpz_t>, fplll::FP_NR<mpfr_t>> gso(
      basis, empty, empty, fplll::GSO_INT_GRAM);
  if (!gso.update_gso()) throw std::runtime_error("GSO update failed");

  FixedRadiusExactEvaluator evaluator(dimension, gso, basis, radius_squared,
                                      !collect_all);
  fplll::Z_NR<mpz_t> integer_radius;
  integer_radius = radius_squared;
  evaluator.int_max_dist = integer_radius;
  evaluator.init_delta_def(precision, rho, true);

  fplll::FP_NR<mpfr_t> maximum_distance;
  maximum_distance.set_z(integer_radius, GMP_RNDU);
  fplll::FP_NR<mpfr_t> maximum_error;
  if (!evaluator.get_max_error_aux(maximum_distance, true, maximum_error)) {
    throw std::runtime_error("could not certify the initial enumeration bound");
  }
  maximum_distance.add(maximum_distance, maximum_error, GMP_RNDU);

  const auto started = std::chrono::steady_clock::now();
  fplll::Enumeration<fplll::Z_NR<mpz_t>, fplll::FP_NR<mpfr_t>> enumerator(gso,
                                                                            evaluator);
  enumerator.enumerate(0, dimension, maximum_distance, 0);
  const double seconds = std::chrono::duration<double>(
                             std::chrono::steady_clock::now() - started)
                             .count();
  fplll::FP_NR<mpfr_t>::set_prec(old_precision);

  std::ofstream output(argv[3]);
  if (!output) throw std::runtime_error("could not open output");
  output << "D128_FPLLL_PROVED_ODD_FIXED_RADIUS_V3\n";
  output << "status RED_SUCCESS\n";
  output << "evaluator FixedRadiusExactEvaluator\n";
  output << "radius_squared " << radius_squared << "\n";
  output << "enumeration_mode " << (collect_all ? "collect_all" : "stop_on_hit")
         << "\n";
  output << "nonzero_hits " << evaluator.nonzero_hits << "\n";
  output << "leaf_callbacks " << evaluator.leaf_callbacks << "\n";
  output << "zero_callbacks " << evaluator.zero_callbacks << "\n";
  output << "outside_radius_callbacks " << evaluator.outside_radius_callbacks << "\n";
  output << "enumeration_nodes " << enumerator.get_nodes() << "\n";
  output << "threads " << threads << "\n";
  output << "mpfr_precision_bits " << precision << "\n";
  output << "wall_seconds " << seconds << "\n";
  if (evaluator.nonzero_hits != 0) {
    output << "minimum_lee_weight " << evaluator.minimum_lee_weight << "\n";
  }
  for (const auto& [profile, count] : evaluator.profile_histogram) {
    const auto [norm, twos, ones] = profile;
    output << "profile norm=" << norm << " twos=" << twos << " ones=" << ones
           << " count=" << count << "\n";
  }

  if (evaluator.nonzero_hits != 0) {
    output << "first_exact_norm " << evaluator.first_norm() << "\n";
    output << "first_enumeration_coordinates";
    for (const long coordinate : evaluator.first_coordinates) {
      output << ' ' << coordinate;
    }
    output << "\n";
    output << "first_lattice_vector";
    for (const long long coordinate : evaluator.first_lattice_vector) {
      output << ' ' << coordinate;
    }
    output << "\n";
    if (!collect_all) {
      std::cerr << "FAIL_D128_NONZERO_ODD_VECTOR_WITHIN_FIXED_RADIUS"
                << " exact_norm=" << evaluator.first_norm() << '\n';
      return 1;
    }
  }

  std::cout << (collect_all ? "PASS_D128_FPLLL_PROVED_COMPLETE_ODD_BALL"
                            : "PASS_D128_FPLLL_PROVED_NO_ODD_VECTOR_WITHIN_FIXED_RADIUS")
            << " nodes=" << enumerator.get_nodes() << " threads=" << threads
            << " precision=" << precision << " seconds=" << seconds << '\n';
}
