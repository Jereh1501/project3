# Library Management System

A simple Python command-line library application backed by SQLite.

## Features
- Register books with ISBN, title, author and publication year.
- Retrieve all registered books.
- Search by title, author or ISBN.
- Modify book information and availability.
- Delete a book by its ID.
- Uses parameterised SQL queries (`?` placeholders) and handles common input and database errors.

## Requirements
Python 3. SQLite is included with Python's built-in `sqlite3` module.

## Run
```bash
python main.py
```
The `library.db` database and `books` table are created automatically.
