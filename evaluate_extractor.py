import time
from context_extractor import extract_context

test_cases = [
    # Movie extraction
    ("Tell me about Interstellar.", "current_movie", "Interstellar"),
    ("Explain the movie Titanic.", "current_movie", "Titanic"),
    ("What is Inception about?", "current_movie", "Inception"),
    ("I watched Avatar yesterday.", "current_movie", "Avatar"),
    ("Have you seen The Dark Knight?", "current_movie", "The Dark Knight"),

    # Director extraction
    ("I like Christopher Nolan.", "current_director", "Christopher Nolan"),
    ("Steven Spielberg is my favorite director.", "current_director", "Steven Spielberg"),
    ("What films did James Cameron direct?", "current_director", "James Cameron"),
    ("Tell me about Quentin Tarantino.", "current_director", "Quentin Tarantino"),
    ("I admire Martin Scorsese.", "current_director", "Martin Scorsese"),

    # Actor extraction
    ("Leonardo DiCaprio is a great actor.", "current_actor", "Leonardo DiCaprio"),
    ("What movies feature Tom Cruise?", "current_actor", "Tom Cruise"),
    ("I like Scarlett Johansson.", "current_actor", "Scarlett Johansson"),
    ("Tell me about Robert Downey Jr.", "current_actor", "Robert Downey Jr."),
    ("Who has worked with Emma Stone?", "current_actor", "Emma Stone"),

    # No explicit entity
    ("Who directed it?", None, None),
    ("What happens next?", None, None),
    ("Is it worth watching?", None, None),
    ("Who stars in that movie?", None, None),
    ("Can you explain the ending?", None, None),
]

REQUEST_DELAY = 5
MAX_RETRIES = 3
correct = 0
incorrect = 0
api_errors = 0
total = len(test_cases)

def extract_with_retry(message):
    """
    Extract entities using Gemini API.

    Retry when the API returns rate limit
    or temporary server errors.
    """
    for attempt in range(MAX_RETRIES):
        try:
            return extract_context(message)
        except Exception as error:
            error_text = str(error)
            is_retryable = (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
                or "503" in error_text
                or "UNAVAILABLE" in error_text
            )
            if not is_retryable:
                raise
            if attempt == MAX_RETRIES - 1:
                raise
            wait_time = 65
            print(
                f"API temporarily unavailable. "
                f"Waiting {wait_time} seconds...",
                flush=True
            )
            time.sleep(wait_time)

for index, (
    message,
    expected_field,
    expected_value
) in enumerate(test_cases, start=1):
    print(f"\nTest {index}/{total}")
    print(f"Message: {message}", flush=True)
    try:
        result = extract_with_retry(message)
        if expected_field is None:
            passed = all(
                result.get(field) is None
                for field in (
                    "current_movie",
                    "current_director",
                    "current_actor"
                )
            )
        else:
            passed = (
                result.get(expected_field)
                == expected_value
            )
        if passed:
            correct += 1
            print("Result: PASS")
        else:
            incorrect += 1
            print("Result: FAIL")
            print(
                f"Expected: {expected_field} "
                f"= {expected_value}"
            )
            print(f"Actual: {result}")
    except Exception as error:
        api_errors += 1
        print("Result: ERROR")
        print(f"Details: {error}")
    # Delay between API requests
    if index < total:
        print(
            f"Waiting {REQUEST_DELAY} seconds...",
            flush=True
        )
        time.sleep(REQUEST_DELAY)

evaluated = correct + incorrect
if evaluated > 0:
    accuracy = (correct / evaluated) * 100
else:
    accuracy = 0
completion_rate = (evaluated / total) * 100

print("\n=====================================")
print("CONTEXT EXTRACTION EVALUATION")
print("=====================================")
print(f"Total Tests     : {total}")
print(f"Evaluated       : {evaluated}")
print(f"Correct         : {correct}")
print(f"Incorrect       : {incorrect}")
print(f"API Errors      : {api_errors}")
print(f"Accuracy        : {accuracy:.2f}%")
print(f"Completion Rate : {completion_rate:.2f}%")
print("=====================================")
