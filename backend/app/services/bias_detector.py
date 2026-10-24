"""Rule-based detector for 15 cognitive biases + LLM passthrough hook."""

import os
import re

BIAS_PATTERNS: dict[str, tuple[str, float, str]] = {
    "confirmation_bias": (
        r"\bi always knew\b|\bknew i was right\b|\bproves? me right\b"
        r"|\bconfirms? what i (believed|thought|expected)\b"
        r"|\bonly (read|trust|listen to)\b.*\b(agree|same view|same opinion)\b",
        0.72,
        "Interprets evidence as confirmation of a prior belief.",
    ),
    "sunk_cost": (
        r"\balready (invested|spent|put in)\b|\bcan'?t (quit|stop|walk away) now\b"
        r"|\btoo (much|far in) to (quit|stop)\b"
        r"|\bafter all (i'?ve|we'?ve|they'?ve) (invested|spent|put)\b"
        r"|\bstick with it since\b",
        0.70,
        "Continues only because of past investment, not future value.",
    ),
    "availability_heuristic": (
        r"\beveryone i know\b|\bi (keep )?(hear|see) it everywhere\b"
        r"|\brecent headlines?\b.*\b(must|means|proves?)\b"
        r"|\b(it'?s all over the news\b.*\bso it must\b)",
        0.62,
        "Judges likelihood by how easily examples come to mind.",
    ),
    "anchoring": (
        r"\bfirst (price|offer|number|impression)\b|\banchored\b"
        r"|\bstarting (at|from)\b.*\b(seems|makes)\b.*\b(cheap|expensive)\b"
        r"|\binitial (estimate|figure)\b.*\b(can'?t|won'?t) (ignore|shake)\b",
        0.60,
        "Leans too heavily on the first number or impression.",
    ),
    "in_group_bias": (
        r"\bthose people\b|\bthese people\b"
        r"|\bour (kind|group|team) (is|are) (better|superior)\b"
        r"|\boutsiders?\b.*\b(can'?t|don'?t) understand\b",
        0.64,
        "Favours one's own group over outsiders.",
    ),
    "attribution_error": (
        r"\b(he|she|they) (failed|messed up) because (he|she|they) (is|are) "
        r"(lazy|stupid|incompetent)\b|\btypical of (him|her|them)\b"
        r"|\b(it'?s just who (he|she|they) (is|are))\b",
        0.61,
        "Blames personality while ignoring the situation.",
    ),
    "black_and_white": (
        r"\bno middle ground\b|\b(all|totally|completely) (good|bad|evil|perfect|worthless)\b"
        r"|\b(either|everything is) (perfect|a disaster)\b|\bwith me or against me\b",
        0.66,
        "Sees things in extremes with no middle ground.",
    ),
    "catastrophising": (
        r"\b(disaster|catastrophe|doomed|ruined)\b"
        r"|\bworst (case|thing)\b.*\b(ever|possible|imaginable)\b"
        r"|\beverything (will|is going to) (fall apart|collapse|fail)\b",
        0.68,
        "Expects the worst possible outcome.",
    ),
    "mind_reading": (
        r"\bi know what (he|she|they) (think|are thinking|want)\b"
        r"|\b(they|he|she) (must |probably )?(think|believes?) (i'?m|i am)\b"
        r"|\bwithout (asking|checking)\b.*\b(i know|assume)\b.*\b(think|feel)\b",
        0.63,
        "Assumes what others think without checking.",
    ),
    "fortune_telling": (
        r"\bi know (what will|what'?s going to) happen\b"
        r"|\b(it|things) will (definitely|certainly) (fail|go wrong)\b"
        r"|\bno point trying\b.*\b(will|going to) fail\b",
        0.65,
        "Predicts a bad future as if it were certain.",
    ),
    "emotional_reasoning": (
        r"\bi feel (like|as if|that)\b.*\b(so|therefore|must be) (true|real|right)\b"
        r"|\bbecause i feel\b.*\b(it must|it is)\b"
        r"|\bmy (feelings|emotions|gut) prove\b",
        0.60,
        "Treats feelings as proof of facts.",
    ),
    "overgeneralisation": (
        r"\b(always|never) happens\b"
        r"|\bevery (single )?(time|one|person)\b.*\b(fails?|wrongs?|lets? me down)\b"
        r"|\bnothing ever works\b",
        0.67,
        "Turns one event into a never-ending pattern.",
    ),
    "personalisation": (
        r"\ball my fault\b|\bbecause of me\b.*\b(happened|failed|went wrong)\b"
        r"|\bi('?m| am) (to blame|responsible for everything)\b",
        0.62,
        "Takes personal blame for things outside one's control.",
    ),
    "mental_filtering": (
        r"\bonly the (bad|negative|failures?)\b.*\b(matter|count|remember)\b"
        r"|\b(ignore|dismiss)\b.*\b(good|positive|success)\b"
        r"|\bnothing good\b.*\b(matters?|counts?)\b",
        0.58,
        "Dwelling only on the negative while filtering out the positive.",
    ),
    "dunning_kruger": (
        r"\bi('?m| am) (clearly |obviously )?(an expert|the best|smarter than)\b"
        r"|\b(no one|nobody) (knows|understands) (this|it) better than (me|i)\b"
        r"|\bit'?s (so )?obvious\b.*\b(experts? are wrong|others? are stupid)\b",
        0.55,
        "Overestimates one's own competence.",
    ),
}

_COMPILED: dict[str, re.Pattern] = {
    name: re.compile(pattern, re.IGNORECASE) for name, (pattern, _, _) in BIAS_PATTERNS.items()
}

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _quote_for(chunk: str, match: re.Match) -> str:
    sentences = _SENT_SPLIT.split(chunk.strip())
    pos = match.start()
    offset = 0
    for sent in sentences:
        start = chunk.find(sent, offset)
        if start == -1:
            start = offset
        end = start + len(sent)
        if start <= pos < end:
            return sent.strip()[:200]
        offset = end
    return match.group(0).strip()[:200]


def detect_biases(chunk: str) -> list[dict]:
    if not chunk or not chunk.strip():
        return []
    results: list[dict] = []
    for bias_type, (_, confidence, explanation) in BIAS_PATTERNS.items():
        pattern = _COMPILED[bias_type]
        match = pattern.search(chunk)
        if match:
            results.append(
                {
                    "bias_type": bias_type,
                    "quote": _quote_for(chunk, match),
                    "confidence": confidence,
                    "explanation": explanation,
                }
            )
    return results


def detect_biases_llm(chunk: str) -> list[dict]:
    """LLM hook: use rule-based mock when no API keys are configured."""
    if os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"):
        return detect_biases(chunk)
    return detect_biases(chunk)
