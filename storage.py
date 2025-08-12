# storage.py
import json

from book import Book
# Import the new dnf_books list
from data import bookshelf, to_be_read, dnf_books 

BOOKSHELF_FILE = "bookshelf.json"
TBR_FILE = "tbr.json"
DNF_FILE = "dnf.json" # <--- New file constant

def save_data():
    """Saves the current state of bookshelf, to_be_read, and dnf_books lists to JSON files."""
    print("DEBUG: Saving data...")

    # Convert bookshelf objects to dictionaries and save
    bookshelf_dicts = [book.to_dict() for book in bookshelf]
    with open(BOOKSHELF_FILE, 'w') as f:
        json.dump(bookshelf_dicts, f, indent=4)

    # Convert to_be_read objects to dictionaries and save
    tbr_dicts = [book.to_dict() for book in to_be_read]
    with open(TBR_FILE, 'w') as f:
        json.dump(tbr_dicts, f, indent=4)
    
    # <--- NEW: Convert dnf_books objects to dictionaries and save
    dnf_dicts = [book.to_dict() for book in dnf_books]
    with open(DNF_FILE, 'w') as f:
        json.dump(dnf_dicts, f, indent=4)

    print("DEBUG: Data saved successfully!")

def load_data():
    """Loads book data from JSON files into the bookshelf, to_be_read, and dnf_books lists."""
    print("DEBUG: Loading data...")

    # Clear current lists to avoid duplicates if loaded multiple times
    bookshelf.clear()
    to_be_read.clear()
    dnf_books.clear() # <--- NEW: Clear dnf_books

    # Load bookshelf data
    try:
        with open(BOOKSHELF_FILE, 'r') as f:
            bookshelf_dicts = json.load(f)
            for book_dict in bookshelf_dicts:
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
            for book_dict in tbr_dicts:
                to_be_read.append(Book(**book_dict))
        print(f"DEBUG: Loaded {len(to_be_read)} books into to-be-read.")
    except FileNotFoundError:
        print(f"DEBUG: {TBR_FILE} not found. Starting with empty to-be-read list.")
    except json.JSONDecodeError:
        print(f"DEBUG: Error reading {TBR_FILE}. File might be corrupted.")

    # <--- NEW: Load dnf_books data
    try:
        with open(DNF_FILE, 'r') as f:
            dnf_dicts = json.load(f)
            for book_dict in dnf_dicts:
                dnf_books.append(Book(**book_dict))
        print(f"DEBUG: Loaded {len(dnf_books)} books into DNF list.")
    except FileNotFoundError:
        print(f"DEBUG: {DNF_FILE} not found. Starting with empty DNF list.")
    except json.JSONDecodeError:
        print(f"DEBUG: Error reading {DNF_FILE}. File might be corrupted.")

    print("DEBUG: Data loading complete.")