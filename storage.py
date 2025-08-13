# storage.py
import json
import csv

from book import Book
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

def book_exists(title, author):
    # Checks if a book with the given title and author already exists in either list
    for book in bookshelf:
        if book.title.lower() == title.lower() and book.author.lower() == author.lower():
            return True
    for book in to_be_read:
        if book.title.lower() == title.lower() and book.author.lower() == author.lower():
            return True
    return False

def export_to_json():
    """Exports all books from the library to a single JSON file."""
    print("\n--- Exporting Library ---")
    export_filename = input("Enter filename for export (e.g., my_library.json): ")
    if not export_filename.endswith(".json"): # Ensure it's a JSON file
        export_filename += ".json"

    # Step 1: Combine all books into one list
    all_books_combined = bookshelf + to_be_read + dnf_books
    exported_book_dicts = [book.to_dict() for book in all_books_combined]
    try:
        with open(export_filename, 'w') as f:
            json.dump(exported_book_dicts, f, indent=4)
        print(f"Successcully exported {len(exported_book_dicts)} books to '{export_filename}'!\n")
    except Exception as e:
        print(f"Error exporting data: {e}\n")

def import_from_json():
    print("\n--- Importing Library ---")
    import_filename = input("Enter filename to import (e.g., my_library.json): ")
    if not import_filename.lower().endswith(".json"):
        import_filename += ".json"

    imported_books_count = 0
    skipped_duplicates_count = 0

    try:
        with open(import_filename, 'r') as f:
            imported_data = json.load(f)

        if not isinstance(imported_data, list):
            print(f"Error: '{import_filename}' does not contain a list of books.\n")
            return

        print(f"Attempting to import {len(imported_data)} books from '{import_filename}'.")
        for book_dict in imported_data:
            # Corrected: Accessing dictionary values with []
            if book_exists(book_dict.get('title'), book_dict.get('author')): # Using .get() for safety
                skipped_duplicates_count += 1
                print(f"Skipped duplicate: '{book_dict.get('title')}' by {book_dict.get('author')} already exists.\n")
                continue # Corrected: Continue to the next book, don't exit function
            else:
                # Corrected: Accessing dictionary values with [] for Book constructor
                new_book = Book(
                    title=book_dict.get('title'),
                    author=book_dict.get('author'),
                    rating=book_dict.get('rating'),
                    tropes=book_dict.get('tropes'),
                    status=book_dict.get('status'),
                    platform=book_dict.get('platform'),
                    length_value=book_dict.get('length_value'),
                    length_unit=book_dict.get('length_unit'),
                    dnf_reason=book_dict.get('dnf_reason')
                    )
                
                # Add new book to respective list based on its status
                if new_book.status == "read":
                    bookshelf.append(new_book)
                    print(f"Added: '{new_book.title}' by {new_book.author} to bookshelf.\n")
                elif new_book.status == "tbr":
                    to_be_read.append(new_book)
                    print(f"Added: '{new_book.title}' by {new_book.author} to to-be-read shelf.\n")
                elif new_book.status == "dnf":
                    dnf_books.append(new_book)
                    print(f"Added: '{new_book.title}' by {new_book.author} to DNF list.\n")
                else:
                    print(f"Warning: Book '{new_book.title}' has an unknown status '{new_book.status}' and was not added.\n")
                    continue
                
                imported_books_count += 1
        save_data()

    except FileNotFoundError:
        print(f"Error: File '{import_filename}' not found.\n")
    except json.JSONDecodeError:
        print(f"Error: Could not read '{import_filename}'. It might not be a valid JSON file.\n")
    except Exception as e:
        print(f"An unexpected error occurred during import: {e}\n")

    print(f"Successfully imported {imported_books_count} books.\nSkipped {skipped_duplicates_count} duplicates.\n")
    print(f"\n--- Your Library ---")
    print(f"Bookshelf now holds {len(bookshelf)} titles! Wow... you sure went on a lot of adventures!")
    print(f"TBR now has {len(to_be_read)} books.. Oof better get reading!")
    print(f"DNF Trashcan now has {len(dnf_books)}.")


