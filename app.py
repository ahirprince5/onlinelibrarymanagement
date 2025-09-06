import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os

# Login Window 
class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Library System Login")
        master.geometry("400x250")
        master.configure(bg="#f0f0f0")
        master.resizable(False, False)

        self.username = "admin"
        self.password = "admin123"

        tk.Label(master, text="Library Management System", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        tk.Label(master, text="Username:", bg="#f0f0f0").pack(pady=(8, 2))
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.pack()

        tk.Label(master, text="Password:", bg="#f0f0f0").pack(pady=(8, 2))
        self.password_entry = tk.Entry(master, width=30, show="*")
        self.password_entry.pack()

        self.login_btn = tk.Button(master, text="Login", command=self.check_login, bg="#4CAF50", fg="white", width=15)
        self.login_btn.pack(pady=15)

        self.username_entry.focus()

    def check_login(self):
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()

        if user == self.username and pwd == self.password:
            self.master.destroy()  # Close login window
            root = tk.Tk()
            LibraryManagementSystem(root)  # Open main system
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")


# Main Library Management System
class LibraryManagementSystem:

    def __init__(self, master):
        self.master = master
        master.title("Library Management System")
        master.geometry("1000x700")
        master.resizable(True, True)

        self.primary_color = "#4A90E2"   # Blue
        self.secondary_color = "#8CC63F" # Green
        self.accent_color = "#F5A623"    # Orange
        self.bg_color = "#F0F2F5"        # Light Gray
        self.text_color = "#333333"      # Dark Gray
        self.header_bg = "#E0E5EB"       # Header Gray

        master.configure(bg=self.bg_color)

        self.books_file = "books.csv"
        self.members_file = "members.csv"
        self.borrowings_file = "borrowings.csv"

        self.books = []
        self.members = []
        self.borrowings = []

        self._load_data()

        # Compute next IDs
        self.next_book_id = self._get_next_id(self.books)
        self.next_member_id = self._get_next_id(self.members)
        self.next_borrowing_id = self._get_next_id(self.borrowings)

        # Top bar with logout
        topbar = tk.Frame(master, bg=self.bg_color)
        topbar.pack(fill="x")
        logout_btn = tk.Button(
            topbar, text="Logout", command=self.logout,
            bg="red", fg="white", font=("Arial", 10, "bold")
        )
        logout_btn.pack(anchor="e", padx=10, pady=10)

        # Build UI
        self._create_widgets()

    def logout(self):
        """Logs out and returns to the login screen."""
        self.master.destroy()
        root = tk.Tk()
        LoginWindow(root)
        root.mainloop()

    def _load_data(self):
        """Loads data from CSV files into memory."""
        self.books = self._load_csv(self.books_file)
        self.members = self._load_csv(self.members_file)
        self.borrowings = self._load_csv(self.borrowings_file)

    def _save_data(self):
        """Saves current data from memory to CSV files."""
        self._save_csv(self.books_file, self.books, ['id', 'title', 'author', 'isbn', 'published_year', 'status'])
        self._save_csv(self.members_file, self.members, ['id', 'name', 'email', 'phone'])
        self._save_csv(self.borrowings_file, self.borrowings, ['id', 'book_id', 'member_id', 'borrow_date', 'return_date'])

    def _load_csv(self, filename):
        """Helper to load data from a single CSV file."""
        data = []
        if os.path.exists(filename):
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Normalize and cast fields
                    if 'id' in row and row['id'] != '':
                        row['id'] = int(row['id'])
                    if 'book_id' in row and row['book_id'] != '':
                        row['book_id'] = int(row['book_id'])
                    if 'member_id' in row and row['member_id'] != '':
                        row['member_id'] = int(row['member_id'])
                    if 'published_year' in row and row['published_year']:
                        try:
                            row['published_year'] = int(row['published_year'])
                        except ValueError:
                            row['published_year'] = None
                    if 'return_date' in row and (row['return_date'] == 'None' or row['return_date'] == ''):
                        row['return_date'] = None
                    data.append(row)
        return data

    def _save_csv(self, filename, data, headers):
        """Helper to save data to a single CSV file with provided headers."""
        # Ensure file exists with headers even if empty
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for item in data:
                row = {}
                for h in headers:
                    v = item.get(h, "")
                    if h == 'return_date' and v is None:
                        v = None
                    row[h] = v
                writer.writerow(row)

    def _get_next_id(self, data_list):
        """Generates the next available ID for a list of dictionaries."""
        if not data_list:
            return 1
        return max(int(item['id']) for item in data_list if 'id' in item) + 1

    #  UI Construction 
    def _create_widgets(self):
        """Creates all the GUI elements for the application."""
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Style for ttk widgets
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass  

        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.primary_color, foreground="white",
                        font=('Arial', 10, 'bold'), padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", self.accent_color)],
                  foreground=[("selected", "white")])

        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=('Arial', 10))
        style.configure("TButton", background=self.primary_color, foreground="white",
                        font=('Arial', 10, 'bold'), padding=5)
        style.map("TButton", background=[('active', self.accent_color)])

        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background=self.header_bg, foreground=self.text_color)
        style.configure("Treeview", font=('Arial', 9), rowheight=25, background="white", foreground=self.text_color, fieldbackground="white")
        style.map('Treeview', background=[('selected', self.primary_color)])

        # --- Books Tab ---
        self.books_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.books_frame, text="Books")
        self._create_books_tab(self.books_frame)

        # --- Members Tab ---
        self.members_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.members_frame, text="Members")
        self._create_members_tab(self.members_frame)

        # --- Borrow/Return Tab ---
        self.borrow_return_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.borrow_return_frame, text="Borrow/Return")
        self._create_borrow_return_tab(self.borrow_return_frame)

        # --- All Borrowings Tab ---
        self.all_borrowings_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.all_borrowings_frame, text="All Borrowings")
        self._create_all_borrowings_tab(self.all_borrowings_frame)

        # Populate initial views
        self._populate_books_treeview()
        self._populate_members_treeview()
        self._populate_borrow_return_treeview()
        self._populate_all_borrowings_treeview()

        # Refresh data on tab change
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _on_tab_change(self, event):
        """Refreshes data in the current tab's Treeview when tab changes."""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "Books":
            self._populate_books_treeview()
        elif selected_tab == "Members":
            self._populate_members_treeview()
        elif selected_tab == "Borrow/Return":
            self._populate_borrow_return_treeview()
            self._update_borrow_comboboxes()
        elif selected_tab == "All Borrowings":
            self._populate_all_borrowings_treeview()

    #  Books Tab
    def _create_books_tab(self, parent_frame):
        """Creates UI elements for the Books tab."""
        form_frame = ttk.LabelFrame(parent_frame, text="Book Details", padding="15")
        form_frame.pack(pady=10, padx=10, fill="x")

        labels = ["Title:", "Author:", "ISBN:", "Published Year:"]
        self.book_entries = {}
        for i, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=5, padx=5)
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
            self.book_entries[label_text.replace(":", "").strip().lower().replace(" ", "_")] = entry

        form_frame.grid_columnconfigure(1, weight=1)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)

        self.add_book_btn = ttk.Button(button_frame, text="Add Book", command=self._add_book)
        self.add_book_btn.pack(side="left", padx=5)

        self.update_book_btn = ttk.Button(button_frame, text="Update Book", command=self._update_book, state=tk.DISABLED)
        self.update_book_btn.pack(side="left", padx=5)

        self.clear_book_form_btn = ttk.Button(button_frame, text="Clear Form", command=self._clear_book_form)
        self.clear_book_form_btn.pack(side="left", padx=5)

        self.books_tree = ttk.Treeview(parent_frame, columns=("ID", "Title", "Author", "ISBN", "Year", "Status"), show="headings")
        self.books_tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.books_tree.heading("ID", text="ID")
        self.books_tree.heading("Title", text="Title")
        self.books_tree.heading("Author", text="Author")
        self.books_tree.heading("ISBN", text="ISBN")
        self.books_tree.heading("Year", text="Year")
        self.books_tree.heading("Status", text="Status")

        self.books_tree.column("ID", width=50, stretch=tk.NO, anchor="center")
        self.books_tree.column("Title", width=200, stretch=tk.YES)
        self.books_tree.column("Author", width=150, stretch=tk.YES)
        self.books_tree.column("ISBN", width=120, stretch=tk.NO, anchor="center")
        self.books_tree.column("Year", width=80, stretch=tk.NO, anchor="center")
        self.books_tree.column("Status", width=90, stretch=tk.NO, anchor="center")

        self.books_tree.bind("<<TreeviewSelect>>", self._on_book_select)

        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        action_button_frame = ttk.Frame(parent_frame)
        action_button_frame.pack(pady=5, padx=10, fill="x", anchor="e")

        self.delete_book_btn = ttk.Button(action_button_frame, text="Delete Selected Book", command=self._delete_book)
        self.delete_book_btn.pack(side="right", padx=5)

    def _populate_books_treeview(self):
        """Populates the books Treeview with current data."""
        for i in self.books_tree.get_children():
            self.books_tree.delete(i)

        for book in self.books:
            self.books_tree.insert("", "end", iid=book['id'], values=(
                book['id'], book.get('title', ''), book.get('author', ''), book.get('isbn', ''),
                book.get('published_year', ''), str(book.get('status', 'available')).capitalize()
            ))

    def _on_book_select(self, event):
        """Populates the book form when a book is selected in the Treeview."""
        selected_item = self.books_tree.focus()
        if not selected_item:
            self._clear_book_form()
            self.update_book_btn.config(state=tk.DISABLED)
            return

        book_id = int(self.books_tree.item(selected_item, "values")[0])
        selected_book = next((b for b in self.books if b['id'] == book_id), None)

        if selected_book:
            self._clear_book_form()
            self.book_entries['title'].insert(0, selected_book.get('title', ''))
            self.book_entries['author'].insert(0, selected_book.get('author', ''))
            self.book_entries['isbn'].insert(0, selected_book.get('isbn', ''))
            self.book_entries['published_year'].insert(0, selected_book.get('published_year', ''))
            self.selected_book_id = book_id

            self.add_book_btn.config(state=tk.DISABLED)
            self.update_book_btn.config(state=tk.NORMAL)
        else:
            self._clear_book_form()
            self.add_book_btn.config(state=tk.NORMAL)
            self.update_book_btn.config(state=tk.DISABLED)

    def _clear_book_form(self):
        """Clears all entry fields in the book form."""
        for entry in self.book_entries.values():
            entry.delete(0, tk.END)
        self.selected_book_id = None
        self.add_book_btn.config(state=tk.NORMAL)
        self.update_book_btn.config(state=tk.DISABLED)
        try:
            self.books_tree.selection_remove(self.books_tree.focus())
        except tk.TclError:
            pass

    def _add_book(self):
        """Adds a new book to the system."""
        title = self.book_entries['title'].get().strip()
        author = self.book_entries['author'].get().strip()
        isbn = self.book_entries['isbn'].get().strip()
        year_str = self.book_entries['published_year'].get().strip()

        if not all([title, author, isbn, year_str]):
            messagebox.showerror("Input Error", "All fields (Title, Author, ISBN, Published Year) are required.")
            return

        try:
            published_year = int(year_str)
            if not (1000 <= published_year <= datetime.now().year + 5):
                messagebox.showerror("Input Error", "Published year must be a valid year.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Published Year must be a number.")
            return

        # Unique ISBN check
        if any(str(book.get('isbn', '')).strip() == isbn for book in self.books):
            messagebox.showerror("Input Error", "Book with this ISBN already exists.")
            return

        new_book = {
            'id': self.next_book_id,
            'title': title,
            'author': author,
            'isbn': isbn,
            'published_year': published_year,
            'status': 'available'
        }
        self.books.append(new_book)
        self.next_book_id += 1
        self._save_data()
        self._populate_books_treeview()
        self._clear_book_form()
        messagebox.showinfo("Success", f"Book '{title}' added successfully!")

    def _update_book(self):
        """Updates details of an existing book."""
        if not hasattr(self, 'selected_book_id') or self.selected_book_id is None:
            messagebox.showerror("Error", "No book selected for update.")
            return

        book_id_to_update = self.selected_book_id
        title = self.book_entries['title'].get().strip()
        author = self.book_entries['author'].get().strip()
        isbn = self.book_entries['isbn'].get().strip()
        year_str = self.book_entries['published_year'].get().strip()

        if not all([title, author, isbn, year_str]):
            messagebox.showerror("Input Error", "All fields are required for update.")
            return

        try:
            published_year = int(year_str)
            if not (1000 <= published_year <= datetime.now().year + 5):
                messagebox.showerror("Input Error", "Published year must be a valid year.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Published Year must be a number.")
            return

        # Unique ISBN check excluding the current book
        if any((str(book.get('isbn', '')).strip() == isbn) and (int(book['id']) != book_id_to_update) for book in self.books):
            messagebox.showerror("Input Error", "Another book with this ISBN already exists.")
            return

        for book in self.books:
            if int(book['id']) == book_id_to_update:
                book['title'] = title
                book['author'] = author
                book['isbn'] = isbn
                book['published_year'] = published_year
                break

        self._save_data()
        self._populate_books_treeview()
        self._clear_book_form()
        messagebox.showinfo("Success", f"Book ID {book_id_to_update} updated successfully!")

    def _delete_book(self):
        """Deletes the selected book from the system."""
        selected_item = self.books_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "No book selected for deletion.")
            return

        book_id_to_delete = int(self.books_tree.item(selected_item, "values")[0])

        if any(int(b['book_id']) == book_id_to_delete and b['return_date'] is None for b in self.borrowings):
            messagebox.showerror("Deletion Error", "This book is currently borrowed and cannot be deleted.")
            return

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Book ID {book_id_to_delete}?"):
            self.books = [book for book in self.books if int(book['id']) != book_id_to_delete]
            self._save_data()
            self._populate_books_treeview()
            self._clear_book_form()
            messagebox.showinfo("Success", f"Book ID {book_id_to_delete} deleted successfully.")

    # Members Tab
    def _create_members_tab(self, parent_frame):
        """Creates UI elements for the Members tab."""
        form_frame = ttk.LabelFrame(parent_frame, text="Member Details", padding="15")
        form_frame.pack(pady=10, padx=10, fill="x")

        labels = ["Name:", "Email:", "Phone (Optional):"]
        self.member_entries = {}
        for i, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=5, padx=5)
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
            key = label_text.replace(":", "").replace("(Optional)", "").strip().lower().replace(" ", "_")
            self.member_entries[key] = entry

        form_frame.grid_columnconfigure(1, weight=1)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)

        self.add_member_btn = ttk.Button(button_frame, text="Add Member", command=self._add_member)
        self.add_member_btn.pack(side="left", padx=5)

        self.update_member_btn = ttk.Button(button_frame, text="Update Member", command=self._update_member, state=tk.DISABLED)
        self.update_member_btn.pack(side="left", padx=5)

        self.clear_member_form_btn = ttk.Button(button_frame, text="Clear Form", command=self._clear_member_form)
        self.clear_member_form_btn.pack(side="left", padx=5)

        self.members_tree = ttk.Treeview(parent_frame, columns=("ID", "Name", "Email", "Phone"), show="headings")
        self.members_tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.members_tree.heading("ID", text="ID")
        self.members_tree.heading("Name", text="Name")
        self.members_tree.heading("Email", text="Email")
        self.members_tree.heading("Phone", text="Phone")

        self.members_tree.column("ID", width=50, stretch=tk.NO, anchor="center")
        self.members_tree.column("Name", width=200, stretch=tk.YES)
        self.members_tree.column("Email", width=250, stretch=tk.YES)
        self.members_tree.column("Phone", width=120, stretch=tk.NO, anchor="center")

        self.members_tree.bind("<<TreeviewSelect>>", self._on_member_select)

        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        action_button_frame = ttk.Frame(parent_frame)
        action_button_frame.pack(pady=5, padx=10, fill="x", anchor="e")

        self.delete_member_btn = ttk.Button(action_button_frame, text="Delete Selected Member", command=self._delete_member)
        self.delete_member_btn.pack(side="right", padx=5)

    def _populate_members_treeview(self):
        """Populates the members Treeview with current data."""
        for i in self.members_tree.get_children():
            self.members_tree.delete(i)

        for member in self.members:
            self.members_tree.insert("", "end", iid=member['id'], values=(
                member['id'], member.get('name', ''), member.get('email', ''), member.get('phone', '')
            ))

    def _on_member_select(self, event):
        """Populates the member form when a member is selected in the Treeview."""
        selected_item = self.members_tree.focus()
        if not selected_item:
            self._clear_member_form()
            self.update_member_btn.config(state=tk.DISABLED)
            return

        member_id = int(self.members_tree.item(selected_item, "values")[0])
        selected_member = next((m for m in self.members if int(m['id']) == member_id), None)

        if selected_member:
            self._clear_member_form()
            self.member_entries['name'].insert(0, selected_member.get('name', ''))
            self.member_entries['email'].insert(0, selected_member.get('email', ''))
            self.member_entries['phone'].insert(0, selected_member.get('phone', ''))
            self.selected_member_id = member_id

            self.add_member_btn.config(state=tk.DISABLED)
            self.update_member_btn.config(state=tk.NORMAL)
        else:
            self._clear_member_form()
            self.add_member_btn.config(state=tk.NORMAL)
            self.update_member_btn.config(state=tk.DISABLED)

    def _clear_member_form(self):
        """Clears all entry fields in the member form."""
        for entry in self.member_entries.values():
            entry.delete(0, tk.END)
        self.selected_member_id = None
        self.add_member_btn.config(state=tk.NORMAL)
        self.update_member_btn.config(state=tk.DISABLED)
        try:
            self.members_tree.selection_remove(self.members_tree.focus())
        except tk.TclError:
            pass

    def _add_member(self):
        """Adds a new member to the system."""
        name = self.member_entries['name'].get().strip()
        email = self.member_entries['email'].get().strip()
        phone = self.member_entries['phone'].get().strip()

        if not all([name, email]):
            messagebox.showerror("Input Error", "Name and Email are required.")
            return

        # Basic email check
        if "@" not in email or "." not in email or email.count("@") != 1:
            messagebox.showerror("Input Error", "Please enter a valid email address.")
            return

        # Unique email
        if any(str(m.get('email', '')).strip().lower() == email.lower() for m in self.members):
            messagebox.showerror("Input Error", "Member with this email already exists.")
            return

        new_member = {
            'id': self.next_member_id,
            'name': name,
            'email': email,
            'phone': phone
        }
        self.members.append(new_member)
        self.next_member_id += 1
        self._save_data()
        self._populate_members_treeview()
        self._clear_member_form()
        messagebox.showinfo("Success", f"Member '{name}' added successfully!")

    def _update_member(self):
        """Updates details of an existing member."""
        if not hasattr(self, 'selected_member_id') or self.selected_member_id is None:
            messagebox.showerror("Error", "No member selected for update.")
            return

        member_id_to_update = self.selected_member_id
        name = self.member_entries['name'].get().strip()
        email = self.member_entries['email'].get().strip()
        phone = self.member_entries['phone'].get().strip()

        if not all([name, email]):
            messagebox.showerror("Input Error", "Name and Email are required for update.")
            return

        if "@" not in email or "." not in email or email.count("@") != 1:
            messagebox.showerror("Input Error", "Please enter a valid email address.")
            return

        if any((str(m.get('email', '')).strip().lower() == email.lower()) and (int(m['id']) != member_id_to_update) for m in self.members):
            messagebox.showerror("Input Error", "Another member with this email already exists.")
            return

        for member in self.members:
            if int(member['id']) == member_id_to_update:
                member['name'] = name
                member['email'] = email
                member['phone'] = phone
                break

        self._save_data()
        self._populate_members_treeview()
        self._clear_member_form()
        messagebox.showinfo("Success", f"Member ID {member_id_to_update} updated successfully!")

    def _delete_member(self):
        """Deletes the selected member from the system."""
        selected_item = self.members_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "No member selected for deletion.")
            return

        member_id_to_delete = int(self.members_tree.item(selected_item, "values")[0])

        if any(int(b['member_id']) == member_id_to_delete and b['return_date'] is None for b in self.borrowings):
            messagebox.showerror("Deletion Error", "This member has outstanding borrowed books and cannot be deleted.")
            return

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Member ID {member_id_to_delete}?"):
            self.members = [m for m in self.members if int(m['id']) != member_id_to_delete]
            self._save_data()
            self._populate_members_treeview()
            self._clear_member_form()
            messagebox.showinfo("Success", f"Member ID {member_id_to_delete} deleted successfully.")

    # Borrow / Return Tab
    def _create_borrow_return_tab(self, parent_frame):
        """Creates UI elements for the Borrow/Return tab."""
        # Borrow Section
        borrow_frame = ttk.LabelFrame(parent_frame, text="Borrow Book", padding="15")
        borrow_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(borrow_frame, text="Select Book:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.borrow_book_combo = ttk.Combobox(borrow_frame, width=50, state="readonly")
        self.borrow_book_combo.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(borrow_frame, text="Select Member:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.borrow_member_combo = ttk.Combobox(borrow_frame, width=50, state="readonly")
        self.borrow_member_combo.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        borrow_frame.grid_columnconfigure(1, weight=1)

        borrow_btn = ttk.Button(borrow_frame, text="Borrow Book", command=self._borrow_book)
        borrow_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Return Section
        return_frame = ttk.LabelFrame(parent_frame, text="Return Book", padding="15")
        return_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(return_frame, text="Select Borrowed Book:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.return_borrowing_combo = ttk.Combobox(return_frame, width=50, state="readonly")
        self.return_borrowing_combo.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        return_frame.grid_columnconfigure(1, weight=1)

        return_btn = ttk.Button(return_frame, text="Return Book", command=self._return_book)
        return_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # Treeview for displaying current borrowings (unreturned)
        ttk.Label(parent_frame, text="Currently Borrowed Books:", font=('Arial', 10, 'bold')).pack(pady=(15, 5), padx=10, anchor="w")
        self.borrow_return_tree = ttk.Treeview(parent_frame, columns=("BorrowID", "Book Title", "Member Name", "Borrow Date"), show="headings")
        self.borrow_return_tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.borrow_return_tree.heading("BorrowID", text="Borrow ID")
        self.borrow_return_tree.heading("Book Title", text="Book Title")
        self.borrow_return_tree.heading("Member Name", text="Member Name")
        self.borrow_return_tree.heading("Borrow Date", text="Borrow Date")

        self.borrow_return_tree.column("BorrowID", width=90, stretch=tk.NO, anchor="center")
        self.borrow_return_tree.column("Book Title", width=280, stretch=tk.YES)
        self.borrow_return_tree.column("Member Name", width=220, stretch=tk.YES)
        self.borrow_return_tree.column("Borrow Date", width=140, stretch=tk.NO, anchor="center")

        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.borrow_return_tree.yview)
        self.borrow_return_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._update_borrow_comboboxes()

    def _update_borrow_comboboxes(self):
        """Populates the book and member comboboxes for borrowing/returning."""
        # Books available to borrow
        available_books = [f"{b['id']} - {b.get('title','')} by {b.get('author','')} (ISBN: {b.get('isbn','')})"
                           for b in self.books if str(b.get('status', 'available')) == 'available']
        self.borrow_book_combo['values'] = available_books
        if available_books:
            self.borrow_book_combo.set(available_books[0])
        else:
            self.borrow_book_combo.set("No books available")

        # Members
        member_options = [f"{m['id']} - {m.get('name','')} ({m.get('email','')})" for m in self.members]
        self.borrow_member_combo['values'] = member_options
        if member_options:
            self.borrow_member_combo.set(member_options[0])
        else:
            self.borrow_member_combo.set("No members registered")

        # Borrowings for returning (only unreturned)
        unreturned_borrowings = []
        for b_rec in self.borrowings:
            if b_rec['return_date'] is None:
                book = next((bk for bk in self.books if int(bk['id']) == int(b_rec['book_id'])), None)
                member = next((m for m in self.members if int(m['id']) == int(b_rec['member_id'])), None)
                if book and member:
                    unreturned_borrowings.append(
                        f"{b_rec['id']} - {book.get('title','')} (by {member.get('name','')})"
                    )
        self.return_borrowing_combo['values'] = unreturned_borrowings
        if unreturned_borrowings:
            self.return_borrowing_combo.set(unreturned_borrowings[0])
        else:
            self.return_borrowing_combo.set("No books currently borrowed")

    def _populate_borrow_return_treeview(self):
        """Populates the Treeview with currently borrowed books."""
        for i in self.borrow_return_tree.get_children():
            self.borrow_return_tree.delete(i)

        for b_rec in self.borrowings:
            if b_rec['return_date'] is None:
                book = next((bk for bk in self.books if int(bk['id']) == int(b_rec['book_id'])), None)
                member = next((m for m in self.members if int(m['id']) == int(b_rec['member_id'])), None)
                if book and member:
                    self.borrow_return_tree.insert("", "end", iid=b_rec['id'], values=(
                        b_rec['id'], book.get('title', ''), member.get('name', ''), b_rec.get('borrow_date', '')
                    ))

    def _borrow_book(self):
        """Handles the borrowing of a book."""
        selected_book_str = self.borrow_book_combo.get()
        selected_member_str = self.borrow_member_combo.get()

        if "No books available" in selected_book_str or "No members registered" in selected_member_str:
            messagebox.showerror("Borrow Error", "Please ensure a book is available and a member is registered.")
            return

        try:
            book_id = int(selected_book_str.split(' ')[0])
            member_id = int(selected_member_str.split(' ')[0])
        except ValueError:
            messagebox.showerror("Borrow Error", "Invalid selection. Please select from the dropdowns.")
            return

        book_to_borrow = next((b for b in self.books if int(b['id']) == book_id), None)
        member_borrowing = next((m for m in self.members if int(m['id']) == member_id), None)

        if not book_to_borrow or not member_borrowing:
            messagebox.showerror("Borrow Error", "Selected book or member not found. Please refresh.")
            return

        if str(book_to_borrow.get('status', 'available')) == 'borrowed':
            messagebox.showwarning("Borrow Warning", f"Book '{book_to_borrow.get('title','')}' is already borrowed.")
            return

        borrow_date = datetime.now().strftime("%Y-%m-%d")

        new_borrowing = {
            'id': self.next_borrowing_id,
            'book_id': book_id,
            'member_id': member_id,
            'borrow_date': borrow_date,
            'return_date': None
        }
        self.borrowings.append(new_borrowing)
        self.next_borrowing_id += 1

        # Update book status
        book_to_borrow['status'] = 'borrowed'

        self._save_data()
        self._populate_books_treeview()
        self._populate_borrow_return_treeview()
        self._populate_all_borrowings_treeview()
        self._update_borrow_comboboxes()
        messagebox.showinfo("Success", f"'{book_to_borrow.get('title','')}' borrowed by '{member_borrowing.get('name','')}'.")

    def _return_book(self):
        """Handles the returning of a book."""
        selected_borrowing_str = self.return_borrowing_combo.get()

        if "No books currently borrowed" in selected_borrowing_str:
            messagebox.showerror("Return Error", "No books are currently borrowed to return.")
            return

        try:
            borrowing_id = int(selected_borrowing_str.split(' ')[0])
        except ValueError:
            messagebox.showerror("Return Error", "Invalid selection. Please select from the dropdown.")
            return

        borrowing_to_return = next((b for b in self.borrowings if int(b['id']) == borrowing_id), None)

        if not borrowing_to_return:
            messagebox.showerror("Return Error", "Selected borrowing record not found. Please refresh.")
            return

        if borrowing_to_return['return_date'] is not None:
            messagebox.showwarning("Return Warning", "This book has already been returned.")
            return

        book_id = int(borrowing_to_return['book_id'])
        book_object = next((b for b in self.books if int(b['id']) == book_id), None)

        if not book_object:
            messagebox.showerror("Return Error", "Associated book not found. Data inconsistency.")
            return

        return_date = datetime.now().strftime("%Y-%m-%d")
        borrowing_to_return['return_date'] = return_date
        book_object['status'] = 'available'

        self._save_data()
        self._populate_books_treeview()
        self._populate_borrow_return_treeview()
        self._populate_all_borrowings_treeview()
        self._update_borrow_comboboxes()
        messagebox.showinfo("Success", f"Book '{book_object.get('title','')}' returned successfully.")

    # All Borrowings Tab
    def _create_all_borrowings_tab(self, parent_frame):
        """Creates UI elements for the All Borrowings tab."""
        ttk.Label(parent_frame, text="Complete Borrowing History:", font=('Arial', 10, 'bold')).pack(pady=(15, 5), padx=10, anchor="w")
        self.all_borrowings_tree = ttk.Treeview(
            parent_frame,
            columns=("BorrowID", "Book Title", "ISBN", "Member Name", "Member Email", "Borrow Date", "Return Date", "Status"),
            show="headings"
        )
        self.all_borrowings_tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.all_borrowings_tree.heading("BorrowID", text="Borrow ID")
        self.all_borrowings_tree.heading("Book Title", text="Book Title")
        self.all_borrowings_tree.heading("ISBN", text="ISBN")
        self.all_borrowings_tree.heading("Member Name", text="Member Name")
        self.all_borrowings_tree.heading("Member Email", text="Member Email")
        self.all_borrowings_tree.heading("Borrow Date", text="Borrow Date")
        self.all_borrowings_tree.heading("Return Date", text="Return Date")
        self.all_borrowings_tree.heading("Status", text="Status")

        self.all_borrowings_tree.column("BorrowID", width=80, stretch=tk.NO, anchor="center")
        self.all_borrowings_tree.column("Book Title", width=200, stretch=tk.YES)
        self.all_borrowings_tree.column("ISBN", width=120, stretch=tk.NO, anchor="center")
        self.all_borrowings_tree.column("Member Name", width=160, stretch=tk.YES)
        self.all_borrowings_tree.column("Member Email", width=220, stretch=tk.YES)
        self.all_borrowings_tree.column("Borrow Date", width=120, stretch=tk.NO, anchor="center")
        self.all_borrowings_tree.column("Return Date", width=120, stretch=tk.NO, anchor="center")
        self.all_borrowings_tree.column("Status", width=100, stretch=tk.NO, anchor="center")

        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.all_borrowings_tree.yview)
        self.all_borrowings_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def _populate_all_borrowings_treeview(self):
        """Populates the Treeview with all borrowing records."""
        for i in self.all_borrowings_tree.get_children():
            self.all_borrowings_tree.delete(i)

        def key_func(x):
            try:
                return x.get('borrow_date', '')
            except Exception:
                return ''
        sorted_borrowings = sorted(self.borrowings, key=key_func, reverse=True)

        for b_rec in sorted_borrowings:
            book = next((bk for bk in self.books if int(bk['id']) == int(b_rec['book_id'])), None)
            member = next((m for m in self.members if int(m['id']) == int(b_rec['member_id'])), None)
            if book and member:
                status = "Returned" if b_rec.get('return_date') else "Borrowed"
                return_date_display = b_rec.get('return_date') if b_rec.get('return_date') else "N/A"
                self.all_borrowings_tree.insert("", "end", iid=b_rec['id'], values=(
                    b_rec['id'], book.get('title', ''), book.get('isbn', ''), member.get('name', ''), member.get('email', ''),
                    b_rec.get('borrow_date', ''), return_date_display, status
                ))


# Start Program 
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
