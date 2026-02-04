from utils.preprocess import clean_text

def test_cleaning():
    raw = "This movie was GREAT! <br> 10/10"
    cleaned = clean_text(raw)
    assert "great" in cleaned
    assert "<br>" not in cleaned