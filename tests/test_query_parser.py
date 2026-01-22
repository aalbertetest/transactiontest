from mini_search.query_parser import AndNode, PhraseNode, QueryParser, TermNode


def test_query_parser_phrase_and_term() -> None:
    parser = QueryParser()
    parsed = parser.parse('"search engine" AND crawler')
    assert ("search", "engine") in parsed.phrases
    assert "crawler" in parsed.terms


def test_query_parser_implicit_and() -> None:
    parser = QueryParser()
    parsed = parser.parse("search engine")
    assert set(parsed.terms) == {"search", "engine"}
    assert isinstance(parsed.ast, AndNode)
    assert isinstance(parsed.ast.left, TermNode)
    assert isinstance(parsed.ast.right, TermNode)
