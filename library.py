# main.py (or library.py)
# Import functions from your functions file
from functions import add_new_book, update_book, view_tbr, view_bookshelf, searching, delete, view_dnf
from storage import * # This will import all the functions you've defined in storage.py

def display_menu():
    print("--- Library Menu ---\n")
    print("1. Modify Library")
    print("2. View Library")
    print("3. Search for a book")
    print("4. Import/Export")
    print("5. Exit program") # Corrected: Now 5 options
    print("--------------------------")

def modify_menu():
    print("--- Modify Library Menu ---\n")
    print("1. Add a new book")
    print("2. Update book details")
    print("3. Delete an entry")
    print("4. Exit to main menu") # This option now correctly breaks from its sub-menu loop
    print("--------------------------")

def view_menu():
    print("--- View Library Menu ---\n")
    print("1. View TBR")
    print("2. View Bookshelf")
    print("3. View DNF Trashcan")
    print("4. Exit to main menu") # This option now correctly breaks from its sub-menu loop
    print("--------------------------")

def import_menu():
    print("--- Import/Export Menu ---\n")
    print("1. Import CSV")
    print("2. Export CSV")
    print("3. Import JSON")
    print("4. Export JSON")
    print("5. Exit to main menu") # This option now correctly breaks from its sub-menu loop
    print("--------------------------")

# --- NEW HELPER FUNCTIONS FOR SUB-MENUS ---
def handle_modify_menu_actions():
    while True: # This loop keeps the modify options active until user exits
        modify_menu()
        modify_choice = input("Enter your choice (1-4):\n") # Added newline for clarity
        if modify_choice == '1':
            print("You chose to add a book!")
            add_new_book()
        elif modify_choice == '2':
            print("You chose to update a book!")
            update_book()
        elif modify_choice == '3':
            print("You chose to delete a book!")
            delete()
        elif modify_choice == '4':
            print("Returning to main menu!")
            break # Breaks THIS 'while True' loop, returning to library_lobby
        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n") # Added newline

def handle_view_menu_actions():
    while True: # Keep showing view options until user chooses to exit
        view_menu()
        view_choice = input("Enter your choice (1-4):\n") # Added newline for clarity
        if view_choice == '1':
            print("You chose to view your TBR!")
            view_tbr()
        elif view_choice == '2':
            print("You chose to view your Bookshelf!")
            view_bookshelf()
        elif view_choice == '3':
            print("You chose to view your DNF Trashcan!")
            view_dnf()
        elif view_choice == '4':
            print("Returning to main menu!")
            break # Breaks THIS 'while True' loop, returning to library_lobby
        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n") # Added newline

def handle_import_menu_actions():
    while True:
        import_menu() # <--- Correctly calls import_menu
        import_choice = input("Enter your choice (1-5):\n") # Corrected: 1-5 for this menu
        if import_choice == '1':
            print("You chose to import a .csv (Goodreads format)!")
            import_from_csv() # <--- Corrected function call
        elif import_choice == '2':
            print("You chose to export your library as a .csv (Goodreads format)!")
            export_to_csv() # <--- Corrected function call
        elif import_choice == '3':
            print("You chose to import a .json (Boot.dev format)! This will replace your current library.\n") # Added warning
            # load_data() from storage.py is for the main program's auto-load.
            # import_from_json() is the one that imports a new file and replaces.
            import_from_json() # <--- Corrected function call
        elif import_choice == '4':
            print("You chose to export your library as a .json (Boot.dev format)!")
            export_to_json() # <--- Corrected function call
        elif import_choice == '5':
            print("Returning to main menu!\n")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")

# --- MAIN PROGRAM LOBBY ---
def library_lobby():
    load_data() # Load data once at the start
    while True: # This main loop keeps the program running until explicitly exited
        display_menu()
        # Corrected: Main menu now has 5 options
        choice = input("Enter your choice (1-5): ") 

        if choice == '1':
            print("You chose to modify your library!")
            handle_modify_menu_actions()
        elif choice == '2':
            print("You chose to view your library!")
            handle_view_menu_actions()
        elif choice == '3':
            print("You chose to search for a book!")
            searching()
        elif choice == '4': # This is the "Import/Export" option
            print("You chose to import/export!")
            handle_import_menu_actions() # Call the new helper function for import/export
        elif choice == '5': # This is the "Exit program" option
            save_data() # Save data when exiting the program
            print("Farewell, mighty librarian! May your reading adventures be grand!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n") # Corrected: 1-5 for main menu

if __name__ == "__main__":
    library_lobby()