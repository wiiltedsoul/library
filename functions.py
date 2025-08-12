from book import Book
from data import bookshelf, to_be_read
from storage import save_data

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

    # --- INPUT VALIDATION FOR LENGTH ---
    book_length = None
    book_len_unit = None

    while True: # Loop for length value
        try:
            book_length_str = input("How many pages/hours is this book? (e.g., 300 or 10.5)\n")
            book_length = float(book_length_str)
            if book_length > 0: # Ensure length is positive
                break
            else:
                print("Length must be a positive number.\n")
        except ValueError:
            print("Invalid input. Please enter a number for length.\n")

    while True: # Loop for length unit
        book_len_unit = input("Are we tracking this book in hrs or pgs? (hrs/pgs)\n").lower()
        if book_len_unit in ["hrs", "pgs"]:
            break
        else:
            print("Invalid unit. Please enter 'hrs' or 'pgs'.\n")
    # --- END INPUT VALIDATION FOR LENGTH ---

    book_tropes_string = input("What are the tropes? (each new trope separated by '|' with no spaces)\n")
    book_tropes_list = [trope.strip() for trope in book_tropes_string.split('|') if trope.strip()]
    book_status = input("Have you read this book? (Y/N)\n").lower()

    # Initialize rating and platform to None
    book_rating = None
    book_platform = None

    if book_status == "y":
        stat = "read"
        while True: # Loop for rating
            try:
                book_rating_str = input("Wonderful! How would you rate that adventure? (On a scale of 1-5)\n")
                book_rating = float(book_rating_str)
                if 1 <= book_rating <= 5:
                    break
                else:
                    print("Please enter a rating between 1 and 5.\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")
    else: # if book_status == "n" (tbr)
        stat = "tbr"
        book_platform = input("Where can you read/listen to this book?\n")
        # No rating for TBR books, so book_rating remains None

    # --- Create the new Book object, passing ALL collected attributes ---
    new_book = Book(
        title=book_title,
        author=book_author,
        rating=book_rating,
        tropes=book_tropes_list,
        status=stat,
        platform=book_platform,
        length_value=book_length,
        length_unit=book_len_unit
    )

    if stat == "read":
        bookshelf.append(new_book)
        print(f"'{book_title}' by {book_author} ({new_book.length_value} {new_book.length_unit}) has been added to your bookshelves with a rating of {new_book.rating} stars!\n")
    else: # stat == "tbr"
        to_be_read.append(new_book)
        print(f"'{book_title}' by {book_author} ({new_book.length_value} {new_book.length_unit}) has been added to your to-be-read shelf! Don't forget to read it on {new_book.platform}!\n")
    
    save_data()

def view_bookshelf():
    if not bookshelf:
        print("\nYour Bookshelves are looking a bit dusty... Time to read some more!\n")
        return
    
    print("\n--- Your Bookshelf ---")
    for book in bookshelf:
        print(f"{book.title} by {book.author}")
        print(f"{book.length_value}{book.length_unit}")
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
        print(f"{book.length_value}{book.length_unit}")
        if book.tropes:
            print(f"Tropes: {', '.join(book.tropes)}")
        else:
            print("You haven't listed any tropes for this book :(")
        print("--------------------")

