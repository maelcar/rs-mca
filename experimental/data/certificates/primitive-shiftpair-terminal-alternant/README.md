# Primitive Shift-Pair Terminal Alternant Certificate

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** PROVED / COUNTEREXAMPLE / OPEN ACTIVE BOUND

Run from the repository root:

```text
python experimental/scripts/verify_primitive_shiftpair_terminal_alternant.py
```

The verifier uses only the Python standard library. It reconstructs the
complete `(p,M,e)=(191,64,4)` terminal row, checks every nontrivial
fixed-bottom pair, verifies the shared-even alternant equations, and checks
the explicit rank-five `6 x 6` counterexample to ambient full spark.

It writes
`primitive_shiftpair_terminal_alternant.json` in this directory and ends
with `PASS_WITH_TERMINAL_VANISHING_AND_ALTERNANT_REDUCTION`.

The certificate is finite evidence for the uniform algebraic reductions. It
does not certify the active common-root or fixed-bottom capacity targets.
