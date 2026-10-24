"""Analytics helpers: weekly trend + same-document co-occurrence."""

from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations


def _parse_dt(value) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            return datetime.fromisoformat(text)
        except ValueError:
            return datetime.strptime(text[:10], "%Y-%m-%d")
    raise TypeError(f"Unsupported datetime value: {value!r}")


def _week_label(dt: datetime) -> str:
    iso_year, iso_week, _ = dt.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def trend(records: list[dict]) -> list[dict]:
    counts: Counter[tuple[str, str]] = Counter()
    for rec in records:
        week = _week_label(_parse_dt(rec["created_at"]))
        counts[(week, rec["bias_type"])] += 1
    return [
        {"week": week, "bias_type": bias_type, "count": count}
        for (week, bias_type), count in sorted(counts.items())
    ]


def cooccurrence(records: list[dict]) -> list[dict]:
    by_doc: dict[str, set[str]] = defaultdict(set)
    for rec in records:
        by_doc[rec["document_id"]].add(rec["bias_type"])
    pair_counts: Counter[tuple[str, str]] = Counter()
    for biases in by_doc.values():
        for a, b in combinations(sorted(biases), 2):
            pair_counts[(a, b)] += 1
    return [
        {"a": a, "b": b, "count": count}
        for (a, b), count in sorted(pair_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    ]