def update_book():
    """Allows the user to find a book and update its details."""
    book_to_update = find_book_update() # Call our helper to get the book object

    if book_to_update is None:
        # The helper function already printed a message if not found, so we just return.
        return

    # If we reached here, book_to_update holds the actual Book object.
    print(f"\n--- Updating: {book_to_update.title} by {book_to_update.author} ---")
    print("What would you like to update?")
    print("1. Title")
    print("2. Author")
    print("3. Rating (for read books)")
    print("4. Tropes")
    print("5. Status (Read / To Be Read)")
    print("6. Platform (for TBR books)")
    print("7. Go back to main menu")
    
    update_choice = input("Enter your choice (1-7): ")

    # update title
    if update_choice == '1':
        new_title = input("What would you like the new title to be?\n")
        book_to_update.title = new_title
        print(f"Book title updated to: {book_to_update.title}")
        save_data()

    # update author
    elif update_choice == '2':
        new_author = input("Oh, okay. Who is the book by then?\n")
        book_to_update.author = new_author
        print(f"You've successfully changed the author to {book_to_update.author}!")
        save_data()

    # update rating
    elif update_choice == '3':
        if book_to_update in bookshelf:
            while True:
                try:
                    updated_rating_str = input("Changed your mind? That's fine! What's the new rating? (On a scale of 1-5)\n")
                    new_book_rating = float(updated_rating_str)
                    if 1 <= new_book_rating <= 5:
                        break
                    else:
                        print("Please enter a rating between 1 and 5.\n")
                except ValueError:
                    print("Invalid input. Please enter a number.\n")
            book_to_update.rating = new_book_rating
            print(f"You've changed your rating to {book_to_update.rating}.")
        else:
            print(f"Sorry you can't rate something you haven't read!")
        save_data()

    # update tropes
    elif update_choice == '4':
        new_tropes_str = input("Oh, did you forget these? That's okay, what's the tropes? (each new trope separated by '|' with no spaces)\n")
        book_to_update.tropes = [trope.strip() for trope in new_tropes_str.split('|') if trope.strip()]
        print(f"The tropes are now {', '.join(book_to_update.tropes) if book_to_update.tropes else 'None listed'}")
        save_data()

    # change shelf
    elif update_choice == '5':
        # Scenario 1: Book is currently on the To Be Read shelf (moving to Read)
        if book_to_update.status == "tbr": # More robust check for current status
            print("OOO A new book under your belt!? Nice!\n")
            # Remove from TBR and add to Bookshelf
            to_be_read.remove(book_to_update) # Remove from its old list
            bookshelf.append(book_to_update)  # Add to its new list
            book_to_update.status = "read"    # Update the book's status attribute
            print(f"Awesome! I've moved '{book_to_update.title}' by {book_to_update.author} over to your bookshelf!")
            # Prompt for rating (your existing robust code)
            while True:
                try:
                    new_rating_str = input("Let's rate it! How'd you like this new adventure? (On a scale of 1-5)\n")
                    new_rating = float(new_rating_str)
                    if 1 <= new_rating <= 5:
                        break
                    else:
                        print("Please enter a rating between 1 and 5.\n")
                except ValueError:
                    print("Invalid input. Please enter a number.\n")
            book_to_update.rating = new_rating # Assign the valid rating
            print(f"I set the rating of '{book_to_update.title}' to {book_to_update.rating} stars!")

        # Scenario 2: Book is currently on the Bookshelf (moving to To Be Read)
        elif book_to_update.status == "read": # Check if it's currently read
            to_tbr_confirm = input(f"Oop, you said you already read {book_to_update.title}... do you need to fix this? (Y/N)").lower()
            # if yes
            if to_tbr_confirm == "y":
                # Remove from Bookshelf and add to TBR
                bookshelf.remove(book_to_update) # Remove from its old list
                to_be_read.append(book_to_update)  # Add to its new list
                book_to_update.status = "tbr"     # Update the book's status attribute
                book_to_update.rating = None      # Clear the rating
                new_plat_ask = input("Oh! Now that it's on your tbr did you want to set what platform it's available on? (Y/N)").lower()
                if new_plat_ask == "y":
                    new_plat = input("Awesome, where can it be read?")
                    book_to_update.platform = new_plat
                    print(f"Awesome! So not only did I move {book_to_update.title} over to your tbr, I also added {book_to_update.platform} as the available platform!\n")
            else:
                print("Oop, gotchya. See ya later!")
                return
        save_data()

    # update plaform
    elif update_choice == '6':
        if book_to_update in to_be_read:
            new_platform = input("Okay, what's the new plaform?\n")
            book_to_update.platform = new_platform
            print(f"{book_to_update.title}'s new platform is {book_to_update.platform}.")
        else:
            print("Sorry this is only for books you haven't read yet!")
        save_data()

    # exit to main menu
    elif update_choice == '7':
        print(f"Gotchya! Sorry to bother you, sending you back to main menu!")
        return
    else:
        print("Invalid choice! Please enter a number between 1 and 7.")
    

