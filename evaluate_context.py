from context_tracker import (
    create_empty_context,
    update_context
)

test_cases = [
    {
        "name": "Initial movie",
        "extracted": {
            "current_movie": "Interstellar",
            "current_director": None,
            "current_actor": None
        },
        "expected": {
            "current_movie": "Interstellar",
            "current_director": None,
            "current_actor": None
        }
    },
    {
        "name": "Add director",
        "extracted": {
            "current_movie": None,
            "current_director": "Christopher Nolan",
            "current_actor": None
        },
        "expected": {
            "current_movie": "Interstellar",
            "current_director": "Christopher Nolan",
            "current_actor": None
        }
    },
    {
        "name": "Add actor",
        "extracted": {
            "current_movie": None,
            "current_director": None,
            "current_actor": "Matthew McConaughey"
        },
        "expected": {
            "current_movie": "Interstellar",
            "current_director": "Christopher Nolan",
            "current_actor": "Matthew McConaughey"
        }
    },
    {
        "name": "Follow-up without entities",
        "extracted": {
            "current_movie": None,
            "current_director": None,
            "current_actor": None
        },
        "expected": {
            "current_movie": "Interstellar",
            "current_director": "Christopher Nolan",
            "current_actor": "Matthew McConaughey"
        }
    },
    {
        "name": "Switch movie to Titanic",
        "extracted": {
            "current_movie": "Titanic",
            "current_director": None,
            "current_actor": None
        },
        "expected": {
            "current_movie": "Titanic",
            "current_director": None,
            "current_actor": None
        }
    },
    {
        "name": "Add new director",
        "extracted": {
            "current_movie": None,
            "current_director": "James Cameron",
            "current_actor": None
        },
        "expected": {
            "current_movie": "Titanic",
            "current_director": "James Cameron",
            "current_actor": None
        }
    },
    {
        "name": "Switch movie to Avatar",
        "extracted": {
            "current_movie": "Avatar",
            "current_director": None,
            "current_actor": None
        },
        "expected": {
            "current_movie": "Avatar",
            "current_director": None,
            "current_actor": None
        }
    },
    {
        "name": "Retain current movie",
        "extracted": {
            "current_movie": None,
            "current_director": None,
            "current_actor": None
        },
        "expected": {
            "current_movie": "Avatar",
            "current_director": None,
            "current_actor": None
        }
    }
]

context = create_empty_context()
correct = 0
total = len(test_cases)
for index, test in enumerate(test_cases, start=1):
    print(f"\nTest {index}/{total}: {test['name']}")
    context = update_context(
        context,
        test["extracted"]
    )
    expected = test["expected"]
    if context == expected:
        correct += 1
        print("Result: PASS")
    else:
        print("Result: FAIL")
        print(f"Expected: {expected}")
        print(f"Actual: {context}")

accuracy = (correct / total) * 100
print("\n=====================================")
print("CONTEXT CONSISTENCY EVALUATION")
print("=====================================")
print(f"Total Tests : {total}")
print(f"Correct     : {correct}")
print(f"Incorrect   : {total - correct}")
print(f"Accuracy    : {accuracy:.2f}%")
print("=====================================")