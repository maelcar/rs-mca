#!/usr/bin/env python3
"""Extract labeled theorem-like environments from the rs-mca TeX sources."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DEFAULT_TEX = [
    "tex/RS_disproof_v3.tex",
    "tex/slackMCA_v3.tex",
    "tex/cs25_cap_v4.tex",
    "tex/snarks_v4.tex",
    "tex/proximity_blueprint_v3.tex",
]

PRIMARY_ENVS = {
    "theorem",
    "lemma",
    "proposition",
    "corollary",
    "conjecture",
    "definition",
    "assumption",
    "problem",
    "openproblem",
}

EXTRA_ENVS = {
    "fact",
    "designrule",
    "construction",
    "example",
    "remark",
    "task",
    "milestone",
}

ITEM_LABEL_PREFIXES = {
    "ass",
    "con",
    "conj",
    "cor",
    "def",
    "ex",
    "fact",
    "lem",
    "milestone",
    "op",
    "prob",
    "prop",
    "rem",
    "rule",
    "task",
    "thm",
}

CS25_CONDITIONAL_LABELS = {
    "thm:informal",
    "thm:A",
    "thm:B",
    "thm:main",
    "cor:grand",
    "cor:deployed",
    "cor:rows",
    "prop:slacked",
    "cor:Fvalued",
}

BEGIN_RE = re.compile(r"\\begin\{(?P<env>[A-Za-z*]+)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:[Cc]?ref|eqref)\{([^}]+)\}")
COMMAND_RE = re.compile(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?")
MATH_RE = re.compile(r"\$[^$]*\$|\\\[[\s\S]*?\\\]")
SPACE_RE = re.compile(r"\s+")


def strip_tex(text: str) -> str:
    """A compact, lossy TeX-to-text normalizer for label-map summaries."""
    text = MATH_RE.sub(" [math] ", text)
    text = text.replace("~", " ").replace("--", "-")
    text = re.sub(r"%.*", "", text)
    text = re.sub(r"\\(?:C|c)?ref\{([^}]+)\}", r"ref:\1", text)
    text = re.sub(r"\\eqref\{([^}]+)\}", r"eq:\1", text)
    text = re.sub(r"\\item(?:\[[^\]]*\])?", " ", text)
    text = re.sub(r"\\begin\{[^}]+\}|\\end\{[^}]+\}", " ", text)
    text = COMMAND_RE.sub(lambda m: m.group(1) or " ", text)
    text = re.sub(r"[{}]", "", text)
    return SPACE_RE.sub(" ", text).strip()


def parse_optional_title(line: str, pos: int) -> str:
    rest = line[pos:].lstrip()
    if not rest.startswith("["):
        return ""
    depth = 0
    chars: list[str] = []
    for char in rest:
        if char == "[":
            if depth > 0:
                chars.append(char)
            depth += 1
            continue
        if char == "]":
            depth -= 1
            if depth == 0:
                return "".join(chars)
            chars.append(char)
            continue
        chars.append(char)
    return "".join(chars)


def summarize(body: str, max_chars: int = 210) -> str:
    cleaned = strip_tex(body)
    if not cleaned:
        return ""
    first = re.split(r"(?<=[.!?])\s+", cleaned)[0]
    if len(first) < 60 and len(cleaned) > len(first):
        first = cleaned[: max_chars + 1]
    if len(first) > max_chars:
        first = first[:max_chars].rsplit(" ", 1)[0] + " ..."
    return first


def status_for(env: str, title: str, body: str) -> str:
    hay = f"{title} {body[:800]}".lower()
    if env in {"conjecture", "problem", "openproblem"}:
        return "CONJECTURAL"
    if env == "assumption":
        return "CONDITIONAL"
    if "counterexample" in hay or "disproof" in hay or "refuted" in hay:
        return "COUNTEREXAMPLE"
    if "experimental" in hay or "verified" in hay or "computation" in hay:
        return "EXPERIMENTAL/AUDIT"
    if (
        "imported" in hay
        or "conditional" in hay
        or "assuming" in hay
        or "crites" in hay
        or "stewart" in hay
        or "bchks" in hay
        or "as stated" in hay
    ):
        return "CONDITIONAL"
    if env in {"definition", "designrule", "construction", "example"}:
        return "AUDIT"
    if env in {"remark"}:
        return "AUDIT"
    return "PROVED"


def is_item_label(label: str) -> bool:
    return label.split(":", 1)[0] in ITEM_LABEL_PREFIXES


def apply_source_overrides(source_name: str, label: str, status: str) -> str:
    if source_name == "tex/cs25_cap_v4.tex" and label in CS25_CONDITIONAL_LABELS:
        return "CONDITIONAL"
    return status


def find_end(lines: list[str], start_idx: int, env: str) -> int:
    end_pat = re.compile(rf"\\end\{{{re.escape(env)}\}}")
    for idx in range(start_idx, len(lines)):
        if end_pat.search(lines[idx]):
            return idx
    return start_idx


def extract_file(path: Path, include_extra: bool) -> list[dict[str, object]]:
    wanted = set(PRIMARY_ENVS)
    if include_extra:
        wanted |= EXTRA_ENVS
    try:
        source_name = path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        source_name = path.as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[dict[str, object]] = []
    idx = 0
    while idx < len(lines):
        match = BEGIN_RE.search(lines[idx])
        if not match or match.group("env") not in wanted:
            idx += 1
            continue
        env = match.group("env")
        title = strip_tex(parse_optional_title(lines[idx], match.end()))
        end_idx = find_end(lines, idx, env)
        body_lines = lines[idx : end_idx + 1]
        body = "\n".join(body_lines)
        statement_body = "\n".join(body_lines[1:-1])
        statement_body = LABEL_RE.sub("", statement_body)
        labels = [label for label in LABEL_RE.findall(body) if is_item_label(label)]
        if not labels:
            idx = end_idx + 1
            continue
        refs = []
        for raw in REF_RE.findall(body):
            refs.extend(part.strip() for part in raw.split(",") if part.strip())
        for label in labels:
            status = status_for(env, title, body)
            status = apply_source_overrides(source_name, label, status)
            out.append(
                {
                    "source": source_name,
                    "line": idx + 1,
                    "end_line": end_idx + 1,
                    "env": env,
                    "label": label,
                    "title": title,
                    "summary": summarize(statement_body),
                    "status": status,
                    "refs": sorted(set(refs)),
                }
            )
        idx = end_idx + 1
    return out


def emit_markdown(items: list[dict[str, object]], include_extra: bool) -> str:
    lines = [
        "# Theorem Label Map",
        "",
        "Generated by `agent_context/extract_labels.py` from TeX sources. Status is a first-pass tag inferred from environment/type/title/body; audit before citing as final.",
        "",
        "| Source | Line | Kind | Label | Displayed title/name | Status | Short statement summary | Cross-refs |",
        "|---|---:|---|---|---|---|---|---|",
    ]
    for item in items:
        refs = ", ".join(item["refs"]) if item["refs"] else ""
        title = item["title"] or ""
        row = [
            str(item["source"]),
            str(item["line"]),
            str(item["env"]),
            f"`{item['label']}`",
            title.replace("|", "\\|"),
            str(item["status"]),
            str(item["summary"]).replace("|", "\\|"),
            refs.replace("|", "\\|"),
        ]
        lines.append("| " + " | ".join(row) + " |")
    if include_extra:
        lines.append("")
        lines.append("Extra labeled examples, remarks, design rules, tasks, and milestones are included because they are cross-citation relevant.")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-extra", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("tex", nargs="*", default=DEFAULT_TEX)
    args = parser.parse_args()

    root = Path.cwd()
    items: list[dict[str, object]] = []
    for source in args.tex:
        path = root / source
        items.extend(extract_file(path, include_extra=args.include_extra))
    markdown = emit_markdown(items, include_extra=args.include_extra)
    if args.output:
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")


if __name__ == "__main__":
    main()
