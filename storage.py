# storage.py
import json

from book import Book
from data import bookshelf, to_be_read # We still need these to put the loaded books into

BOOKSHELF_FILE = "bookshelf.json"
TBR_FILE = "tbr.json"

def save_data():
    """Saves the current state of bookshelf and to_be_read lists to JSON files."""
    print("DEBUG: Saving data...")

    bookshelf_dicts = [book.to_dict() for book in bookshelf]
    with open(BOOKSHELF_FILE, 'w') as f:
        json.dump(bookshelf_dicts, f, indent=4)

    tbr_dicts = [book.to_dict() for book in to_be_read]
    with open(TBR_FILE, 'w') as f:
        json.dump(tbr_dicts, f, indent=4)

    print("DEBUG: Data saved successfully!")

def load_data():
    """Loads book data from JSON files into the bookshelf and to_be_read lists."""
    print("DEBUG: Loading data...")

    # Clear current lists to avoid duplicates if loaded multiple times
    bookshelf.clear()
    to_be_read.clear()

    # Load bookshelf data
    try:
        with open(BOOKSHELF_FILE, 'r') as f:
            bookshelf_dicts = json.load(f)
            # Reconstruct Book objects from dictionaries
            for book_dict in bookshelf_dicts:
                # Use a dictionary unpacking trick (**) to pass dict items as kwargs
                bookshelf.append(Book(**book_dict))
        print(f"DEBUG: Loaded {len(bookshelf)} books into bookshelf.")
    except FileNotFoundError:
        print(f"DEBUG: {BOOKSHELF_FILE} not found. Starting with empty bookshelf.")
    except json.JSONDecodeError:
        print(f"DEBUG: Error reading {BOOKSHELF_FILE}. File might be corrupted.")

    # Load to_be_read data
    try:
        with open(TBR_FILE, 'r') as f:
            tbr_dicts = json.load(f)
            # Reconstruct Book objects from dictionaries
            for book_dict in tbr_dicts:
                to_be_read.append(Book(**book_dict))
        print(f"DEBUG: Loaded {len(to_be_read)} books into to-be-read.")
    except FileNotFoundError:
        print(f"DEBUG: {TBR_FILE} not found. Starting with empty to-be-read list.")
    except json.JSONDecodeError:
        print(f"DEBUG: Error reading {TBR_FILE}. File might be corrupted.")

    print("DEBUG: Data loading complete.")