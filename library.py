# main.py (or library.py)
# Import functions from your functions file
from functions import add_new_book, update_book, view_tbr, view_bookshelf, searching # and other functions like update_book_status, etc.
from storage import save_data, load_data

def display_menu():
    print("--- Library Menu ---\n")
    print("1. Add a new book")
    print("2. Update book details")
    print("3. View TBR Shelf")
    print("4. View Bookshelf")
    print("5. Search for a book")
    print("6. Exit program")
    print("--------------------------")


def library_lobby():
    load_data()
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            print("You chose to add a book!")
            add_new_book()
        elif choice == '2':
            print("You chose to update a book!")
            update_book()
        elif choice == '3':
            print("You chose to view your TBR Shelf!")
            view_tbr()
        elif choice == '4':
            print("You chose to view your Bookshelf!")
            view_bookshelf()
        elif choice == '5':
            print("You chose to search for a book!")
            searching()
        elif choice == '6':
            save_data()
            print("Farewell, mighty librarian! May your reading adventures be grand!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    library_lobby()