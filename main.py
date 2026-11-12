import sqlite3

DATABASE = "library.db"


def connect():
    return sqlite3.connect(DATABASE)


def create_table():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT UNIQUE,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publication_year INTEGER,
                available INTEGER NOT NULL DEFAULT 1
            )
        """)


def register_book():
    try:
        isbn = input("ISBN: ").strip()
        title = input("Book title: ").strip()
        author = input("Author: ").strip()
        year_text = input("Publication year (leave blank if unknown): ").strip()
        year = int(year_text) if year_text else None

        with connect() as conn:
            conn.execute("""
                INSERT INTO books (isbn, title, author, publication_year)
                VALUES (?, ?, ?, ?)
            """, (isbn or None, title, author, year))
        print("Book registered successfully.")
    except ValueError:
        print("Publication year must be a number.")
    except sqlite3.IntegrityError as error:
        print("Could not register book:", error)


def display_books(rows):
    if not rows:
        print("No books found.")
        return
    print("\nID | ISBN | Title | Author | Year | Available")
    print("-" * 85)
    for row in rows:
        print(" | ".join(str(value) for value in row))


def retrieve_books():
    with connect() as conn:
        rows = conn.execute("""
            SELECT book_id, isbn, title, author, publication_year, available
            FROM books ORDER BY title
        """).fetchall()
    display_books(rows)


def search_books():
    term = input("Enter a title, author, or ISBN to search: ").strip()
    pattern = f"%{term}%"
    with connect() as conn:
        rows = conn.execute("""
            SELECT book_id, isbn, title, author, publication_year, available
            FROM books
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
            ORDER BY title
        """, (pattern, pattern, pattern)).fetchall()
    display_books(rows)


def modify_book():
    try:
        book_id = int(input("Book ID to modify: "))
        title = input("New title: ").strip()
        author = input("New author: ").strip()
        year_text = input("New publication year (blank if unknown): ").strip()
        year = int(year_text) if year_text else None
        availability_text = input("Available? (yes/no): ").strip().lower()
        if availability_text not in ("yes", "no"):
            print("Enter yes or no for availability.")
            return
        available = 1 if availability_text == "yes" else 0

        with connect() as conn:
            cursor = conn.execute("""
                UPDATE books
                SET title = ?, author = ?, publication_year = ?, available = ?
                WHERE book_id = ?
            """, (title, author, year, available, book_id))
        print("Book updated." if cursor.rowcount else "Book ID not found.")
    except ValueError:
        print("Book ID and publication year must be numbers.")


def delete_book():
    try:
        book_id = int(input("Book ID to delete: "))
        with connect() as conn:
            cursor = conn.execute(
                "DELETE FROM books WHERE book_id = ?", (book_id,)
            )
        print("Book deleted." if cursor.rowcount else "Book ID not found.")
    except ValueError:
        print("Book ID must be a number.")


def main():
    create_table()
    actions = {
        "1": register_book,
        "2": retrieve_books,
        "3": search_books,
        "4": modify_book,
        "5": delete_book,
    }
    while True:
        print("""
LIBRARY MANAGEMENT SYSTEM
1. Register a book
2. Retrieve all books
3. Search for a book
4. Modify a book
5. Delete a book
0. Exit
""")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