def find_book_update():
# Prompts user for book details and returns the Book object if found, else None
    search_title = input("Enter the title of the book you're looking for: ")
    search_author = input("Enter the author of the book you're looking for: ")
    found_book = None # Initialize to None

    # Search in bookshelf
    for book in bookshelf:
        if book.title.lower() == search_title.lower() and \
           book.author.lower() == search_author.lower():
            found_book = book
            print(f"DEBUG: Found '{book.title}' in bookshelf.")
            return found_book # Return the actual book object and exit

    # Search in to_be_read
    for book in to_be_read:
        if book.title.lower() == search_title.lower() and \
           book.author.lower() == search_author.lower():
            found_book = book
            print(f"DEBUG: Found '{book.title}' in to-be-read shelf.")
            return found_book # Return the actual book object and exit

    print(f"Book '{search_title}' by {search_author}' not found in your library, maybe double check spelling?")
    return None # If we get here, no book was found

def searching():
    user_choice = input("What are we looking for, trope(s) or a specific book? (trope or book)\n").lower()

    if user_choice == "book":
        find_book_title = input("Gotchya, what's the name of the book?\n")
        find_author = input("And who's the author?\n")

        all_books = bookshelf + to_be_read
        search_results_book = [] # Renamed for clarity in this branch

        for book in all_books:
            if book.title.lower() == find_book_title.lower() and \
               book.author.lower() == find_author.lower():
                search_results_book.append(book)

        print(f"Found {len(search_results_book)} matching books.") # This prints once now
        
        if search_results_book:
            print("\n--- Search Results ---")
            for book in search_results_book: # This loop processes EACH found book
                print(f"{book.title} by {book.author}")
                print(f"{book.length_value}{book.length_unit}")
                
                if book.status == "read":
                    if book.rating is not None:
                        print(f"Rating: {book.rating} / 5")
                elif book.status == "tbr":
                    if book.platform is not None:
                        print(f"Platform: {book.platform}")
                
                if book.tropes:
                    print(f"Tropes: {', '.join(book.tropes)}")
                else:
                    print("You haven't listed any tropes for this book :(")
                print("--------------------")
        else:
            print("No books found matching your criteria.")

    elif user_choice == "trope":
        find_trope_query = input("Gotchya, what trope are you looking for?\n").lower()

        all_books = bookshelf + to_be_read
        matching_books_trope = [] # Renamed for clarity in this branch

        for book in all_books:
            for trope_item in book.tropes: # Changed 'trope' to 'trope_item' to avoid name collision
                if trope_item.lower() == find_trope_query:
                    matching_books_trope.append(book)
                    break # Found the trope in this book, move to the next book

        # --- Display results for the 'trope' search, OUTSIDE both loops ---
        print(f"Found {len(matching_books_trope)} matching books with the trope '{find_trope_query}'.")
        
        if matching_books_trope: # This condition now correctly uses 'matching_books_trope'
            print("\n--- Search Results ---")
            for book in matching_books_trope: # This loop processes EACH found book for trope
                print(f"{book.title} by {book.author}")
                print(f"{book.length_value}{book.length_unit}")
                
                if book.status == "read":
                    if book.rating is not None:
                        print(f"Rating: {book.rating} / 5")
                elif book.status == "tbr":
                    if book.platform is not None:
                        print(f"Platform: {book.platform}")
                
                if book.tropes:
                    print(f"Tropes: {', '.join(book.tropes)}")
                else:
                    print("You haven't listed any tropes for this book :(")
                print("--------------------")
        else:
            print("No books found with that trope.")
    # Add an else block for invalid user_choice, just like in previous examples
    else:
        print("Invalid search type. Please choose 'trope' or 'book'.")

