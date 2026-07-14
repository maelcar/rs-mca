# Exact Two-Sector Classification Certificates

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** PROVED / COUNTEREXAMPLE

Run all commands from the repository root with Python 3.

```text
python experimental/scripts/verify_l1_two_sector_width_vacancy.py
python experimental/scripts/verify_l1_ell7_two_sector_vacancy.py
python experimental/scripts/verify_l1_ell11_13_two_sector_vacancy.py
python experimental/scripts/verify_l1_ell17_19_two_sector_frontier.py
python experimental/scripts/verify_l1_exceptional_two_sector_d0.py
python experimental/scripts/verify_l1_ell17_two_sector_propagation.py
python experimental/scripts/verify_l1_ell19_two_sector_dpositive.py
```

The scripts use only the Python standard library. Each one recomputes and
overwrites its corresponding JSON certificate in this directory.

| Certificate | Main check |
|---|---|
| `two_sector_width_vacancy.json` | cyclic-width theorem and finite-field root checks |
| `ell7_two_sector_vacancy.json` | complete `ell=7` resultant obstruction |
| `ell11_13_two_sector_vacancy.json` | complete `ell=11,13` resultant and availability sieve |
| `ell17_19_two_sector_exceptional_frontier.json` | resultant frontier and exact rank caps |
| `exceptional_two_sector_d0.json` | `F_2699` vacancy and explicit `F_1361` `D=0` witnesses |
| `ell17_two_sector_propagation.json` | all fifteen `F_1361` exceptional cells |
| `ell19_two_sector_dpositive_vacancy.json` | common-root dichotomy for every `F_2699` `D>0` cell |

Every verifier terminates with a `PASS_WITH_...` verdict or raises an
exception on the first failed invariant.
