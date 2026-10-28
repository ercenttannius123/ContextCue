
from context_tracker import (
    create_empty_context,
    format_context,
    update_context
)

# Membuat konteks awal
context = create_empty_context()

print("Konteks awal:")
print(context)

# Simulasi informasi dari pesan pertama
extracted_1 = {
    "current_movie": "Interstellar",
    "current_director": None,
    "current_actor": None
}

context = update_context(context, extracted_1)

print("\nSetelah pesan pertama:")
print(context)

# Simulasi informasi dari pesan kedua
extracted_2 = {
    "current_movie": None,
    "current_director": "Christopher Nolan",
    "current_actor": None
}

context = update_context(context, extracted_2)

print("\nSetelah pesan kedua:")
print(context)

print("\nFormatted context:")
print(format_context(context))
