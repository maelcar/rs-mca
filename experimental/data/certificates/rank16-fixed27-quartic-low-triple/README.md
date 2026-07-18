# Fixed-27 quartic low-triple certificate

This directory contains the exact independent-audit sources consumed by the
finite local theorem in
`experimental/notes/l2/rank16_fixed27_quartic_low_triple_band.md`.

The three Python programs use only the standard library. Their ordinary and
`python3 -O` outputs are byte-identical to the adjacent expected-output files.

The C++17 program is the full split-quartic Pasch census over the deployed
field. It performs no file, network, or subprocess access. On a machine with a
local C++ compiler, replay it through

```bash
python3 experimental/scripts/verify_rank16_fixed27_quartic_low_triple.py --full-census
```

The compiled executable is temporary and is not shipped. The expected census
transcript distinguishes `11,328` unique Pasch configurations from their
`67,968` oriented completion paths.

`SHA256SUMS.txt` pins every source and expected-output artifact in this
directory except itself.
