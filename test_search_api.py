from app.services.search_api import search_web

def test_search_web():
    results = search_web("OpenAI", "Find the founder of {company}")
    assert isinstance(results, list)
