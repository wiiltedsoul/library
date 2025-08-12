from book import Book
from data import bookshelf, to_be_read

def book_exists(title, author):
    # Checks if a book with the given title and author already exists in either list
    for book in bookshelf:
        if book.title.lower() == title.lower() and book.author.lower() == author.lower():
            return True
    for book in to_be_read:
        if book.title.lower() == title.lower() and book.author.lower() == author.lower():
            return True
    return False

def add_new_book():
    book_title = input("Enter the book's title:\n")
    book_author = input("Enter the book's author:\n")

    if book_exists(book_title, book_author):
        print(f"Error: '{book_title}' by {book_author} already exists in your library!\n")
        return
    book_tropes_string = input("What are the tropes? (each new trope separated by '|' with no spaces)\n")
    book_status = input("Have you read this? (Y/N)\n").lower() # Added .lower() here for consistency
    book_tropes_list = [trope.strip() for trope in book_tropes_string.split('|')] # Added .strip() to clean spaces

    if book_status == "y":
        stat = "read"
        while True:
            try:
                book_rating_str = input("Wonderful! How would you rate that adventure? (On a scale of 1-5)\n")
                book_rating = float(book_rating_str)
                if 1 <= book_rating <= 5:
                    break
                else:
                    print("Please enter a rating between 1 and 5.\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")
        new_book = Book(book_title, book_author, rating=book_rating, tropes=book_tropes_list, status=stat)
        bookshelf.append(new_book)
        print(f"'{book_title}' by {book_author} has been added to your bookshelves with a rating of {book_rating} stars!\n")
    else:
        stat = "tbr"
        book_platform = input("Where can you read this book?\n")
        new_book = Book(book_title, book_author, tropes=book_tropes_list, status=stat, platform=book_platform)
        to_be_read.append(new_book)
        print(f"'{book_title}' by {book_author} has been added to your to-be-read shelf! Don't forget to read it on {book_platform}!\n")

def view_bookshelf():
    if not bookshelf:
        print("\nYour Bookshelves are looking a bit dusty... Time to read some more!\n")
        return
    
    print("\n--- Your Bookshelf ---")
    for book in bookshelf:
        print(f"{book.title} by {book.author}")
        if book.rating is not None:
            print(f"Rating: {book.rating} / 5")
        
        if book.tropes:
            print(f"Tropes: {', '.join(book.tropes)}")
        else:
            print("You haven't listed any tropes for this book :(")
        print("--------------------")

def view_tbr():
    if not to_be_read:
        print("\nYour tbr is looking a bit dusty... go explore tiktok or reels!")
        return
    
    print("\n--- Your TBR Shelf ---")
    for book in to_be_read:
        print(f"{book.title} by {book.author}. [{book.platform}]")        
        if book.tropes:
            print(f"Tropes: {', '.join(book.tropes)}")
        else:
            print("You haven't listed any tropes for this book :(")
        print("--------------------")