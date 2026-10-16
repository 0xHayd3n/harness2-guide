#!/usr/bin/env python3
"""Offline publication checks for this independent reading guide (Python 3.11+).

Run from any directory: python scripts/check_docs.py
These checks find documentation defects; they do not validate the paper's research.
Copyright (c) 2026 0xHayd3n. Licensed under scripts/LICENSE (MIT).
"""

from __future__ import annotations

import html
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
ARXIV_ID = "2610.14224"
VERSION = "v1"
PAPER_VERSION = ARXIV_ID + VERSION
PAGE_COUNT = 37
TITLE = "Harness2: Recursive Agent Harnessing for an Open World"
AUTHORS = [
    "Ruiyao Xu", "Yanfei Chen", "Zhongying CuiZhu", "Bhavana Dalvi Mishra",
    "Yifei Ming", "Han Yu", "Rujun Han", "Chen-Yu Lee", "Tomas Pfister",
]
EXPECTED = {
    "README.md", "AGENTS.md", "ATTRIBUTION.md", "CITATION.cff", "CONTRIBUTING.md",
    "LICENSE.md", "SOURCES.md", "VERIFICATION.md", "llms.txt", "references.bib",
    "docs/01-concepts.md", "docs/02-method.md", "docs/03-results.md",
    "docs/04-critical-reading.md", "docs/05-paper-map.md",
    "docs/06-discussion-and-reproduction.md", "metadata/paper.json",
    "metadata/claims.json", "metadata/sources.json", "data/reported-results.json",
    ".gitignore", "scripts/check_docs.py", "scripts/LICENSE", ".github/workflows/docs.yml",
}
ERRORS: list[str] = []
COUNTS = {"files": 0, "local_links": 0, "external_links": 0, "page_links": 0,
          "claims": 0, "sources": 0}


def error(where: str, message: str) -> None:
    ERRORS.append(f"{where}: {message}")


