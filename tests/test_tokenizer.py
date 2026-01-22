from mini_search.tokenizer import tokenize, tokenize_with_positions


def test_tokenize_basic() -> None:
    text = "Search engines, search!"
    assert tokenize(text) == ["search", "engines", "search"]


def test_tokenize_with_positions() -> None:
    text = "A quick brown fox"
    tokens = tokenize_with_positions(text)
    assert tokens == [("quick", 1), ("brown", 2), ("fox", 3)]
