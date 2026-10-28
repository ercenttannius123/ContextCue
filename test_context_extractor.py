import pytest
from context_extractor import extract_context

@pytest.mark.parametrize(
    "message, expected_field, expected_value",
    [
        (
            "Tell me about Interstellar.",
            "current_movie",
            "Interstellar"
        ),
        (
            "I like Christopher Nolan.",
            "current_director",
            "Christopher Nolan"
        ),
        (
            "What movies feature Leonardo DiCaprio?",
            "current_actor",
            "Leonardo DiCaprio"
        ),
    ]
)
def test_entity_extraction(
    message,
    expected_field,
    expected_value
):
    result = extract_context(message)

    assert result[expected_field] == expected_value


def test_no_explicit_entity():
    result = extract_context("Who directed it?")

    assert result == {
        "current_movie": None,
        "current_director": None,
        "current_actor": None
    }
