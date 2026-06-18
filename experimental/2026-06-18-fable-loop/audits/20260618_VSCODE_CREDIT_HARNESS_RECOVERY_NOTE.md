# VS Code Credited-Lane Harness Recovery Note

Status: AUDIT / HARNESS.

Cycle 6 and Cycle 6B both produced `HARNESS_MALFORMED_VISIBLE_TERMINAL`.

The failure is not mathematical and not merely answer length:

- Cycle 6 was long and corrupted in the visible-terminal capture.
- Cycle 6B was short, ASCII-constrained, line-length constrained, and still
  corrupted in `response_malformed_visible_terminal.md`.
- In both cases `sentinelSeen=true`, `adSeenInTranscript=true`, and
  `noOutputTimedOut=false`.

Cycle 6B revealed the correct recovery path:

```text
/Users/danielcabezas/.claude/projects/-Users-danielcabezas-packy-fable-ui/<sessionId>.jsonl
```

The structured Claude CLI JSONL contained a clean assistant message while the
terminal/PTTY scrape dropped spaces/letters and duplicated fragments.

Recommended harness change before another serious VS Code credited theorem run:

1. Keep `terminal_transcript.ansi` as revenue/debug evidence.
2. If terminal extraction is contaminated, locate the `sessionId` from the
   Claude command/process or `.claude/history.jsonl`.
3. Read the matching `.claude/projects/.../<sessionId>.jsonl`.
4. Extract the final assistant message that contains the completion sentinel.
5. Write that clean message to `response.md` only if it is free of prompt echo,
   ad text, terminal chrome, duplicated fragments, and missing-space damage.
6. Otherwise keep the current `response_malformed_visible_terminal.md` behavior.

Until this fallback is implemented, do not spend another serious RS-MCA theorem
call in the VS Code credited lane if a clean theorem artifact is required.
