class Book:
    def __init__(self, title, author, rating=None, tropes=None, status=None):
        self.title = title
        self.author = author
        self.rating = rating
        self.tropes = tropes if tropes is not None else []
        self.status = status

bookshelves = []
to_be_read = []

def add_new_book():
    book_title = input("What's this magical book called?\n") # Get book title
    book_author = input("Who is the Author?\n") # Get book author
    book_tropes_string = input("What are the tropes? (each new trope separated by '|' with no spaces)\n") # Get book tropes
    # First, split the string into a list
    book_tropes_list = book_tropes_string.split('|')

    
    book_status = input("Have you read this? (Y/N)\n") # Get read or tbr status
    # if read, status is read and book rating is asked
    if book_status.upper() == "Y":
        stat = "read"
        while True:
            try:
                book_rating_str = input("Wonderful! How would you rate that adventure? (On a scale of 1-5)\n")
                book_rating = float(book_rating_str)
                if 1 <= book_rating <= 5:
                    break # Exit loop if input is valid
                else:
                    print("Please enter a rating between 1 and 5.\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")
        new_book = Book(book_title, book_author, rating=book_rating, tropes=book_tropes_list, status=stat)
        bookshelves.append(new_book)
        print(f"'{book_title}' by {book_author} has been added to your bookshelves with a rating of {book_rating} stars!")

    # is not read, book is added to tbr
    else:
        stat = "tbr"
        new_book = Book(book_title, book_author, tropes=book_tropes_list, status=stat) 
        to_be_read.append(new_book)
        print(f"'{book_title}' by {book_author} has been added to your to-be-read shelf!")

def display_menu():
    """Prints the main menu options to the user."""
    print("\n--- Library Menu ---")
    print("1. Add a new book")
    print("2. Update book details")
    print("3. View TBR Shelf")
    print("4. View Bookshelf")
    print("5. Search for a book")
    print("6. Exit program")
    print("--------------------------")

def library_lobby():
    """Manages the main flow of the program."""
    while True: # This loop keeps the program running until explicitly told to stop
        display_menu() # Show the user their options
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            print("You chose to add a book!")
            # Call the function to add a book (you're already working on this!)
            add_new_book()
        elif choice == '2':
            print("You chose to update a book!")
            # Call the function to update book details (like the one we discussed)
            # update_book_status()
        elif choice == '3':
            print("You chose to view your TBR Shelf!")
            # You'll need a new function here to display books with status "plan_to_read"
        elif choice == '4':
            print("You chose to view your Bookshelves!")
            # You'll need a new function here to display books with status "plan_to_read"
        elif choice == '5':
            print("You chose to search for a book!")
            # You'll need a new function here for searching
        elif choice == '6':
            print("Farewell, mighty librarian! May your reading adventures be grand!")
            break # This breaks out of the while True loop, ending the program
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# To run your program, you would simply call your main loop function:
library_lobby()