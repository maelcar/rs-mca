# RS-MCA Frontier Site

Static site for the public RS-MCA frontier board.

## Vercel

Create a Vercel project from this repository and set:

```text
Root Directory: site
Framework Preset: Other
Build Command: empty / none
Output Directory: .
```

The deployed entry point is `index.html`.

## Data Files

- `data/frontier.json`: chart and leaderboard entries.
- `data/updates.json`: browsable result ledger entries for proof notes,
  audits, counterexamples, bridge results, and targets.
- `data/papers.json`: Paper A/B/D/C links, including GitHub PDF and TeX
  source URLs.

The four PDF files are copied into `papers/` because Vercel only serves files
inside the configured root directory.
