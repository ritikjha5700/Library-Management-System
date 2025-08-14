import sqlite3
import os

class Book:
    def __init__(self, title, author, genre = "Unknown"):
        self.title = title
        self.author = author
        self.genre = genre
        self.is_issued = False

    def __str__(self):
        status = f"Issued to {self.issued_to} on {Da}" if self.issued_to else "Available"
        return f"'{self.title}' by {self.author} [{self.genre}] - {status}"
class Library:
    def __init__(self, db_name = "library.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL COLLATE NOCASE,
                author TEXT NOT NULL,
                genre TEXT,
                is_issued INTEGER DEFAULT 0,
                issued_to INTEGER,
                FOREIGN KEY (issued_to) REFERENCES user(id)
            )
    ''' )
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )
    ''')
        
        self.conn.commit()

    ################ Add and Display user ################

    def add_user(self, name, email):
        try:
            self.cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            self.conn.commit()
            print(f"✅ User '{name}' added successfully.")
        except sqlite3.IntegrityError:
            print(f"⚠️ A user with email '{email}' already exists.")
    
    def list_users(self):
        self.cursor.execute("SELECT id, name, email FROM users")
        rows = self.cursor.fetchall()

        if not rows:
            print("No usres registered yet.")
        else:
            print("\n👤 Registered Users:")
            for user_id, name, email in rows:
                print(f"ID: {user_id} | Name: {name} | Email: {email}")

    ################ Search by Title or Author ################

    def search_by_title(self, keyword):
        self.cursor.execute("SELECT title, author, genre, is_issued FROM books WHERE title LIKE ?", (f"%{keyword}%",))
        rows = self.cursor.fetchall()

        if not rows:
            print(f"No book fount with title '{keyword}'.")
        else:
            print(f"\n Books matching '{keyword}'")
            for row in rows:
                title, author, genre, is_issued = row
                status = "Issued" if is_issued else "Available"
                print(f"- {title} by {author} | Genre: {genre} | Status: {status}")

    def search_by_author(self, keyword):
        self.cursor.execute("SELECT title, author, genre, is_issued FROM books WHERE author LIKE ?", (f"%{keyword}%",))
        rows = self.cursor.fetchall()

        if not rows:
            print(f"No book fount by author '{keyword}'.")
        else:
            print(f"\n Books matching '{keyword}")
            for row in rows:
                title, author, genre, is_issued = row
                status = "Issued" if is_issued else "Available"
                print(f"- {title} by {author} | Genre: {genre} | Status: {status}")

    ################ Book Actions ################
    
    def add_book(self, book):
        self.cursor.execute("""
            INSERT INTO books (title, author, genre, is_issued)
            VALUES (?, ?, ?, ?)
        """, (book.title, book.author, book.genre, int(book.is_issued)))
        self.conn.commit()
        print(f"✅ Book '{book.title}' added to the library.")

    def remove_book(self, title):
        self.cursor.execute("""DELETE FROM books WHERE LOWER(title) = LOWER(?)""", (title,))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            print(f"Book {title} removed. It's gone like your ex.")
        else:
            print(f"uh, can't find {title}, u sure?")

    def display_book(self):
        self.cursor.execute("SELECT title, author, genre, is_issued FROM books")
        rows = self.cursor.fetchall()

        if not rows:
            print("No books here yet. Shelf's empty, bro.")
        else:
            print("\nHere's what we got 📚:")
            for row in rows:
                title, author, genre, is_issued = row
                status = "Issued" if is_issued else "Available"
                print(f"-{title} by {author} | Genre: {genre} | Status: {status}")

    def issue_book(self, title):
        self.cursor.execute("SELECT is_issued FROM books WHERE title = ?", (title,))
        result = self.cursor.fetchone()

        if not result:
            print(f"❌ Can't find {title}. Check the spelling maybe?")
            return
        
        book_id, is_issued = result
        
        if is_issued == 1:
            print(f"{title} is already taken. Gotta wait till it’s back.")
            return
        
        self.list_users()
        try:
            user_id = int(input("Enter the User ID to issue the book to"))
        except ValueError:
            print(f"Invalid input. User ID must be a number.")
            return
        
        self.cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not self.cursor.fetchone():
            print(f"⚠️ No user found with that ID")
            return
        
        self.cursor.execute("UPDATE books SET is_issued = 1 WHERE title = ?", (title,))
        self.conn.commit()
        print(f"✅ Issued {title}. Don't lose it!")

    def show_books_by_user(self, user_id):
        self.cursor.execute("""
            SELECT title, author, genre FROM books WHERE issued_to = ?
    """, (user_id,))
        rows = self.cursor.fetchall()

        if not rows:
            print("This user has no borrowed books")
        else:
            print(f"\nBooks borrowed by user id:")
            for title, author, genre in rows:
                print(f"- {title} by {author} ({genre})")

    def return_book(self,title):
        self.cursor.execute("SELECT is_issued FROM books WHERE Lower(title) = LOWER(?)", (title,))
        result = self.cursor.fetchone()

        if not result:
            print(f"u sure that book is from here? can't find {title}")
            return
        
        if result[0] == 0:
            print(f"📌 Book '{title}' was never issued.")
            return
        
        self.cursor.execute("UPDATE books SET is_issued = 0 WHERE LOWER(title) = LOWER(?)", (title,))
        self.conn.commit()
        print(f"{title} returned. Appreciate it!")
            
    def find_book(self,title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None
    
def main():
    library = Library()

    while True:
        print("\n--- LIBRARY ZONE ---")
        print("1. Show me the books")
        print("2. Add a new book")
        print("3. Remove a book")
        print("4. Issue a book")
        print("5. Return a book")
        print("6. Search by Title")
        print("7. Search by Author")
        print("8. Add a new user")
        print("9. Show all users")
        print("10. Show books borrowed by a user")
        print("11. Exit")

        choice = input("Choose an option (1-11): ")

        if choice == '1':
            library.display_book()

        elif choice == '2':
            while True:
                title = input("book title (or 'q' to stop adding): ")
                if title.lower() == 'q':
                    break
                author = input("who wrote it?: ")
                genre = input("Genre?: ")

                new_book = Book(title, author, genre)
                library.add_book(new_book)
                print(f"bet. {title} by {author} is in.")

        elif choice == '3':
            title = input("book title?: ")
            library.remove_book(title)

        elif choice == '4':
            title = input("which one u tryna read?: ")
            library.issue_book(title)

        elif choice == '5':
            title = input("which one u bringing back?: ")
            library.return_book(title) 

        elif choice == '6':
            keyword = input("Whatchu lookin' for? Drop a title: ")
            library.search_by_title(keyword)

        elif choice == '7':
            keyword = input("Whatchu lookin' for? Drop the Author name: ")
            library.search_by_author(keyword)

        elif choice == '8':
            name = input("Enter a user name: ")
            email = input("Enter user email: ")
            library.add_user(name, email)

        elif choice == '9':
            library.list_users()
        
        elif choice == '10':
            try:
                user_id = int(input("Enter user ID: "))
                library.show_books_by_user(user_id)
            except ValueError:
                print("⚠️ Invalid user ID.")

        elif choice == '11':
            print("aight, cya later! Come back if you feel like reading again")
            break

        else:
            print("fam, that's not an option. pick 1-6.")


if __name__ == "__main__":
    main()
