import tkinter as tk
from tkinter import messagebox, font

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

    def borrow_book(self):
        self.is_borrowed = True

    def return_book(self):
        self.is_borrowed = False

    def check_info(self):
        return self.title, self.author

class Library:
    def __init__(self):
        self.books = []
        self.borrowed_books = []

    def add_book(self, book):
        self.books.append(book)

    def display_books(self):
        available_books = [book.title for book in self.books]
        return available_books if available_books else ["No books available"]

    def display_borrowed_books(self):
        borrowed_books = [book.title for book in self.borrowed_books]
        return borrowed_books if borrowed_books else ["No books borrowed"]

    def borrow_book(self, title):
        book = next((book for book in self.books if book.title == title), None)
        if not book:
            return "Book not found"
        self.borrowed_books.append(book)
        self.books.remove(book)
        return f"Borrowed '{title}' successfully!"

    def return_book(self, title):
        book = next((book for book in self.borrowed_books if book.title == title), None)
        if not book:
            return "Book not found"
        self.borrowed_books.remove(book)
        self.books.append(book)
        return f"Returned '{title}' successfully!"

    def check_info(self):
        return len(self.books), len(self.borrowed_books)

library = Library()

# Adding 300 books for testing
for i in range(1, 301):
    library.add_book(Book(f"Book {i}", f"Author {i}"))

# GUI Setup
root = tk.Tk()
root.title("Library Management System")
root.geometry("500x650")
root.configure(bg="#ECF0F1")

custom_font = font.Font(family="Poppins", size=12)

title_label = tk.Label(root, text="Library Management", font=("Poppins", 16, "bold"), bg="#2C3E50", fg="white")
title_label.pack(fill=tk.X, pady=10)

def update_lists():
    available_books_list.delete(0, tk.END)
    borrowed_books_list.delete(0, tk.END)
    for book in library.books:
        available_books_list.insert(tk.END, book.title)
    for book in library.borrowed_books:
        borrowed_books_list.insert(tk.END, book.title)

def borrow_book():
    selected = available_books_list.get(tk.ACTIVE)
    if selected:
        messagebox.showinfo("Success", library.borrow_book(selected))
        update_lists()

def return_book():
    selected = borrowed_books_list.get(tk.ACTIVE)
    if selected:
        messagebox.showinfo("Success", library.return_book(selected))
        update_lists()

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    if title and author:
        library.add_book(Book(title, author))
        update_lists()
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter both title and author")

def search_book():
    search_query = search_entry.get().strip()
    if not search_query:
        messagebox.showwarning("Warning", "Please enter a book title to search.")
        return
    
    found = False
    for index, book in enumerate(library.books):
        if book.title.lower() == search_query.lower():
            available_books_list.selection_clear(0, tk.END)
            available_books_list.selection_set(index)
            available_books_list.activate(index)
            found = True
            break
    
    for index, book in enumerate(library.borrowed_books):
        if book.title.lower() == search_query.lower():
            borrowed_books_list.selection_clear(0, tk.END)
            borrowed_books_list.selection_set(index)
            borrowed_books_list.activate(index)
            found = True
            break
    
    if not found:
        messagebox.showinfo("Search Result", "Book not found.")

button_style = {"font": custom_font, "bg": "#F39C12", "fg": "white", "bd": 0, "relief": "flat", "padx": 10, "pady": 8, "borderwidth": 2, "highlightthickness": 0}

tk.Label(root, text="Add a Book:", font=custom_font, bg="#ECF0F1").pack(pady=5)
tk.Label(root, text="Title:", font=custom_font, bg="#ECF0F1").pack()
title_entry = tk.Entry(root, font=custom_font, bg="white", fg="#2C3E50", relief="solid", borderwidth=1)
title_entry.pack(fill=tk.X, padx=10, pady=3)
tk.Label(root, text="Author:", font=custom_font, bg="#ECF0F1").pack()
author_entry = tk.Entry(root, font=custom_font, bg="white", fg="#2C3E50", relief="solid", borderwidth=1)
author_entry.pack(fill=tk.X, padx=10, pady=3)
add_button = tk.Button(root, text="Add Book", **button_style, command=add_book)
add_button.pack(anchor="w", padx=10, pady=5)

tk.Label(root, text="Search Book:", font=custom_font, bg="#ECF0F1").pack()
search_entry = tk.Entry(root, font=custom_font, bg="white", fg="#2C3E50", relief="solid", borderwidth=1)
search_entry.pack(fill=tk.X, padx=10, pady=3)
search_button = tk.Button(root, text="Search", **button_style, command=search_book)
search_button.pack(anchor="w", padx=10, pady=5)

tk.Label(root, text="Available Books:", font=custom_font, bg="#ECF0F1").pack()
available_books_list = tk.Listbox(root, font=custom_font, bg="white", fg="#2C3E50", relief="solid", borderwidth=1)
available_books_list.pack(fill=tk.X, padx=10, pady=3)
borrow_button = tk.Button(root, text="Borrow Book", **button_style, command=borrow_book)
borrow_button.pack(anchor="w", padx=10, pady=5)

tk.Label(root, text="Borrowed Books:", font=custom_font, bg="#ECF0F1").pack()
borrowed_books_list = tk.Listbox(root, font=custom_font, bg="white", fg="#2C3E50", relief="solid", borderwidth=1)
borrowed_books_list.pack(fill=tk.X, padx=10, pady=3)
return_button = tk.Button(root, text="Return Book", **button_style, command=return_book)
return_button.pack(anchor="w", padx=10, pady=5)

update_lists()
root.mainloop()
