from context_tracker import (
    create_empty_context,
    update_context
)

def test_initial_context():
    context = create_empty_context()
    assert context == {
        "current_movie": None,
        "current_director": None,
        "current_actor": None
    }

def test_movie_extraction_update():
    context = create_empty_context()
    extracted = {
        "current_movie": "Interstellar",
        "current_director": None,
        "current_actor": None
    }
    updated = update_context(context, extracted)
    assert updated["current_movie"] == "Interstellar"

def test_context_retention():
    context = {
        "current_movie": "Interstellar",
        "current_director": None,
        "current_actor": None
    }
    extracted = {
        "current_movie": None,
        "current_director": "Christopher Nolan",
        "current_actor": None
    }
    updated = update_context(context, extracted)
    assert updated["current_movie"] == "Interstellar"
    assert updated["current_director"] == "Christopher Nolan"

def test_topic_switching():
    context = {
        "current_movie": "Interstellar",
        "current_director": "Christopher Nolan",
        "current_actor": "Matthew McConaughey"
    }
    extracted = {
        "current_movie": "Titanic",
        "current_director": None,
        "current_actor": None
    }
    updated = update_context(context, extracted)
    assert updated["current_movie"] == "Titanic"
    assert updated["current_director"] is None
    assert updated["current_actor"] is None

def test_same_movie_keeps_context():
    context = {
        "current_movie": "Interstellar",
        "current_director": "Christopher Nolan",
        "current_actor": None
    }
    extracted = {
        "current_movie": "interstellar",
        "current_director": None,
        "current_actor": None
    }
    updated = update_context(context, extracted)
    assert updated["current_director"] == "Christopher Nolan"