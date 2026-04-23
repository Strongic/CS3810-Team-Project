# Library Management System

## Overview

This is a full-stack library management system. The application features a Python Tkinter desktop client that communicates with a Flask REST API to manage user authentication, book discovery, and personal collections.

The system follows a Client-Server architecture, ensuring that the user interface is completely decoupled from the database logic.
Core Features

🔐 Authentication

    User Registration: Create a unique account directly through the UI.

    Secure Login: Session-based interaction where the UI tracks the user_id. Password hashing soon to be added

    Credential Validation: Server-side verification of usernames and passwords.

📚 Book Management

    Seeded Catalog: A pre-populated library of professional software engineering and data science texts.

    Smart Search: Local database querying with support for partial matches on titles and authors.

    Hybrid Discovery: Capability to interface with the Google Books API for expanded search (optional toggle).

🤝 Borrowing System

    Personal Collections: Users can "Borrow" books, creating a persistent link in the database.

    Many-to-Many Relationships: Managed via a junction table (user_books) to allow multiple users to interact with multiple books.

    Real-time Returns: Remove books from your collection to update the library inventory.

Tech Stack
Frontend (Desktop)

    Python 3.x

    Tkinter / ttk: For a native, responsive desktop GUI.

    Requests: For handling asynchronous API calls to the Flask backend.

Backend (API)

    Flask: RESTful API routing.

    SQLAlchemy (ORM): To manage database models and relationships without raw SQL.

    SQLite: A lightweight, reliable relational database.

Project Structure

.
├── app/
│   ├── __init__.py        # App factory & SQLAlchemy init
│   ├── models.py          # Database Schema (User, Book, user_books)
│   ├── routes.py          # API Endpoints (Login, Register, Search, Collection)
│   └── services.py        # External API integration (Google Books)
├── ui.py                  # Tkinter Desktop Application
├── seed.py                # Database initialization and data seeding
├── run.py                 # Entry point for the Flask server
└── library.db             # SQLite Database file

Database Schema

The system utilizes three main tables to manage the data:

    User: Stores user_id, username, and password.

    Book: Stores book_id, google_id, title, and authors.

    User_Books: A junction table linking user_id to book_id for the borrowing system.