def delete():
    book_to_delete = find_book_update() # Renamed to match your helper function and be clearer

    if book_to_delete is None: # If the book wasn't found by the helper, just exit
        return

    delete_confirm = input(f"Is '{book_to_delete.title}' by {book_to_delete.author} the book you're trying to delete? (Y/N)\n").lower() # Fixed f-string and added newline

    if delete_confirm == "y":
        # Check which list it's in and remove it
        if book_to_delete in bookshelf:
            bookshelf.remove(book_to_delete)
            print(f"Awh, sad to see '{book_to_delete.title}' go! It has been removed from your bookshelf.\n")
        elif book_to_delete in to_be_read: # Use elif to ensure only one list is checked if it's found in the first
            to_be_read.remove(book_to_delete)
            print(f"Awh, sad to see '{book_to_delete.title}' go! It has been removed from your to-be-read shelf.\n")
        else:
            # This 'else' should theoretically not be hit if find_book_for_update works,
            # but it's good for robustness.
            print(f"Error: '{book_to_delete.title}' not found in either list, despite initial search.")
            return # Exit if somehow not found

        save_data() # Save ONLY if a deletion actually occurred and was confirmed
    else:
        print("Oop, gotchya. See ya later!")
        return
    
def filter_menu():
    print("--- Filtering Options ---\n")
    print("1. By Status")
    print("2. By Rating")
    print("3. By Platform")
    print("4. By Specific Tropes")
    print("5. Return to main menu")
    print("--------------------------")

def sorting_menu():
    print("--- Sorting Options ---\n")
    print("1. By Title")
    print("2. By Author")
    print("3. By Rating")
    print("4. By Page No.")
    print("5. Return to main menu")
    print("--------------------------")

# (Your filter_menu() and sorting_menu() functions would be here in functions.py)

