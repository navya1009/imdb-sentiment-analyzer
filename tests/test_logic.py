import pytest
from utils.preprocess import clean_text

def test_clean_text_lowercase():
    assert clean_text("HELLO World") == "hello world"

def test_clean_text_removes_html():
    # If your clean_text doesn't handle <br>, this is a good time to fix it!
    assert "<br>" not in clean_text("Bad movie <br> would not watch")

def test_clean_text_removes_punctuation():
    assert "!!!" not in clean_text("Amazing!!!")