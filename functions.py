from book import Book
from data import bookshelves, to_be_read

def book_exists(title, author):
    # Checks if a book with the given title and author already exists in either list
    for book in bookshelves:
        if book.title.lower() == title.lower() and book.author.lower() == author.lower():
            return True
    for book in to_be_read:
        if book.title.lower() == title.lower() and book.author.lower() == author.lower():
            return True
    return False

def add_new_book():
    book_title = input("Enter the book's title: ")
    book_author = input("Enter the book's author: ")

    if book_exists(book_title, book_author):
        print(f"Error: '{book_title}' by {book_author} already exists in your library!")
        return

    book_status = input("Have you read this? (Y/N)").lower() # Added .lower() here for consistency
    book_tropes_string = input("What are the tropes? (each new trope separated by '|' with no spaces) ")
    book_tropes_list = [trope.strip() for trope in book_tropes_string.split('|')] # Added .strip() to clean spaces

    if book_status == "y":
        stat = "read"
        while True:
            try:
                book_rating_str = input("Wonderful! How would you rate that adventure? (On a scale of 1-5): ")
                book_rating = float(book_rating_str)
                if 1 <= book_rating <= 5:
                    break
                else:
                    print("Please enter a rating between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        new_book = Book(book_title, book_author, rating=book_rating, tropes=book_tropes_list, status=stat)
        bookshelves.append(new_book)
        print(f"'{book_title}' by {book_author} has been added to your bookshelves with a rating of {book_rating} stars!")
    else:
        stat = "tbr"
        new_book = Book(book_title, book_author, tropes=book_tropes_list, status=stat)
        to_be_read.append(new_book)
        print(f"'{book_title}' by {book_author} has been added to your to-be-read shelf!")