def strings(value: object):
    """Yield strings from arbitrarily nested JSON without assuming a table shape."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from strings(nested)


def normalized_title(value: object) -> str:
    """Compare the paper title across plain text, Unicode, and citation TeX."""
    if not isinstance(value, str):
        return ""
    value = html.unescape(value)
    value = re.sub(r"<sup>\s*2\s*</sup>", "2", value, flags=re.I)
    value = re.sub(r"\$\s*\^\s*\{?\s*2\s*\}?\s*\$", "2", value)
    value = re.sub(r"\^\s*\{?\s*2\s*\}?", "2", value)
    value = unicodedata.normalize("NFKC", value)
    return value.replace("{", "").replace("}", "").casefold()


def masked_markdown(text: str, where: str) -> str:
    """Blank fenced code, preserving line numbers; also check fence closure."""
    fence: tuple[str, int, int] | None = None
    output = []
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= fence[1] and not match[2].strip():
                fence = None
            output.append("\n" if line.endswith("\n") else "")
        elif match and not (match[1][0] == "`" and "`" in match[2]):
            fence = (match[1][0], len(match[1]), number)
            output.append("\n" if line.endswith("\n") else "")
        else:
            output.append(line)
    if fence:
        error(where, f"unclosed fenced code block at line {fence[2]}")
    return "".join(output)


def heading_text(value: str) -> str:
    value = re.sub(r"!?\[([^]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"[\\`*_~]", "", value)
    return value


def anchors(text: str) -> set[str]:
    """GitHub-style heading slugs, including duplicate suffixes and HTML IDs."""
    found = set(re.findall(r"<(?:a|[A-Za-z][\w-]*)\b[^>]*\b(?:id|name)=[\"']([^\"']+)[\"']", text))
    used: dict[str, int] = {}
    lines = text.splitlines()
    for index, line in enumerate(lines):
        atx = re.match(r"^ {0,3}#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$", line)
        label = atx[1] if atx else None
        if label is None and index + 1 < len(lines) and line.strip() and re.match(r"^ {0,3}(?:=+|-+)[ \t]*$", lines[index + 1]):
            label = line.strip()
        if label is None:
            continue
        label = heading_text(label).lower()
        slug = "".join(char for char in label if char in "-_ " or unicodedata.category(char)[0] in "LN")
        slug = slug.replace(" ", "-")
        count = used.get(slug, 0)
        used[slug] = count + 1
        found.add(slug if count == 0 else f"{slug}-{count}")
    return found


def markdown_links(text: str, where: str):
    """Read inline and reference links with balanced destination parentheses."""
    # Inline code does not create links. Fenced code was masked by the caller.
    text = re.sub(r"(`+).*?\1", "", text, flags=re.S)
    definitions: dict[str, str] = {}
    for match in re.finditer(r"^ {0,3}\[([^]\n]+)\]:\s*(?:<([^>\n]+)>|(\S+))", text, re.M):
        definitions[" ".join(match[1].lower().split())] = match[2] or match[3]
        yield match[2] or match[3]
    position = 0
    while position < len(text):
        match = re.search(r"\[[^]\n]*\]\(", text[position:])
        if not match:
            break
        start = position + match.end()
        cursor = start
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        if cursor < len(text) and text[cursor] == "<":
            end = text.find(">", cursor + 1)
            if end == -1:
                error(where, "unterminated angle-bracket link destination")
                break
            yield text[cursor + 1:end]
            position = end + 1
            continue
        depth = 0
        begin = cursor
        while cursor < len(text):
            char = text[cursor]
            if char == "\\":
                cursor += 2
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                if depth == 0:
                    break
                depth -= 1
            elif char.isspace() and depth == 0:
                break
            cursor += 1
        if cursor == len(text):
            error(where, "unterminated inline link destination")
            break
        yield text[begin:cursor]
        position = cursor + 1
    for match in re.finditer(r"\[([^]\n]+)\]\[([^]\n]*)\]", text):
        key = " ".join((match[2] or match[1]).lower().split())
        if key not in definitions:
            error(where, f"undefined reference link [{key}]")
    for match in re.finditer(r"<(https?://[^<>\s]+)>", text):
        yield match[1]
    for match in re.finditer(r"\b(?:href|src)=[\"']([^\"']+)[\"']", text):
        yield html.unescape(match[1])


def check_url(destination: str, where: str, anchor_map: dict[str, set[str]]) -> None:
    destination = html.unescape(re.sub(r"\\([()])", r"\1", destination))
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme not in {"https", "http", "mailto"}:
            error(where, f"unsupported link scheme: {parsed.scheme}")
        if parsed.username or parsed.password:
            error(where, "URL contains embedded credentials")
        COUNTS["external_links"] += 1
        if parsed.hostname in {"arxiv.org", "www.arxiv.org", "export.arxiv.org"} and parsed.path.startswith(f"/pdf/{ARXIV_ID}"):
            if not re.fullmatch(rf"/pdf/{re.escape(PAPER_VERSION)}(?:\.pdf)?", parsed.path):
                error(where, "arXiv PDF links must pin the selected v1 paper")
    else:
        COUNTS["local_links"] += 1
        local_path = unquote(parsed.path)
        target = (ROOT / Path(where).parent / local_path).resolve() if local_path else ROOT / where
        try:
            relative = target.relative_to(ROOT).as_posix()
        except ValueError:
            error(where, f"relative link escapes the repository: {destination}")
            return
        if not target.is_file():
            error(where, f"missing local link target: {destination}")
        elif parsed.fragment and target.suffix.lower() == ".md":
            fragment = unquote(parsed.fragment)
            if fragment not in anchor_map.get(relative, set()):
                error(where, f"missing heading anchor: {destination}")
    for page in parse_qs(parsed.fragment).get("page", []):
        COUNTS["page_links"] += 1
        if not page.isdigit() or not 1 <= int(page) <= PAGE_COUNT:
            error(where, f"PDF page fragment must be in 1..{PAGE_COUNT}: {destination}")


def check_private_material(where: str, text: str) -> None:
    patterns = {
        "private Library identifier": r"\b(?:libfile|library-file)_[A-Za-z0-9]{12,}\b|\bfile_[a-f0-9]{32}\b",
        "GitHub credential": r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b",
        "API credential": r"\b(?:sk-(?:proj-|ant-)?[A-Za-z0-9_-]{24,}|xox[baprs]-[A-Za-z0-9-]{20,})\b",
        "cloud access key": r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
        "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        "bearer credential": r"(?i)\bBearer\s+[A-Za-z0-9._~-]{20,}",
        "signed URL": r"(?i)https?://[^\s<>\"']+[?&](?:x-amz-signature|x-goog-signature|signature|sig|access_token|token)=[^\s<>\"'&]+",
    }
    for label, pattern in patterns.items():
        if re.search(pattern, text):
            error(where, f"possible {label}; remove private material before publication")


def json_object(texts: dict[str, str], name: str) -> dict:
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate object key {key!r}")
            result[key] = value
        return result

    try:
        value = json.loads(texts.get(name, "null"), object_pairs_hook=unique_object,
                           parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"non-finite {value}")))
    except (ValueError, json.JSONDecodeError) as exc:
        error(name, f"invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        error(name, "top-level JSON value must be an object")
        return {}
    return value


def check_json(texts: dict[str, str]) -> None:
    paper = json_object(texts, "metadata/paper.json")
    if normalized_title(paper.get("title")) != normalized_title(TITLE):
        error("metadata/paper.json", f"title must identify {TITLE!r}")
    for field, expected in {"arxiv_id": ARXIV_ID, "version": VERSION,
                            "pages": PAGE_COUNT, "authors": AUTHORS,
                            "scope": "independent_reading_guide"}.items():
        if paper.get(field) != expected:
            error("metadata/paper.json", f"{field} must equal {expected!r}")
    for field, route in (("pdf_url", "pdf"), ("abstract_url", "abs")):
        urls = {f"https://arxiv.org/{route}/{PAPER_VERSION}"}
        if route == "pdf":
            urls.add(f"https://arxiv.org/{route}/{PAPER_VERSION}.pdf")
        if paper.get(field) not in urls:
            error("metadata/paper.json", f"{field} must pin official arXiv {PAPER_VERSION}")
    if not re.fullmatch(r"[0-9a-f]{64}", str(paper.get("source_sha256", ""))):
        error("metadata/paper.json", "source_sha256 must be a lowercase SHA-256 digest")
    if type(paper.get("size_bytes")) is not int or paper.get("size_bytes", 0) <= 0:
        error("metadata/paper.json", "size_bytes must be a positive integer")
    if paper.get("doi") != f"10.48550/arXiv.{ARXIV_ID}":
        error("metadata/paper.json", "unexpected arXiv DOI")

    source_data = json_object(texts, "metadata/sources.json")
    source_rows = source_data.get("sources", [])
    if not isinstance(source_rows, list) or not source_rows:
        error("metadata/sources.json", "sources must be a nonempty array")
        source_rows = []
    source_ids: set[str] = set()
    for source in source_rows:
        if not isinstance(source, dict):
            error("metadata/sources.json", "every source must be an object")
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id or source_id in source_ids:
            error("metadata/sources.json", f"empty or duplicate source id: {source_id!r}")
        else:
            source_ids.add(source_id)
        for field in ("url", "role", "status", "notes"):
            if not isinstance(source.get(field), str) or not source[field].strip():
                error("metadata/sources.json", f"source {source_id!r} needs {field}")
        if source_id == "paper-v1" and PAPER_VERSION not in str(source.get("url", "")):
            error("metadata/sources.json", "paper-v1 URL must pin v1")
    required_sources = {"paper-v1", "arxiv-version-history", "authors-code", "authors-site", "paper-license", "code-license"}
    if required_sources - source_ids:
        error("metadata/sources.json", f"missing source ids: {', '.join(sorted(required_sources - source_ids))}")
    COUNTS["sources"] = len(source_rows)

    claims = json_object(texts, "metadata/claims.json")
    if claims.get("paper_version") != PAPER_VERSION:
        error("metadata/claims.json", "paper_version must pin v1")
    claim_rows = claims.get("claims", [])
    if not isinstance(claim_rows, list) or not claim_rows:
        error("metadata/claims.json", "claims must be a nonempty array")
        claim_rows = []
    claim_ids: set[str] = set()
    for claim in claim_rows:
        if not isinstance(claim, dict):
            error("metadata/claims.json", "every claim must be an object")
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id or claim_id in claim_ids:
            error("metadata/claims.json", f"empty or duplicate claim id: {claim_id!r}")
        else:
            claim_ids.add(claim_id)
        if claim.get("kind") not in {"reported", "method", "interpretation"}:
            error("metadata/claims.json", f"claim {claim_id!r} has an invalid kind")
        for field in ("claim", "caveat"):
            if not isinstance(claim.get(field), str) or not claim[field].strip():
                error("metadata/claims.json", f"claim {claim_id!r} needs {field}")
        evidence = claim.get("evidence", [])
        if not isinstance(evidence, list) or not evidence:
            error("metadata/claims.json", f"claim {claim_id!r} needs evidence")
            continue
        for item in evidence:
            if not isinstance(item, dict):
                error("metadata/claims.json", f"claim {claim_id!r} evidence must be an object")
                continue
            if not isinstance(item.get("source_id"), str) or item["source_id"] not in source_ids:
                error("metadata/claims.json", f"claim {claim_id!r} references an unknown source")
            if not isinstance(item.get("locator"), str) or not item["locator"].strip():
                error("metadata/claims.json", f"claim {claim_id!r} needs an evidence locator")
            pages = item.get("pages")
            if not isinstance(pages, list) or not pages or any(type(page) is not int or not 1 <= page <= PAGE_COUNT for page in pages):
                error("metadata/claims.json", f"claim {claim_id!r} evidence pages must be integers in 1..{PAGE_COUNT}")
    COUNTS["claims"] = len(claim_rows)
    results = json_object(texts, "data/reported-results.json")
    if not any(PAPER_VERSION in value for value in strings(results)):
        error("data/reported-results.json", "reported results must identify the pinned paper version")
    check_result_tree(results, source_ids, claim_ids)
    check_reported_tables(results)


def check_result_tree(value: object, source_ids: set[str], claim_ids: set[str], location: str = "data/reported-results.json") -> None:
    """Validate cross-references and numeric sanity without forcing a table schema."""
    if isinstance(value, dict):
        for key, nested in value.items():
            label = f"{location}.{key}"
            if key == "source_id" and (not isinstance(nested, str) or nested not in source_ids):
                error(label, "unknown source id")
            elif key == "claim_id" and (not isinstance(nested, str) or nested not in claim_ids):
                error(label, "unknown claim id")
            elif key in {"pdf_page", "page"} or key.endswith("_pdf_page"):
                if type(nested) is not int or not 1 <= nested <= PAGE_COUNT:
                    error(label, f"page must be an integer in 1..{PAGE_COUNT}")
            elif key in {"pdf_pages", "pages"} or key.endswith("_pdf_pages"):
                if not isinstance(nested, list) or any(type(page) is not int or not 1 <= page <= PAGE_COUNT for page in nested):
                    error(label, f"pages must be integers in 1..{PAGE_COUNT}")
            check_result_tree(nested, source_ids, claim_ids, label)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            check_result_tree(nested, source_ids, claim_ids, f"{location}[{index}]")
    elif isinstance(value, float) and not math.isfinite(value):
        error(location, "non-finite number")


def check_reported_tables(results: dict) -> None:
    """Crosscheck this transcription, not the authors' unreleased raw measurements."""
    where = "data/reported-results.json"
    if results.get("paper_id") != "arxiv:" + PAPER_VERSION:
        error(where, "paper_id must identify the pinned arXiv version")
    if results.get("source_pdf_url") != f"https://arxiv.org/pdf/{PAPER_VERSION}":
        error(where, "source_pdf_url must match the pinned official PDF")
    tables = results.get("tables", {})
    if not isinstance(tables, dict):
        error(where, "tables must be an object")
        return
    expected_columns = {
        "table_1": ["code_score", "code_steps", "web_score", "web_steps", "office_score", "office_steps", "avg_score", "avg_steps"],
        "table_2": ["jobbench_score", "jobbench_steps", "lab_partial", "lab_steps"],
    }
    expected_methods = {"base", "reasoningbank", "meta_harness", "harness_scaling", "harness2", "parallel_recursion_delta"}
    configurations = {(executor, harness) for executor in ("Gemini 3.5 Flash", "GLM-5") for harness in ("OpenCode", "Codex")}
    lookup: dict[tuple, dict] = {}

    def number(value: object) -> bool:
        return type(value) in {int, float} and math.isfinite(value)

    def equal(actual: object, expected: object, label: str, tolerance: float = 0.00001) -> None:
        if not number(actual) or not number(expected) or not math.isclose(actual, expected, abs_tol=tolerance):
            error(label, f"inconsistent value: {actual!r}; expected {expected!r}")

    for table_id, columns in expected_columns.items():
        table = tables.get(table_id, {})
        label = f"{where}.{table_id}"
        if not isinstance(table, dict):
            error(label, "table must be an object")
            continue
        if table.get("columns") != columns:
            error(label, "column definitions differ from the transcribed table")
        expected_page = 8 if table_id == "table_1" else 9
        if table.get("pdf_page") != expected_page:
            error(label, f"table belongs to PDF page {expected_page}")
        rows = table.get("rows", [])
        if not isinstance(rows, list) or len(rows) != 24:
            error(label, "expected 24 transcribed rows")
        if not isinstance(rows, list):
            continue
        seen: set[tuple] = set()
        for row in rows:
            if not isinstance(row, dict):
                error(label, "row must be an object")
                continue
            identity = tuple(row.get(field) for field in ("executor", "initial_harness", "method"))
            if any(not isinstance(part, str) for part in identity):
                error(label, "row identity fields must be strings")
                continue
            if identity in seen or identity[:2] not in configurations or identity[2] not in expected_methods:
                error(label, f"duplicate or unexpected row identity: {identity!r}")
            seen.add(identity)
            lookup[(table_id, *identity)] = row
            is_delta = identity[2] == "parallel_recursion_delta"
            if row.get("kind") != ("delta_from_harness2_k1" if is_delta else "mean_sd"):
                error(label, f"incorrect row kind for {identity!r}")
            if is_delta and (row.get("k") != 5 or row.get("recursion") != "parallel"):
                error(label, "delta rows must describe parallel k=5 minus k=1")
            if identity[2] == "harness2" and row.get("k") != 1:
                error(label, "Harness2 mean/SD rows must describe k=1")
            values = row.get("values", {})
            if not isinstance(values, dict) or set(values) != set(columns):
                error(label, f"missing or unexpected metric columns in {identity!r}")
                continue
            for metric, cell in values.items():
                expected_fields = {"delta"} if is_delta else {"mean", "sd"}
                if not isinstance(cell, dict) or set(cell) != expected_fields or not all(number(value) for value in cell.values()):
                    error(label, f"{identity!r}/{metric} must contain {sorted(expected_fields)} numbers; k=5 SD is not reported")
                    continue
                if not is_delta and (cell["mean"] < 0 or cell["sd"] < 0):
                    error(label, "means and standard deviations must be nonnegative")
                if metric.endswith("score") or metric == "lab_partial":
                    if is_delta and cell["delta"] <= 0:
                        error(label, "reported k=5 score deltas must be positive")
                    elif not is_delta and cell["mean"] > 100:
                        error(label, "reported scores must be on their documented 0..100 display scale")
            if table_id == "table_1" and all(isinstance(values.get(metric), dict) for metric in columns):
                field = "delta" if is_delta else "mean"
                for suffix in ("score", "steps"):
                    domain = [values[f"{name}_{suffix}"].get(field) for name in ("code", "web", "office")]
                    if all(number(value) for value in domain):
                        equal(values[f"avg_{suffix}"].get(field), sum(domain) / 3, f"{label}/{identity!r}/avg_{suffix}", 0.11)
        if len(seen) != 24:
            error(label, "expected all four executor/harness configurations and six methods")

    def table_cell(table_id: str, executor: str, harness: str, method: str, metric: str, field: str):
        row = lookup.get((table_id, executor, harness, method), {})
        return row.get("values", {}).get(metric, {}).get(field)

    summary = results.get("main_summary", [])
    if not isinstance(summary, list) or len(summary) != 12:
        error(where, "main_summary must contain 12 benchmark/configuration rows")
        summary = []
    summary_seen = set()
    benchmark_metrics = {"WorkBuddy-Bench": ("table_1", "avg_score"), "JobBench": ("table_2", "jobbench_score"), "LAB": ("table_2", "lab_partial")}
    for row in summary:
        if not isinstance(row, dict):
            error(where, "summary row must be an object")
            continue
        identity = tuple(row.get(field) for field in ("executor", "initial_harness", "benchmark"))
        if any(not isinstance(part, str) for part in identity):
            error(where, "summary identity fields must be strings")
            continue
        executor, harness, benchmark = identity
        if identity in summary_seen or (executor, harness) not in configurations or benchmark not in benchmark_metrics:
            error(where, f"duplicate or unexpected summary row {identity!r}")
            continue
        summary_seen.add(identity)
        table_id, metric = benchmark_metrics[benchmark]
        if row.get("metric") != metric:
            error(where, f"summary metric inconsistent for {identity!r}")
        if row.get("source_pdf_page") != (8 if table_id == "table_1" else 9):
            error(where, f"summary table page inconsistent for {identity!r}")
        base = table_cell(table_id, executor, harness, "base", metric, "mean")
        k1 = table_cell(table_id, executor, harness, "harness2", metric, "mean")
        delta = table_cell(table_id, executor, harness, "parallel_recursion_delta", metric, "delta")
        for field, expected in (("base_mean", base), ("k1_mean", k1), ("k5_delta", delta)):
            equal(row.get(field), expected, f"{where}/summary/{identity!r}/{field}")
        if all(number(value) for value in (base, k1, delta)):
            equal(row.get("k1_gain_over_base"), round(k1 - base, 1), f"{where}/summary/{identity!r}/k1_gain_over_base")
            equal(row.get("k5_derived_mean"), round(k1 + delta, 1), f"{where}/summary/{identity!r}/k5_derived_mean")
            if k1 <= base:
                error(where, f"summary k=1 gain is not positive for {identity!r}")

    for table_id, count, page in (("table_3", 4, 10), ("table_4", 28, 19)):
        table = tables.get(table_id, {})
        if not isinstance(table, dict) or not isinstance(table.get("rows"), list) or len(table["rows"]) != count or table.get("pdf_page") != page:
            error(where, f"{table_id} must have {count} rows and PDF page {page}")
            continue
        for row in table["rows"]:
            if not isinstance(row, dict):
                error(where, f"{table_id} row must be an object")
            elif table_id == "table_4" and any(type(row.get(field)) is not bool for field in ("label", "streaming", "scaling", "improver_update")):
                error(where, "Table 4 categorization flags must be booleans")
            elif table_id == "table_3":
                scores = row.get("scores", {})
                if not isinstance(scores, dict) or set(scores) != {"WorkBuddy-Bench", "JobBench"} or any(not number(value) or not 0 <= value <= 100 for value in scores.values()):
                    error(where, "Table 3 scores must contain both documented benchmark scales")
                elif row.get("method") == "harness2":
                    for benchmark, value in scores.items():
                        table_id_source, metric = benchmark_metrics[benchmark]
                        expected = table_cell(table_id_source, "Gemini 3.5 Flash", "OpenCode", "harness2", metric, "mean")
                        equal(value, expected, f"{where}/table_3/{benchmark}")


