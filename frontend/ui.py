import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import requests
 
BASE_URL = "http://127.0.0.1:5000"

# hits flask /search route
def search_books_google(query):
    response = requests.get(f"{BASE_URL}/search", params={"q": query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"search failed: {response.status_code}")
    
# send registration data to backend
def register_user(username, password):
    payload = {"username": username, "password": password}
    try:
        response = requests.post(f"{BASE_URL}/register", json=payload)
        if response.status_code == 201:
            return True, "Account created successfully!"
        else:
            error_msg = response.json().get("error", "Registration failed")
            return False, error_msg
    except Exception as e:
        return False, str(e)
    

# hits route to remove a book from users collection
def return_book_for_user(user, book):
    payload = {
        "user_id": user['user_id'],
        "book_id": book.get('book_id')
    }
    try:
        response = requests.post(f"{BASE_URL}/collection/remove", json=payload)
        if response.status_code == 200:
            return True, response.json().get("message")
        else:
            return False, response.json().get("error", "Could not return book.")
    except Exception as e:
        return False, str(e)


# hits /login route
def login_user(username, password):
    payload = {"username": username, "password": password}
    try:
        response = requests.post(f"{BASE_URL}/login", json=payload)
        if response.status_code == 200:
            return True, response.json()
        return False, response.json("error", "Login failed")
    except Exception as e:
        return False, str(e)
    
# hits route for adding book to user's collection
def borrow_book_for_user(user, book):
    payload = {
        "user_id": user['user_id'],
        "book_id": book['book_id']
    }
    response = requests.post(f"{BASE_URL}/collection/add", json=payload)
    if response.status_code == 200:
        return True, "Book added to your collection!"
    return False, "Could not add book to collection."








# Temporary implementations were removed, the functions just need to be redefined (hopefully) 


# Borrow/return and google book implementation removed: 
# borrow_book_for_user, return_book_for_user, and search_books_google functions


# Auth implementation removed: 
# account_db.sqlite
# users(user_id, username UNIQUE, password_hash)
# register_user and login_user functions




# App
 
class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Library System")
        self.geometry("980x640")
        self.minsize(900, 580)

        self.current_user = None
        self.current_books = []
        self.selected_book = None

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self._build_frames()
        self.show_auth_frame()

    
    # Frame setup
 

    def _build_frames(self):
        self.auth_frame = ttk.Frame(self, padding=20) # authentication page
        self.main_frame = ttk.Frame(self, padding=12) # main library page

        for frame in (self.auth_frame, self.main_frame):
            frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_auth_frame()
        self._build_main_frame()

    def show_auth_frame(self):
        self.auth_frame.tkraise()

    def show_main_frame(self):
        self.main_frame.tkraise()

     
    # Auth UI
    
    def _build_auth_frame(self):
        container = ttk.Frame(self.auth_frame, padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            container,
            text="Library System",
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 16))

        ttk.Label(container, text="Username").grid(row=1, column=0, sticky="w", pady=4)
        self.username_entry = ttk.Entry(container, width=32)
        self.username_entry.grid(row=1, column=1, pady=4)

        ttk.Label(container, text="Password").grid(row=2, column=0, sticky="w", pady=4)
        self.password_entry = ttk.Entry(container, width=32, show="*")
        self.password_entry.grid(row=2, column=1, pady=4)

        button_row = ttk.Frame(container)
        button_row.grid(row=3, column=0, columnspan=2, pady=(14, 6))

        ttk.Button(button_row, text="Login", command=self.handle_login).grid(row=0, column=0, padx=6)
        ttk.Button(button_row, text="Register", command=self.handle_register).grid(row=0, column=1, padx=6)

        ttk.Label(
            container,
            text="\u00A9 2026 Landon Pace Tommy Cameron. All rights reserved  ",
        ).grid(row=4, column=0, columnspan=2, pady=(12, 0))

        self.password_entry.bind("<Return>", lambda event: self.handle_login())

    def handle_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        success, message = register_user(username, password)

        if success:
            messagebox.showinfo("Register", message)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Register Failed", message)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        success, result = login_user(username, password)

        if success:
            self.current_user = result
            self.password_entry.delete(0, tk.END)
            self.user_label.config(text=f"Logged in as: {self.current_user['username']}")
            self.show_main_frame()
        else:
            messagebox.showerror("Login Failed", result)

   
    # Main App UI
  

    def _build_main_frame(self):
        # Top bar
        top_bar = ttk.Frame(self.main_frame)
        top_bar.pack(fill="x", pady=(0, 8))

        self.user_label = ttk.Label(top_bar, text="Logged in as: [None]")
        self.user_label.pack(side="left")

        ttk.Button(top_bar, text="Logout", command=self.handle_logout).pack(side="right")

        # Search controls
        search_frame = ttk.LabelFrame(self.main_frame, text="Search Books", padding=10)
        search_frame.pack(fill="x", pady=(0, 8))

        self.search_var = tk.StringVar()

        ttk.Label(search_frame, text="Title / Author / Genre").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        ttk.Button(search_frame, text="Search", command=self.handle_search).grid(row=0, column=2)
        ttk.Button(search_frame, text="Clear", command=self.clear_results).grid(row=0, column=3, padx=(8, 0))

        search_frame.grid_columnconfigure(1, weight=1)
        self.search_entry.bind("<Return>", lambda event: self.handle_search())

        #Middle content split
        content = ttk.Frame(self.main_frame)
        content.pack(fill="both", expand=True)

        left = ttk.LabelFrame(content, text="Results", padding=8)
        right = ttk.LabelFrame(content, text="Book Details", padding=8)

        left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        # Results table
        self.results_tree = ttk.Treeview(
            left,
            columns=("title", "authors", "genre"),
            show="headings",
            height=18
        )
        self.results_tree.heading("title", text="Title")
        self.results_tree.heading("authors", text="Authors")
        self.results_tree.heading("genre", text="Genre")

        self.results_tree.column("title", width=240, anchor="w")
        self.results_tree.column("authors", width=180, anchor="w")
        self.results_tree.column("genre", width=140, anchor="w")

        y_scroll = ttk.Scrollbar(left, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=y_scroll.set)

        self.results_tree.pack(side="left", fill="both", expand=True)
        y_scroll.pack(side="right", fill="y")

        self.results_tree.bind("<<TreeviewSelect>>", self.on_result_select)

        # Details panel
        self.details_text = tk.Text(right, wrap="word", height=22, width=42)
        self.details_text.pack(fill="both", expand=True)

        button_row = ttk.Frame(right)
        button_row.pack(fill="x", pady=(8, 0))

        ttk.Button(button_row, text="Borrow Selected Book", command=self.handle_borrow).pack(side="left", padx=(0, 6))
        ttk.Button(button_row, text="Return Selected Book", command=self.handle_return).pack(side="left")

    def handle_logout(self):
        self.current_user = None
        self.selected_book = None
        self.search_var.set("")
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.clear_results()
        self.show_auth_frame()

     # Search/Results
 
    def handle_search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Search", "Enter a title, author, or genre.")
            return

        try:
            books = search_books_google(query)
        except Exception as exc:
            messagebox.showerror("Search Error", str(exc))
            return

        self.current_books = books
        self.selected_book = None

        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        for idx, book in enumerate(books):
            self.results_tree.insert(
                "",
                "end",
                iid=str(idx),
                values=(book["title"], book["authors"], book["genre"])
            )

        self.details_text.delete("1.0", tk.END)

        if not books:
            self.details_text.insert(tk.END, "No books found.")
        else:
            self.details_text.insert(
                tk.END,
                f"Found {len(books)} result(s).\nSelect a row to view details."
            )

    def clear_results(self):
        self.current_books = []
        self.selected_book = None
        self.search_var.set("")
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.details_text.delete("1.0", tk.END)

    def on_result_select(self, event=None):
        selection = self.results_tree.selection()
        if not selection:
            return

        index = int(selection[0])
        if index < 0 or index >= len(self.current_books):
            return

        self.selected_book = self.current_books[index]
        self.show_book_details(self.selected_book)

    def show_book_details(self, book):
        self.details_text.delete("1.0", tk.END)


        details = (
                f"Title: {book.get('title', 'N/A')}\n\n"
                f"Authors: {book.get('authors', 'Unknown')}\n\n"
                f"Google ID: {book.get('google_id', 'N/A')}\n\n"
                f"Description: {book.get('description', 'No description available.')}\n"
            )
        # details = (
        #     f"Title: {book['title']}\n\n"
        #     f"Authors: {book['authors']}\n\n"
        #     f"Genre: {book['genre']}\n\n"
        #     f"Publisher: {book['publisher']}\n\n"
        #     f"Published Date: {book['published_date']}\n\n"
        #     f"ISBN: {book['isbn']}\n\n"
        #     f"Page Count: {book['page_count']}\n\n"
        #     f"{book['external_access_note']}\n\n"
        #     f"Info Link: {book['info_link'] or 'N/A'}\n\n"
        #     f"Description:\n{book['description']}\n\n"
        #     f"Borrow Status in Project DB: [VALUE NEEDED]\n"
        # )

        self.details_text.insert(tk.END, details)

    
    # Borrow/Return
    
    def handle_borrow(self):
        if not self.current_user:
            messagebox.showerror("Borrow", "You must be logged in.")
            return

        if not self.selected_book:
            messagebox.showwarning("Borrow", "Select a book first.")
            return

        success, message = borrow_book_for_user(self.current_user, self.selected_book)

        if success:
            messagebox.showinfo("Borrow", message)
        else:
            messagebox.showwarning("Borrow", message)

    def handle_return(self):
        if not self.current_user:
            messagebox.showerror("Return", "You must be logged in.")
            return

        if not self.selected_book:
            messagebox.showwarning("Return", "Select a book first.")
            return

        success, message = return_book_for_user(self.current_user, self.selected_book)

        if success:
            messagebox.showinfo("Return", message)
        else:
            messagebox.showwarning("Return", message)


# Init

def main():
   # init_account_db() 
    app = LibraryApp()
    app.mainloop()


if __name__ == "__main__":
    main()