def import_from_csv():
    # Imports books from a Goodreads CSV export file
    print("\n--- Importing from Goodreads CSV ---")
    import_filename = input("Enter the Goodreads CSV filename (e.g., goodreads_library.csv): ")
    if not import_filename.lower().endswith(".csv"):
        import_filename += ".csv"

    imported_count = 0
    skipped_count = 0

    try:
        with open(import_filename, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # --- CORRECTED: Adjust required_headers to match YOUR CSV ---
            required_headers = ["Title", "Author", "My Rating", "Exclusive Shelf", "Bookshelves", "My Review", "ISBN13"] # Added Bookshelves and ISBN13
            # You can decide which ones are truly "required" for your basic import logic
            
            if not all(header in reader.fieldnames for header in required_headers):
                print(f"Error: Missing one or more required headers in '{import_filename}'. "
                      f"Required: {', '.join(required_headers)}. Found: {', '.join(reader.fieldnames)}\n") # Added found headers for better debug
                return

            for row in reader:
                title = row.get("Title")
                author = row.get("Author")
                goodreads_rating_str = row.get("My Rating")
                
                # --- CORRECTED: Use "Exclusive Shelf" and "Bookshelves" ---
                exclusive_shelf = row.get("Exclusive Shelf") 
                goodreads_bookshelves_str = row.get("Bookshelves") # Use Bookshelves for custom shelves
                
                goodreads_review = row.get("My Review", "")
                
                # --- NEW: Get ISBN13 from the CSV ---
                isbn13_from_csv = row.get("ISBN13") # New field from your CSV
                isbn = None
                if isbn13_from_csv:
                    # Clean ISBN13 (remove quotes if present, sometimes CSVs wrap numbers in quotes)
                    isbn = isbn13_from_csv.replace('="', '').replace('"', '').strip() # Common fix for Excel-exported ISBNs
                    if not (len(isbn) == 13 and isbn.isdigit()): # Basic validation for ISBN13
                        isbn = None # Invalidate if not a clean ISBN13

                # Skip if essential data is missing
                if not title or not author:
                    print(f"Skipped a row due to missing Title or Author: {row.get('Title', 'N/A')} by {row.get('Author', 'N/A')}\n")
                    skipped_count += 1
                    continue

                # --- Map Goodreads data to your Book object attributes ---
                
                # Rating
                rating = None
                try:
                    if goodreads_rating_str and goodreads_rating_str.strip(): # Check if not empty string
                        rating = float(goodreads_rating_str)
                        if not (1 <= rating <= 5): # Ensure rating is within your range
                            rating = None 
                except ValueError:
                    rating = None # If conversion fails

                # Status and DNF Reason mapping
                status = "read" # Default status
                dnf_reason = None
                
                # Use Exclusive Shelf for primary status
                if exclusive_shelf and exclusive_shelf.strip().lower() == "to-read":
                    status = "tbr"
                elif exclusive_shelf and exclusive_shelf.strip().lower() == "currently-reading":
                    status = "tbr" # Map Goodreads 'currently-reading' to your 'tbr'
                
                # Check custom bookshelves for 'did-not-finish'
                custom_shelves_list = [s.strip().lower() for s in goodreads_bookshelves_str.split(',')] if goodreads_bookshelves_str else []
                
                if "did-not-finish" in custom_shelves_list: # Your custom DNF shelf
                    status = "dnf"
                    if goodreads_review.strip().lower().startswith("dnf reason:"):
                        dnf_reason = goodreads_review.strip()[len("dnf reason:"):].strip()
                    else:
                        dnf_reason = "No specific reason provided in Goodreads review (via custom shelf)."


                # If it's not explicitly 'to-read' or 'dnf' via shelves, it defaults to 'read'.
                # We can refine this later if 'Date Read' is used for 'read' status.


                # --- Check for duplicates and create/add book ---
                if book_exists(title, author):
                    skipped_count += 1
                    print(f"Skipped duplicate: '{title}' by {author} already exists in your library.\n")
                    continue # Move to the next book in the CSV
                else:
                    new_book = Book(
                        title=title,
                        author=author,
                        rating=rating,
                        tropes=[], # Ignored for import as per your decision
                        status=status,
                        platform=None, # Ignored for import
                        length_value=None, # Ignored for import
                        length_unit=None, # Ignored for import
                        dnf_reason=dnf_reason,
                        isbn=isbn # <--- Pass the extracted ISBN
                    )
                    
                    # Add new book to respective list based on its status
                    if new_book.status == "read":
                        bookshelf.append(new_book)
                        print(f"Imported: '{new_book.title}' by {new_book.author} to bookshelf.\n")
                    elif new_book.status == "tbr":
                        to_be_read.append(new_book)
                        print(f"Imported: '{new_book.title}' by {new_book.author} to to-be-read shelf.\n")
                    elif new_book.status == "dnf":
                        dnf_books.append(new_book)
                        print(f"Imported: '{new_book.title}' by {new_book.author} to DNF list.\n")
                    else:
                        print(f"Warning: Book '{new_book.title}' by {new_book.author} has an unknown status '{new_book.status}' and was not imported.\n")
                        continue # Skip counting if status is unknown
                    
                    imported_count += 1
        
        save_data() # Save all changes after import is complete

    except FileNotFoundError:
        print(f"Error: File '{import_filename}' not found.\n")
    except csv.Error as e: # Catch specific CSV errors
        print(f"Error reading CSV file '{import_filename}': {e}\n")
    except json.JSONDecodeError: # Should not happen with csv.DictReader, but good to keep
        print(f"Error: Could not read '{import_filename}'. It might not be a valid JSON/CSV file.\n")
    except Exception as e:
        print(f"An unexpected error occurred during import: {e}\n")

    print(f"\n--- Import Summary ---")
    print(f"Successfully imported {imported_count} books.")
    print(f"Skipped {skipped_count} duplicates or invalid entries.")
    print(f"\n--- Your Current Library Totals ---")
    print(f"Bookshelf: {len(bookshelf)} titles")
    print(f"TBR: {len(to_be_read)} titles")



def export_to_csv(): # Remember to update the function name in storage.py if it's export_to_goodreads_csv
    """Exports all books from the library to a Goodreads-compatible CSV file."""
    print("\n--- Exporting to Goodreads CSV ---")
    export_filename = input("Enter filename for Goodreads export (e.g., my_goodreads_export.csv): ")
    if not export_filename.lower().endswith(".csv"):
        export_filename += ".csv"

    goodreads_fieldnames = [
        "Title", "Author", "ISBN", "My Rating", "Average Rating", "Publisher", 
        "Binding", "Year Published", "Original Publication Year", "Date Read", 
        "Date Added", "Shelves", "Bookshelves", "My Review"
    ]

    all_books_for_export = bookshelf + to_be_read + dnf_books
    exported_rows = [] 

    for book in all_books_for_export:
        row_data = {
            "Title": book.title,
            "Author": book.author,
            "ISBN": "",
            "My Rating": book.rating if book.status == "read" and book.rating is not None else "",
            "Average Rating": "",
            "Publisher": "",
            "Binding": "",
            "Year Published": "",
            "Original Publication Year": "",
            "Date Read": "",
            "Date Added": "",
            "Shelves": "", # Initialize as empty string
            "Bookshelves": "", # Initialize as empty string (as per your choice to ignore tropes)
            "My Review": "" # Initialize as empty string for safety
        }
        
        # Specific logic for mapping status, dnf_reason to Shelves/My Review
        if book.status == "read":
            row_data["Shelves"] = "" 
        elif book.status == "tbr":
            row_data["Shelves"] = "to-read"
        elif book.status == "dnf":
            row_data["Shelves"] = "did-not-finish" # Your custom DNF shelf
            if book.dnf_reason:
                row_data["My Review"] = f"DNF Reason: {book.dnf_reason}"

        exported_rows.append(row_data)

    # --- NEW: Write 'exported_rows' to the CSV file using csv.DictWriter ---
    try:
        with open(export_filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=goodreads_fieldnames)
            writer.writeheader() # Write the first row with column names
            writer.writerows(exported_rows) # Write all the data rows
        print(f"Successfully exported {len(exported_rows)} books to '{export_filename}'.\n")
    except Exception as e:
        print(f"Error exporting data: {e}\n")