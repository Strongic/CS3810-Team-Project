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
