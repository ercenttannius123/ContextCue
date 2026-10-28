from context_extractor import extract_context
test_messages = [
    "Tell me about Interstellar.",
    "Who directed it?",
    "I like Christopher Nolan.",
    "What movies feature Leonardo DiCaprio?"
]
for message in test_messages:
    print("\nUser:", message)
    try:
        result = extract_context(message)
        print("Extracted:", result)
    except Exception as error:
        print("Error:", error)
