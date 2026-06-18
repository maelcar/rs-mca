# Cycle 15 Forced-Ra Slope Scan Certificate

Status: EXPERIMENTAL / AUDIT.

Script:

- `experimental/2026-06-18-fable-loop/local_checks/20260618_cycle15_forced_ra_slope_scan.py`

Command:

```bash
python3 experimental/2026-06-18-fable-loop/local_checks/20260618_cycle15_forced_ra_slope_scan.py
```

Mathematical object checked:

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `q_chal` unused.
- `D=F_p`, `t=sigma=2`, `j=n-a=3`.
- `Ra` resonance condition forced by requiring all ten quadratic coefficients
  of `Delta(tau_1,tau_2,tau_3)` to lie on one `B`-line in `F`.

Output:

```text
p=7 seed=0 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=3 C2=3 max_slope_fiber=1
p=7 seed=1 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=5 C2=5 max_slope_fiber=1
p=7 seed=2 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=2 C2=2 max_slope_fiber=1
p=7 seed=3 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=6 C2=6 max_slope_fiber=1
p=7 seed=4 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=9 C2=4 max_slope_fiber=5
p=7 seed=5 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=5 C2=5 max_slope_fiber=1
p=7 seed=6 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=8 C2=4 max_slope_fiber=5
p=7 seed=7 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=3 C2=2 max_slope_fiber=2
p=7 seed=8 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=8 C2=4 max_slope_fiber=5
p=7 seed=9 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=8 C2=4 max_slope_fiber=5
p=7 seed=10 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=9 C2=5 max_slope_fiber=5
p=7 seed=11 q_gen=7 q_line=49 checked=64 max_kernel_dim=7 best_direction=(1, 0) kernel_dim=7 coeff_rank=1 off_R0=True split_landings=3 C2=3 max_slope_fiber=1
forced_ra_slope_scan: BEST p=7 q_gen=7 q_line=49 seed=3 C2=6 split_landings=6 off_R0=True direction=(1, 0) kernel_dim=7
```

Interpretation:

- The forced resonance condition was achieved in the smoke cases:
  `coeff_rank=1`.
- The examples stayed off `R0`.
- No large slope image was found in this bounded `p=7` sample:
  `C2<=6`.

This is not a proof of the `O(p)` slope bound. It is not a counterpacket to the
rank/determinant wall. It supports the next scanner/proof target:

```text
W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER-RANK-DETERMINANT.
```
