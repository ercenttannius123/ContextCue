def create_empty_context():
    """
    Membuat struktur konteks awal untuk percakapan baru.
    """
    return {
        "current_movie": None,
        "current_director": None,
        "current_actor": None
    }

def format_context(context):
    """
    Mengubah dictionary konteks menjadi teks
    yang dapat diberikan kepada LLM.
    """
    movie = context.get("current_movie")
    director = context.get("current_director")
    actor = context.get("current_actor")
    return f"""
Current conversation context:
- Movie: {movie or 'Unknown'}
- Director: {director or 'Unknown'}
- Actor: {actor or 'Unknown'}
Use this context only when relevant.
If the context is missing or uncertain,
refer to the conversation history.
"""


def update_context(context, extracted_context):
    """
    Update konteks berdasarkan entitas baru.
    Jika pengguna menyebut film baru,
    hapus director dan actor dari konteks lama.
    """
    updated_context = context.copy()
    new_movie = extracted_context.get("current_movie")
    old_movie = updated_context.get("current_movie")
    # Deteksi pergantian film
    if new_movie is not None:
        if (
            old_movie is not None
            and new_movie.strip().casefold()
            != old_movie.strip().casefold()
        ):
            updated_context["current_director"] = None
            updated_context["current_actor"] = None
    # Gabungkan entitas baru
    for key in updated_context:
        new_value = extracted_context.get(key)
        if new_value is not None:
            updated_context[key] = new_value
    return updated_context