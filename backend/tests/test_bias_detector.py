from app.services.bias_detector import detect_biases


def test_confirmation_and_sunk_flagged_with_quotes():
    text = (
        "I always knew I was right about this; it proves me right. "
        "We already invested so much money and time, we can't quit now."
    )
    results = detect_biases(text)
    by_type = {r["bias_type"] for r in results}
    assert "confirmation_bias" in by_type
    assert "sunk_cost" in by_type
    for r in results:
        assert r["quote"], "quote must be non-empty"
        assert len(r["quote"]) <= 200
        assert 0.55 <= r["confidence"] <= 0.8
        assert r["explanation"]
        assert set(r.keys()) >= {"bias_type", "quote", "confidence", "explanation"}


def test_neutral_text_clean():
    results = detect_biases("The gauge rose 12% after calibration.")
    assert results == []
