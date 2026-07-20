# Last-predeep cube-fiber profile obstruction certificate

This certificate binds the independently audited R34 Role 06 obstruction to
the current source interfaces and a deterministic standard-library replay.

Run:

```bash
python3 experimental/scripts/verify_last_predeep_cube_fiber_profile_obstruction.py --check
python3 -O experimental/scripts/verify_last_predeep_cube_fiber_profile_obstruction.py --check
python3 experimental/scripts/verify_last_predeep_cube_fiber_profile_obstruction.py --tamper-selftest
```

The normal and optimized check outputs must match
`verify_last_predeep_cube_fiber_profile_obstruction.expected.txt`. This is a
zero-payment necessary route cut, not a complete replacement exclusion. The
official score remains `0/2`.
