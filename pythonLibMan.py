import json
import os

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_issued = False

    def __str__(self):
        status = "Issued" if self.is_issued else "Available"
        return f"'{self.title}' by {self.author} - {status}"
    
class Library:
    def __init__(self):
        self.books = []

    def save_to_file(self, filename="books.json"):
        data = [ 
            {"title": book.title, "author": book.author, "is_issued": book.is_issued}
            for book in self.books
        ]
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_from_file(self, filename="books.json"):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                for item in data:
                    book = Book(item["title"], item["author"])
                    book.is_issued = item["is_issued"]
                    self.books.append(book)

    
    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, title):
        book = self.find_book(title)
        if book:
            self.books.remove(book)
            print(f"Book {title} removed. It's gone like your ex.")
        else:
            print(f"uh, can't find {title}, u sure?")

    def display_book(self):
        if not self.books:
            print("No books here yet. Shelf's empty, bro.")
        else:
            print("\nHere's what we got 📚:")
            for book in self.books:
                print(f"- {book}")
                
    def issue_book(self, title):
        book = self.find_book(title)
        if book:
            if book.is_issued:
                print(f"{title} is already taken. Gotta wait till it’s back.")
            else:
                book.is_issued = True
                print(f"✅ Issued {title}. Don't lose it!")
        else:
            print(f"❌ Can't find {title}. Check the spelling maybe?")
    
    def return_book(self,title):
        book = self.find_book(title)
        if book:
            if book.is_issued:
                book.is_issued = False
                print(f"{title} returned. Appreciate it!")
            else:
                print(f"lowkey {title} was never checked out...")
        else:
            print(f"u sure that book is from here? can't find {title}")

    def find_book(self,title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None
    
def main():
    library = Library()
    library.load_from_file()

    while True:
        print("\n--- LIBRARY ZONE ---")
        print("1. Show me the books")
        print("2. Add a new book")
        print("3. Remove a book")
        print("4. Issue a book")
        print("5. Return a book")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == '1':
            library.display_book()

        elif choice == '2':
            title = input("book title?: ")
            author = input("who wrote it?: ")
            new_book = Book(title, author)
            library.add_book(new_book)
            library.save_to_file()
            print(f"bet. {title} by {author} is in.")

        elif choice == '3':
            title = input("book title?: ")
            library.remove_book(title)
            library.save_to_file()  

        elif choice == '4':
            title = input("which one u tryna read?: ")
            library.issue_book(title)
            library.save_to_file() 

        elif choice == '5':
            title = input("which one u bringing back?: ")
            library.return_book(title)  

        elif choice == '6':
            print("aight, cya later! Come back if you feel like reading again")
            library.save_to_file()
            break
        else:
            print("fam, that's not an option. pick 1-6.")


if __name__ == "__main__":
    main()
