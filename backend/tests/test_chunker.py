from app.services.chunker import chunk_text


def test_short_text_single_chunk():
    text = "Hello world, this is short."
    chunks = chunk_text(text)
    assert len(chunks) == 1
    assert chunks[0] == text.strip()


def test_long_doc_bounds_and_overlap():
    words = [f"word{i}" for i in range(500)]
    text = " ".join(words)
    chunks = chunk_text(text)
    assert len(chunks) > 1
    for c in chunks:
        n = len(c.split())
        assert 50 <= n <= 300, f"chunk size {n} out of bounds"
    # overlap: last 50 words of chunk[0] == first 50 words of chunk[1]
    first = chunks[0].split()
    second = chunks[1].split()
    assert first[-50:] == second[:50]
