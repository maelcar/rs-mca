# L1 Multisector Onset Certificates

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** PROVED / COUNTEREXAMPLE

Run from the repository root:

```text
python experimental/scripts/verify_l1_multisector_common_root_deficit.py
python experimental/scripts/verify_l1_ell7_three_sector_counterexample.py
python experimental/scripts/verify_l1_ell7_four_sector_counterexample.py
python experimental/scripts/verify_l1_ell11_three_sector_onset.py
python experimental/scripts/verify_l1_ell13_three_sector_onset.py
python experimental/scripts/verify_l1_ell17_three_sector_onset.py
python experimental/scripts/verify_l1_ell19_three_sector_onset.py
```

The first five commands use only the Python standard library. The `ell=17`
and `ell=19` commands additionally require a C++20 compiler named `g++` on
`PATH`, or a compiler path supplied in the `CXX` environment variable. They
compile the corresponding `verify_l1_ell*_three_sector_spectrum.cpp` source
in a temporary directory.

Each command regenerates one JSON file in this directory and ends with a
`PASS_WITH_...` verdict. The JSON files contain the exact resultant tables,
exceptional-state rows, vacancy inequalities, witness coefficients, and
pointwise reconstruction checks.

The certificates are deterministic and use exact integer or finite-field
arithmetic. No random sampling or floating-point comparison is used.
