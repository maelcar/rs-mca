# Typed pair-resource compiler certificates

**Author:** Manuel E. Rey-Álvarez Zafiria

From the repository root run:

```text
python experimental/scripts/verify_typed_pair_resource_partition.py
python experimental/scripts/audit_typed_pair_resource_partition.py
python experimental/scripts/verify_equal_price_supportwise_ratio.py
python experimental/scripts/audit_equal_price_supportwise_ratio.py
python experimental/scripts/verify_two_price_pair_compiler.py
python experimental/scripts/audit_two_price_pair_compiler.py
python experimental/scripts/verify_mixed_mass8_prefix_owner.py
python experimental/scripts/verify_m31_transfer_cap_ledger.py
```

The scripts use Python 3 and the standard library.  The optimizers enumerate
all local occupancy types and global Pareto profiles using exact arithmetic;
the independent two-price check uses a separate scalar dynamic program.

The recorded JSON files are reference outputs.  `SHA256SUMS.txt`
authenticates the note, all eight scripts, and every recorded output.

The codegree values `(21,4)` are checked only as sufficient hypotheses; no
certificate in this directory asserts that they hold globally.
