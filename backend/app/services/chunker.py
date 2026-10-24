"""Word-window chunker: ~200 words per chunk with 50-word overlap.

Short-tail rule: if the last chunk has <150 words, merge it into the
previous chunk (full chunks keep the 50-word overlap).
"""

CHUNK_WORDS = 200
OVERLAP_WORDS = 50
MIN_TAIL_WORDS = 150


def chunk_text(text: str) -> list[str]:
    stripped = (text or "").strip()
    if not stripped:
        return []
    words = stripped.split()
    if len(words) <= CHUNK_WORDS:
        return [stripped]
    chunks: list[str] = []
    starts: list[int] = []
    step = CHUNK_WORDS - OVERLAP_WORDS
    for start in range(0, len(words), step):
        chunk = words[start : start + CHUNK_WORDS]
        if not chunk:
            break
        chunks.append(" ".join(chunk))
        starts.append(start)
        if start + CHUNK_WORDS >= len(words):
            break
    if len(chunks) >= 2 and len(chunks[-1].split()) < MIN_TAIL_WORDS:
        chunks[-2] = " ".join(words[starts[-2] :])
        chunks.pop()
    return chunks