def check_citations(texts: dict[str, str]) -> None:
    cff = texts.get("CITATION.cff", "")
    bib = texts.get("references.bib", "")
    for where, content in (("CITATION.cff", cff), ("references.bib", bib)):
        if normalized_title(TITLE) not in normalized_title(content):
            error(where, "paper title missing or inconsistent")
        if ARXIV_ID not in content:
            error(where, "paper arXiv identifier missing")
        if PAPER_VERSION not in content:
            error(where, "citation must include a v1-pinned paper URL")
    if "preferred-citation:" not in cff:
        error("CITATION.cff", "needs a preferred-citation for the paper")
    if not re.search(r"eprint\s*=\s*[{\"]" + re.escape(ARXIV_ID) + r"(?:v1)?[}\"]", bib, re.I):
        error("references.bib", "eprint must identify the paper")


def main() -> int:
    publication_paths = [path for path in ROOT.rglob("*") if ".git" not in path.relative_to(ROOT).parts]
    for path in publication_paths:
        if path.is_symlink():
            error(path.relative_to(ROOT).as_posix(), "symlinks are not allowed in the publication tree")
    actual = {path.relative_to(ROOT).as_posix() for path in publication_paths if path.is_file()}
    for name in sorted(EXPECTED - actual):
        error(name, "required publication file is missing")
    for name in sorted(actual - EXPECTED):
        error(name, "file is outside the publication allowlist")
    texts: dict[str, str] = {}
    for name in sorted(actual):
        path = ROOT / name
        if path.is_symlink():
            continue
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            error(name, "file is not UTF-8 text")
            continue
        if text.startswith("\ufeff"):
            error(name, "UTF-8 BOM is not allowed")
        if any(unicodedata.category(char) == "Cc" and char not in "\t\r\n" for char in text):
            error(name, "unexpected control character")
        check_private_material(name, text)
        texts[name] = text
    COUNTS["files"] = len(texts)
    markdown = {name: masked_markdown(text, name) for name, text in texts.items() if name.endswith(".md")}
    anchor_map = {name: anchors(text) for name, text in markdown.items()}
    for name, text in markdown.items():
        for destination in markdown_links(text, name):
            check_url(destination, name, anchor_map)
    # JSON and source notes can contain bare PDF links as well as Markdown links.
    for name, text in texts.items():
        for match in re.finditer(r"https?://[^\s<>\"')]+#page=[^\s<>\"')]+", text):
            page = re.split(r"[&#]", match[0].split("#page=", 1)[1])[0]
            if not page.isdigit() or not 1 <= int(page) <= PAGE_COUNT:
                error(name, f"PDF page fragment outside 1..{PAGE_COUNT}")
    check_json(texts)
    check_citations(texts)
    if ERRORS:
        print(f"Documentation checks FAILED ({len(ERRORS)} errors):")
        for message in ERRORS:
            print(f"  - {message}")
        return 1
    summary = ", ".join(f"{value} {key.replace('_', ' ')}" for key, value in COUNTS.items())
    print(f"Documentation checks passed: {summary}.")
    print("Offline only: external HTTP availability, full CFF schema, and research claims require separate review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
