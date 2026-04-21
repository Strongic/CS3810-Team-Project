# Library System Project

## Overview

This project is a **full-stack library management system** that allows users to:

* Create accounts and log in
* Search and view books
* Borrow and return books

The system is designed with **separation of concerns**, using:

* A **User Database** for authentication
* A **Book Database** (separate source) for library data

---

## Core Features (MVP)

### Authentication

* User registration (username + password)
* Login / logout functionality
* Secure password storage (hashed passwords)

### Book Management

* Search books by title, author, or genre
* View book details
* Borrow and return books
* Track book availability

### Integration

* Backend connects to:

  * User database (authentication)
  * Book database (library data)

---

## Tech Stack

### Frontend

* JavaScript
* React
* (Optional) Tailwind CSS or plain CSS

### Backend

* Python
* Flask (or FastAPI as an alternative)

### Databases

* User DB: SQLite or PostgreSQL
* Book DB: SQLite, PostgreSQL, or separate API

### Authentication

* bcrypt for password hashing
* Flask sessions or JWT for login sessions

---

## Project Structure

### Backend

```
backend/
│
├── app.py
├── routes/
│   ├── auth.py
│   ├── books.py
│
├── models/
│   ├── user.py
│   ├── book.py
│
├── db/
│   ├── user_db.sqlite
│   ├── book_db.sqlite
│
└── utils/
    ├── auth_helpers.py
```

---

### Frontend

```
frontend/
│
├── src/
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── BookList.jsx
│   │   ├── BookDetail.jsx
│   │
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── BookCard.jsx
│   │
│   └── api/
│       ├── client.js
```


Came up with this groupwork proposal earlier today, we can discuss further on 4/2:

Person 1: Entity relationship diagram and requirements define entities define relationships write assumptions

Person 2: SQL schema/structure create tables keys constraints indexes

Person 3: Database finder, tester for data and queries find/create db of books sample inserts test queries reports/search queries

Person 4: UI Python tkinter app forms/buttons/search connect UI to SQLite Shared work testing making sure schema and UI match