def filter_and_sort_books():
    # Allows the user to filter or sort their library.
    while True: # This loop keeps the filter/sort menu active until user exits
        print("\n--- Filter & Sort Menu ---")
        print("1. Filter books")
        print("2. Sort books")
        print("3. Return to main menu")
        print("--------------------------")

        main_choice = input("Enter your choice (1-3):\n")

        if main_choice == '1':
            filter_menu() # Display filtering options
            filter_choice = input("Enter your filtering preference (1-5):\n") # <--- NOW get the specific choice
            
            # --- We'll put the filtering logic here ---
            if filter_choice == '1':
                print("You chose to filter by Status!")
                status_choice = input("Do you want to see books you've read or books on your tbr? (read/tbr)\n").lower() # Clarified prompt

                filtered_books = [] # A new list to collect all books that match the filter

                if status_choice == "read":
                    for book in bookshelf: # Iterate only bookshelf, since read books are there
                        if book.status == "read": # Redundant, but ensures correctness if data inconsistencies
                            filtered_books.append(book)
                    print(f"\n--- Books Read ({len(filtered_books)}) ---")
                elif status_choice == "tbr":
                    for book in to_be_read: # Iterate only tbr, since tbr books are there
                        if book.status == "tbr": # Redundant, but ensures correctness
                            filtered_books.append(book)
                    print(f"\n--- Books To Be Read ({len(filtered_books)}) ---")
                else:
                    print("Invalid status choice. Please enter 'read' or 'tbr'.")
                    continue # Go back to the Filter & Sort main menu

                # --- Display the collected filtered books ---
                if filtered_books:
                    for book in filtered_books:
                        print(f"{book.title} by {book.author}")
                        print(f"{book.length_value}{book.length_unit}")
                        if book.status == "read": # Display rating only for read books
                            if book.rating is not None:
                                print(f"Rating: {book.rating} / 5")
                        elif book.status == "tbr": # Display platform only for tbr books
                            if book.platform is not None:
                                print(f"Platform: {book.platform}")
                        
                        if book.tropes:
                            print(f"Tropes: {', '.join(book.tropes)}")
                        else:
                            print("You haven't listed any tropes for this book :(")
                        print("--------------------")
                else:
                    print("No books found matching this status criteria.\n")

            if filter_choice == '2':
                print("You chose to filter by Rating!")
                while True:
                    try:
                        minimum = input("What's the minimum rating you want to see?").lower()
                        min_rating = float(minimum)
                        if 1 <= min_rating <= 5:
                            break
                        else:
                            print("Please enter a rating between 1 and 5.\n")
                    except ValueError:
                        print("Invalid input. Please enter a number.\n")
                filtered_books = []
                for book in bookshelf:
                    if book.rating is not None and book.rating >= min_rating:
                        filtered_books.append(book)
                
                if filtered_books:
                    for book in filtered_books:
                        print(f"{book.title} by {book.author}.")
                        print(f"{book.length_value}{book.length_unit}")
                        print(f"Rating: {book.rating} / 5")
                        if book.tropes:
                            print(f"Tropes: {', '.join(book.tropes)}")
                        else:
                            print("You haven't listed any tropes for this book :(")
                        print("--------------------")
                else:
                    print("No books found matching this rating criteria.\n")

            elif main_choice == '3': 
                print("You chose to filter by Platform!")
                platform_query = input("What platform are you looking for?\nPhysical, Kindle, Kobo, Audible, Google or BookFunnel").lower()
                filtered_books = [] # This list will hold books matching the platform
                for book in to_be_read:
                    if book.platform is not None and book.platform.lower() == platform_query:
                        filtered_books.append(book)
                if filtered_books:
                    for book in filtered_books:
                        print(f"{book.title} by {book.author}. [{book.platform}]")
                        print(f"{book.length_value}{book.length_unit}")
                        if book.tropes:
                            print(f"Tropes: {', '.join(book.tropes)}")
                        else:
                            print("You haven't listed any tropes for this book :(")
                        print("--------------------")
                else:
                    print("No books found matching this platform criteria.\n")

            elif filter_choice == '4':
                print("You chose to filter by Specific Tropes!")
                trope_query = input("What specific trope are you looking for?\n").lower()

                all_books = bookshelf + to_be_read
                filtered_books = []
                for book in all_books:
                    for trope_item in book.tropes:
                        if trope_item.lower() == trope_query:
                            filtered_books.append(book)
                            break # Found the trope in this book, move to the next book
                print(f"\n--- Found {len(filtered_books)} matching books with the trope '{trope_query}' ---") # Added newlines for better spacing
                    
                if filtered_books:
                    print("\n--- Search Results ---") # Added newline for consistency
                    for book in filtered_books:
                        print(f"{book.title} by {book.author}.")
                        if book.status == "read":
                            if book.rating is not None:
                                print(f"Rating: {book.rating} / 5")
                        elif book.status == "tbr":
                            if book.platform is not None:
                                print(f"Platform: {book.platform}") # Display platform clearly labeled
                            # No else needed here, if platform is None, it won't print.
                            
                        if book.tropes:
                            print(f"Tropes: {', '.join(book.tropes)}")
                        else:
                            print("You haven't listed any tropes for this book :(")
                        print("--------------------")
                else:
                    print("No books found with that trope.\n") # Added newline for spacing

            elif filter_choice == '5':
                print("Returning to Filter & Sort main menu.")
            else:
                print("Invalid filtering choice. Please enter a number between 1 and 5.\n")

        elif main_choice == '2':
            sorting_menu() # Display sorting options
            sort_choice = input("Enter your sorting choice (1-5):\n") # <--- NOW get the specific choice

            # --- We'll put the sorting logic here ---
            if sort_choice == '1':
                print("You chose to sort by Title (A-Z)!")
                all_books = bookshelf + to_be_read
                sorted_books = sorted(all_books, key=lambda book: book.title.lower())
                if sorted_books:
                    print("\n--- Sorted by Title (A-Z) ---")
                    for book in sorted_books:
                        print(f"{book.title} by {book.author}")
                        print(f"{book.length_value}{book.length_unit}")
                        
                        if book.status == "read":
                            if book.rating is not None:
                                print(f"Rating: {book.rating} / 5")
                        elif book.status == "tbr":
                            if book.platform is not None:
                                print(f"Platform: {book.platform}")
                        
                        if book.tropes:
                            print(f"Tropes: {', '.join(book.tropes)}")
                        else:
                            print("You haven't listed any tropes for this book :(")
                        print("--------------------")
                else:
                    print("No books to sort :(\n")


            elif sort_choice == '2':
                print("You chose to sort by Author (A-Z)!")

                all_books = bookshelf + to_be_read
                sorted_books = sorted(all_books, key=lambda book: book.author.lower())
                if sorted_books:
                    print("\n--- Sorted by Author (A-Z) ---")
                    for book in sorted_books:
                        print(f"{book.title} by {book.author}")
                        print(f"{book.length_value}{book.length_unit}")
                        
                        if book.status == "read":
                            if book.rating is not None:
                                print(f"Rating: {book.rating} / 5")
                        elif book.status == "tbr":
                            if book.platform is not None:
                                print(f"Platform: {book.platform}")
                        
                        if book.tropes:
                            print(f"Tropes: {', '.join(book.tropes)}")
                        else:
                            print("You haven't listed any tropes for this book :(")
                        print("--------------------")
                else:
                    print("No books to sort :(\n")


            elif sort_choice == '3':
                print("You chose to sort by Rating (Highest to Lowest)!")

                # Step 1: Filter for books that are "read" and have a rating
                rated_books = []
                for book in bookshelf:
                    if book.rating is not None:
                        rated_books.append(book)
                sorted_by_rating = sorted(rated_books, key=lambda book: book.rating, reverse=True)
                if sorted_by_rating:
                    print("\n--- Sorted by Rating (Highest to Lowest) ---")
                    for book in sorted_by_rating:
                        print(f"{book.title} by {book.author}")
                        print(f"{book.length_value}{book.length_unit}")
                        print(f"Rating: {book.rating} / 5")
                        if book.tropes:
                            print(f"Tropes: {', '.join(book.tropes)}")
                        else:
                            print("You haven't listed any tropes for this book :(")
                        print("--------------------")
                else:
                    print("No books to sort :(\n")

            elif sort_choice == '4':
                print("You chose to sort by Length (Shortest to Longest)!")

                books_w_length = []
                all_books_combined = bookshelf + to_be_read # Start with all books
                for book in all_books_combined:
                    if book.length_value is not None: # Check if it actually has a length
                        books_w_length.append(book)
                sorted_by_length = sorted(books_w_length, key=lambda book: book.length_value)
                if sorted_by_length:
                    print("\n--- Sorted by Length (Shortest to Longest) ---")
                    for book in sorted_by_length:
                        print(f"{book.title} by {book.author}")
                        print(f"{book.length_value}{book.length_unit}")
                        if book.status == "read":
                            if book.rating is not None:
                                print(f"Rating: {book.rating} / 5")
                        elif book.status == "tbr":
                            if book.platform is not None:
                                print(f"Platform: {book.platform}")
                        
                        if book.tropes:
                            print(f"Tropes: {', '.join(book.tropes)}")
                        else:
                            print("You haven't listed any tropes for this book :(")
                        print("--------------------")
                else:
                    print("No books to sort :(\n")
                
                # Step 2: How would you use sorted() to sort 'all_books_with_length' by length_value?
                # sorted_books_by_length = sorted(all_books_with_length, key=lambda book: ???)

                # Step 3: Then, how would you display the 'sorted_books_by_length' list?
                # Remember your standard book display format.



            elif sort_choice == '5':
                print("Returning to Filter & Sort main menu.")
            else:
                print("Invalid sorting choice. Please enter a number between 1 and 5.\n")

        elif main_choice == '3':
            print("Returning to main menu.")
            return # Exit this function to go back to library_lobby
        else:
            print("Invalid main choice. Please enter 1, 2, or 3.\n")