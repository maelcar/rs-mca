# Audit: first-wall MDS-extension Lean ownership map

**STATUS:** `AUDIT`

**Audited references:**

- PR #853 head `0c8d2c3c`, based on `7f278167` and manually integrated by
  `06b2a6fb`;
- current audited upstream snapshot `c4856fa6`; and
- open consumer PR #882 head `af213091`.

## Verdict

PR #853's mathematical packet is clean. Its interpolation partition,
retained/deleted charge identity, MDS-extension equivalence, local slope-map
criterion, weighted graph normalization, finite arc exhaustions, and
one-coordinate perturbation ledger agree with the note, deterministic
certificate, and independent replay. The Lean module also compiles and is
honest about being only an abstract finite-counting companion.

The integrated package maps were not accurate. Manual integration `06b2a6fb`
added two descriptions saying that the Lean module formalizes the MDS
extension inverse, retained/deleted collision slack, and graph-arc
normalization. None of those semantic statements occurs in the executable
Lean declarations. This is a statement-ownership repair, not a counterexample
to PR #853's mathematical theorems or certificate.

## MUST finding

- **MUST — package maps overstate formal ownership.**
  `experimental/lean/grande_finale/README.md:24-27 @ c4856fa6` says the module
  formalizes the finite MDS-extension inverse, interpolation-owner partition,
  retained/deleted slack, and graph-arc normalization.
  `experimental/lean/grande_finale/FORMALIZATION_SUMMARY.md:25-27 @ c4856fa6`
  repeats the MDS/slack/graph claim. Both entries were introduced by
  `06b2a6fb`; neither map was in PR #853's file list.

  The source says otherwise. In
  `experimental/lean/grande_finale/GrandeFinale/FirstWallMDSExtensionInverse.lean:3-14 @ c4856fa6`,
  the header limits the module to a finite owner map and leaves the
  Reed--Solomon construction and injectivity-to-augmented-MDS equivalence in
  the mathematical note. Lines 28-80 define only generic finite images,
  fibers, cardinality bounds, equality/injectivity criteria, and an exact
  fiber partition. Lines 82-103 prove five pinned `Nat.choose` arithmetic
  fixtures. There is no Lean interpolation construction, MDS equivalence,
  retained/deleted slack formula, graph, arc, or normalization theorem.

## Repair

Only the two package-map entries change. They now assign the module exactly
the abstract owner-image cap, equality/injectivity criterion, owner-fiber
partition, and five pinned binomial identities that it proves. They explicitly
leave weighted-GRS interpolation, the MDS-extension equivalence,
retained/deleted slack, and graph-arc normalization in the mathematical note.

The repaired SHA-256 values are:

- `experimental/lean/grande_finale/README.md`:
  `80612e1c49043856b0e57588281bb8120c753039b18fcad298341de98899677e`;
- `experimental/lean/grande_finale/FORMALIZATION_SUMMARY.md`:
  `9ef6ec4538e9760c2f05b2b27abce50fa45ecf57a50fe3aee4d4ffa6d56439bc`.

The audit verifier restores each retired entry in isolation and requires the
same scope predicate to reject it. The retired full-file SHA-256 values are
`359b3c332927c834fd59eb5f40df3a590449c240e20f8daa001bdec34c5d262c`
and
`db65f5604ef05b7ba25276db1ced43224fa6f9b7b142c88e80e9f11179a7e7bc`.

## Producer correspondence and certificate freshness

The four substantive PR #853 artifacts are byte-identical at head
`0c8d2c3c`, integration `06b2a6fb`, and current main `c4856fa6`:

- `experimental/notes/thresholds/first_wall_mds_extension_inverse.md`, blob
  `e2f6d996`, SHA-256
  `bbbf4eb88a5a0f693e73393aa27084e66bb68ad249377c88a31596f932743427`;
- `experimental/scripts/verify_first_wall_mds_extension_inverse.py`, blob
  `7ac25269`, SHA-256
  `4286d9d5c6616b03a5c49f9042992efc1d287d735297b0e3faf3e04aa2b4b011`;
- `experimental/data/certificates/first-wall-mds-extension-inverse/first_wall_mds_extension_inverse.json`,
  blob `e8417909`, SHA-256
  `c0c00c665699622b09d02d0b334a4e6fcee9bb51c753be689a76a9022bb01d67`;
- `experimental/lean/grande_finale/GrandeFinale/FirstWallMDSExtensionInverse.lean`,
  blob `e03e8e36`, SHA-256
  `6352005fb4c7223dea2d90e4fe9ba9fa153885c85a4d3e3259facbe753c9449e`.

The frozen certificate's canonical payload SHA-256 is
`65112f380c39047733527493ab9aa233115b0a01a81f72dd7ecfa11b650a2307`.
Its source-manifest hashes equal the actual note and verifier bytes. Its scope
keeps `lean_target_independent: true` and lists weighted-GRS interpolation
formalization as not claimed.

Normal and optimized replay both return `verification: PASS`; their rebuilt
payload matches the frozen JSON. Normal and optimized tamper replay each
reject all `19/19` mutations. Independent standard-library enumeration also
recovers:

- the `F_11` MDS/collision pair counts `70/54`, zero histograms
  `{4:70}` and `{4:50,5:4}`, and exactly four dependent five-sets;
- exactly `100` and `294` graph arcs over `F_5` and `F_7`, equal to the
  nondegenerate quadratic functions; and
- one-point perturbation deficits `2,4,8,10` over fields `5,7,11,13`.

The source note itself states the correct Lean boundary at
`experimental/notes/thresholds/first_wall_mds_extension_inverse.md:453-456 @ c4856fa6`:
finite image cap, equality/injectivity, collision partition, and pinned
binomial values are formalized; weighted-GRS interpolation, MDS equivalence,
and Segre's theorem are not.

## Lean and live-consumer boundary

From `experimental/lean/grande_finale`,

```bash
lake env lean GrandeFinale/FirstWallMDSExtensionInverse.lean
```

exits zero. The module contains no `sorry`, `admit`, custom `axiom`, or
`unsafe` declaration. Its generic finite theorems use only the expected
Mathlib foundations (`propext`, `Classical.choice`, and `Quot.sound`).

Open PR #882 head `af213091` is a clean consumer.
`experimental/lean/grande_finale/GrandeFinale/RSExactCardOccupancyBridge.lean:1-2,60-66 @ af213091`
imports the module and uses only the generic theorem
`card_eq_sum_ownerFiber` to partition explanation states. Its own scope keeps
the semantic classifier and payment outside Lean. The map-only repair changes
no declaration or API used by #882.

Open PR #905 head `00009641` appends to
`experimental/scripts/README.md` and pins that file in its manifest. This
repair deliberately does not touch that related packet map, so no #905 hash
refresh or conflict is created.

## Replay

From repository root:

```bash
python3 experimental/scripts/verify_first_wall_mds_extension_map_audit.py
python3 -O experimental/scripts/verify_first_wall_mds_extension_map_audit.py
python3 -B experimental/scripts/verify_first_wall_mds_extension_inverse.py --check
python3 -B -O experimental/scripts/verify_first_wall_mds_extension_inverse.py --check
python3 -B experimental/scripts/verify_first_wall_mds_extension_inverse.py --tamper-selftest
python3 -B -O experimental/scripts/verify_first_wall_mds_extension_inverse.py --tamper-selftest
```

Expected audit result:

```text
RESULT: PASS (14/14)
STATUS: AUDIT
```

No submission-facing TeX/PDF, mathematical note, certificate, producer
verifier, Lean declaration, theorem API, first-match assignment, numerical
frontier, or proof architecture is changed.
