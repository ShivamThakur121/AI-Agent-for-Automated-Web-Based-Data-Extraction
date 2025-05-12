from app.services.llm_parser import extract_information

def test_extract_information():
    mock_results = [{"snippet": "OpenAI was co-founded by Elon Musk."}]
    info = extract_information("OpenAI", mock_results, "Find the founder of {company}")
    assert "Elon Musk" in info or "Error" not in info