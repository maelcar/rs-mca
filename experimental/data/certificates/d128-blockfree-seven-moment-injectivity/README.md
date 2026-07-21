# D128 block-free seven-subset three-moment injectivity certificate

**Author:** Manuel E. Rey-Álvarez Zafiria

This directory records the finite certificates used by
`experimental/notes/thresholds/d128_blockfree_seven_moment_injectivity.md`.

The fast end-to-end check is

```text
python experimental/scripts/verify_d128_antipodal_lee_collision_exclusion.py
python experimental/scripts/verify_d128_blockfree_seven_moment_injectivity.py
```

The first command requires Python 3 and `sympy`.  It independently rebuilds
the Chebyshev domain, checks the lattice indices and witnesses, verifies the
fixed-radius transcript, derives all twelve Lee profiles, and checks the
complete profile outputs.  The second command combines that result with the
small-side and six-subset classifications.

The small-side and exhaustive six-subset classifiers can be replayed with
optimized Rust:

```text
rustc -O experimental/scripts/verify_d128_small_set_moment_collisions.rs -o verify_small
./verify_small experimental/data/certificates/d128-blockfree-seven-moment-injectivity/small_side_moment_collision_audit.json
rustc -O experimental/scripts/classify_d128_six_set_moment_collisions.rs -o classify_e6
./classify_e6 experimental/data/certificates/d128-blockfree-seven-moment-injectivity/six_set_moment_collision_primary.json
rustc -O experimental/scripts/audit_d128_six_set_moment_collisions.rs -o audit_e6
./audit_e6 experimental/data/certificates/d128-blockfree-seven-moment-injectivity/six_set_moment_collision_independent.json
```

The small-side program enumerates `10668000` four-subsets and `264566400`
five-subsets.  Each six-subset run enumerates `5423611200` subsets and uses
about 43.4 GB of temporary external fingerprint data before exact-key
recovery.  The programs remove their temporary buckets on successful
completion.

Generate the sector certificate and compile the profile programs with

```text
python experimental/scripts/generate_d128_antipodal_sector_certificate.py
g++ -O3 -std=c++20 experimental/scripts/verify_d128_lee_profile_7_0.cpp -o profile70
g++ -O3 -std=c++20 experimental/scripts/verify_d128_lee_profile_generic.cpp -o profile
g++ -O3 -std=c++20 -pthread experimental/scripts/verify_d128_lee_profile_4_6.cpp -o profile46
g++ -O3 -std=c++20 experimental/scripts/verify_d128_even_first_profiles.cpp -o even_first
```

With `D=experimental/data/certificates/d128-blockfree-seven-moment-injectivity`
and `C=$D/antipodal_sector_lattice_certificate.txt`, replay the profiles as
follows:

```text
./profile70 $C $D/profile_7_0_output.json
./profile $C 4 2 1 2 $D/profile_4_2_output.json
./profile $C 5 0 2 0 $D/profile_5_0_output.json
./profile $C 5 2 1 2 $D/profile_5_2_output.json
./profile $C 6 0 3 0 $D/profile_6_0_output.json
./profile $C 4 4 0 4 $D/profile_4_4_output.json
./profile $C 6 2 3 1 $D/profile_6_2_output.json
./profile $C 5 4 0 4 $D/profile_5_4_output.json
./profile $C 3 6 3 1 $D/profile_3_6_output.json
./profile46 $C 12 $D/profile_4_6_output.json
./even_first $C 3 $D/profile_3_8_output.json
./even_first $C 2 $D/profile_2_10_output.json
./even_first $C 4 $D/profile_4_6_even_first_crosscheck.json
```

For the exact fixed-radius proof, install `fplll`, compile with

```text
g++ -O3 -std=c++20 experimental/scripts/verify_d128_odd_fixed_radius.cpp \
    -lfplll -lmpfr -lgmp -o odd_radius
```

and run

```text
./odd_radius $D/odd_sector_lll_replay_basis.txt 15 $D/odd_radius15_output.txt
./odd_radius $D/odd_sector_lll_replay_basis.txt 16 $D/odd_ball16_output.txt collect
```

The recorded radius runs enumerate `1334988488` and `1491620685` nodes,
respectively.

`SHA256SUMS.txt` authenticates every file in this certificate directory and
every verifier source shipped by the PR.
