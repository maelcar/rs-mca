# Reproducibility notes for `RS_MCA_Paving_v9.2`

## Environment

- Python 3.12.13 (the scripts use only the standard library)
- pdfTeX 3.141592653-2.6-1.40.25, TeX Live 2023
- `amsart` on A4 paper with one-inch margins

## Commands

Run the unconditional and conditional arithmetic audits separately:

```sh
python3 verify_paving_mca_v9_2.py
python3 verify_retained_bchks_v9_2.py
```

The expected outputs are:

```text
v9.2 unconditional arithmetic: all checks passed
v9.2 conditional retained-lift arithmetic: all checks passed
NOTE: the Parameter-retained factor lift remains an assumption.
```

Compile the paper with three passes:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error RS_MCA_Paving_v9.2.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error RS_MCA_Paving_v9.2.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error RS_MCA_Paving_v9.2.tex
```

The release PDF has 55 A4 pages. The final log has no undefined references,
layout warnings, or overfull/underfull boxes.

## SHA-256

```text
8e89be94dd6291dc5563897e72ae34b49880512cd37f72287b4288ff030cbbc0  RS_MCA_Paving_v9.2.tex
2d9eaa739e0c95dbb485496453cff93d44a2ef6df0b2d57405c879ba1bbdc7d4  RS_MCA_Paving_v9.2.pdf
10af5ac3ba096ab770440d7822c526dd292665965ed151f237cd128976923c7b  verify_paving_mca_v9_2.py
1e40dee273964935aaf3cc1efef2e75415979b2802974108587c3fc99bad119c  verify_retained_bchks_v9_2.py
1f77eac75f842c0b11380de3fe4dc261189729c0c54450048d116ed90f9ea279  AI_USE_v9.2.md
```

The unconditional script checks the Proth and Lucas--Lehmer certificates,
field budgets, exact all-test-size circuit minima, Jo endpoint field
conditions, improved adjacent thresholds, exact shortened Johnson margins,
the three length-512 shortening comparisons, and the circle rows. The
conditional script verifies only arithmetic consequences of the explicitly
stated factor-lifting assumption; it does not discharge that assumption.
