import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os

class LibraryManagementSystem:
    """
    A GUI-based Library Management System using Tkinter and CSV files for data storage.
    Manages books, members, and borrowing/returning operations.
    Optimized for better UI responsiveness.
    """

    def __init__(self, master):
        """
        Initializes the Library Management System GUI.
        Sets up the main window, loads data from CSVs, and creates UI elements.
        """
        self.master = master
        master.title("Colorful Library Management System")
        master.geometry("1000x700") # Set initial window size
        master.resizable(True, True) # Allow resizing

        # Define color scheme
        self.primary_color = "#4A90E2" # Blue
        self.secondary_color = "#8CC63F" # Green
        self.accent_color = "#F5A623" # Orange
        self.bg_color = "#F0F2F5" # Light Gray
        self.text_color = "#333333" # Dark Gray
        self.header_bg = "#E0E5EB" # Lighter Gray for headers

        master.configure(bg=self.bg_color)

        # File paths for CSV data
        self.books_file = "books.csv"
        self.members_file = "members.csv"
        self.borrowings_file = "borrowings.csv"

        # Data storage (lists of dictionaries)
        self.books = []
        self.members = []
        self.borrowings = []

        # Load data on startup
        self._load_data()

        # Generate next available IDs
        self.next_book_id = self._get_next_id(self.books)
        self.next_member_id = self._get_next_id(self.members)
        self.next_borrowing_id = self._get_next_id(self.borrowings)

        self._create_widgets()

    def _load_data(self):
        """Loads data from CSV files into memory."""
        self.books = self._load_csv(self.books_file)
        self.members = self._load_csv(self.members_file)
        self.borrowings = self._load_csv(self.borrowings_file)

    def _save_data(self):
        """Saves current data from memory to CSV files."""
        self._save_csv(self.books_file, self.books)
        self._save_csv(self.members_file, self.members)
        self._save_csv(self.borrowings_file, self.borrowings)

    def _load_csv(self, filename):
        """Helper to load data from a single CSV file."""
        data = []
        if os.path.exists(filename):
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert ID fields to int, year to int, handle None for return_date
                    row['id'] = int(row['id'])
                    if 'book_id' in row: row['book_id'] = int(row['book_id'])
                    if 'member_id' in row: row['member_id'] = int(row['member_id'])
                    if 'published_year' in row and row['published_year']:
                        row['published_year'] = int(row['published_year'])
                    if 'return_date' in row and row['return_date'] == 'None':
                        row['return_date'] = None
                    data.append(row)
        return data

    def _save_csv(self, filename, data):
        """Helper to save data to a single CSV file."""
        if not data:
            # If no data, just create an empty file with headers
            headers = []
            if filename == self.books_file:
                headers = ['id', 'title', 'author', 'isbn', 'published_year', 'status']
            elif filename == self.members_file:
                headers = ['id', 'name', 'email', 'phone']
            elif filename == self.borrowings_file:
                headers = ['id', 'book_id', 'member_id', 'borrow_date', 'return_date']
            
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
            return

        # Ensure all dictionaries have the same keys for DictWriter
        # This assumes the first item's keys define the header
        headers = list(data[0].keys()) if data else []
        
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

    def _get_next_id(self, data_list):
        """Generates the next available ID for a list of dictionaries."""
        if not data_list:
            return 1
        return max(item['id'] for item in data_list) + 1

    def _create_widgets(self):
        """Creates all the GUI elements for the application."""
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Style for ttk widgets
        style = ttk.Style()
        style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'
        
        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.primary_color, foreground="white",
                        font=('Inter', 10, 'bold'), padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", self.accent_color)],
                  foreground=[("selected", "white")])
        
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=('Inter', 10))
        style.configure("TButton", background=self.primary_color, foreground="white",
                        font=('Inter', 10, 'bold'), padding=5, relief="raised")
        style.map("TButton", background=[('active', self.accent_color)])

        style.configure("Treeview.Heading", font=('Inter', 10, 'bold'), background=self.header_bg, foreground=self.text_color)
        style.configure("Treeview", font=('Inter', 9), rowheight=25, background="white", foreground=self.text_color, fieldbackground="white")
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

        # Initial population of Treeviews (and force update for responsiveness)
        self._populate_books_treeview()
        self.master.update_idletasks()
        self._populate_members_treeview()
        self.master.update_idletasks()
        self._populate_borrow_return_treeview()
        self.master.update_idletasks()
        self._populate_all_borrowings_treeview()
        self.master.update_idletasks()

        # Bind tab change event to refresh relevant data
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
        self.master.update_idletasks() # Ensure UI updates after tab change

    # --- Books Tab UI ---
    def _create_books_tab(self, parent_frame):
        """Creates UI elements for the Books tab."""
        # Input Form Frame
        form_frame = ttk.LabelFrame(parent_frame, text="Book Details", padding="15", style="TFrame")
        form_frame.pack(pady=10, padx=10, fill="x")

        # Labels and Entry widgets for book details
        labels = ["Title:", "Author:", "ISBN:", "Published Year:"]
        self.book_entries = {}
        for i, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=5, padx=5)
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
            self.book_entries[label_text.replace(":", "").strip().lower().replace(" ", "_")] = entry
        
        # Configure column weights for responsiveness
        form_frame.grid_columnconfigure(1, weight=1)

        # Buttons for Add/Update/Clear
        button_frame = ttk.Frame(form_frame, style="TFrame")
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)

        self.add_book_btn = ttk.Button(button_frame, text="Add Book", command=self._add_book, style="TButton")
        self.add_book_btn.pack(side="left", padx=5)

        self.update_book_btn = ttk.Button(button_frame, text="Update Book", command=self._update_book, state=tk.DISABLED, style="TButton")
        self.update_book_btn.pack(side="left", padx=5)

        self.clear_book_form_btn = ttk.Button(button_frame, text="Clear Form", command=self._clear_book_form, style="TButton")
        self.clear_book_form_btn.pack(side="left", padx=5)

        # Treeview for displaying books
        self.books_tree = ttk.Treeview(parent_frame, columns=("ID", "Title", "Author", "ISBN", "Year", "Status"), show="headings")
        self.books_tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Define column headings and widths
        self.books_tree.heading("ID", text="ID")
        self.books_tree.heading("Title", text="Title")
        self.books_tree.heading("Author", text="Author")
        self.books_tree.heading("ISBN", text="ISBN")
        self.books_tree.heading("Year", text="Year")
        self.books_tree.heading("Status", text="Status")

        self.books_tree.column("ID", width=50, stretch=tk.NO, anchor="center")
        self.books_tree.column("Title", width=200, stretch=tk.YES)
        self.books_tree.column("Author", width=150, stretch=tk.YES)
        self.books_tree.column("ISBN", width=100, stretch=tk.NO, anchor="center")
        self.books_tree.column("Year", width=70, stretch=tk.NO, anchor="center")
        self.books_tree.column("Status", width=80, stretch=tk.NO, anchor="center")

        # Bind selection event to populate form for editing
        self.books_tree.bind("<<TreeviewSelect>>", self._on_book_select)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Buttons for Delete
        action_button_frame = ttk.Frame(parent_frame, style="TFrame")
        action_button_frame.pack(pady=5, padx=10, fill="x", anchor="e")
        
        self.delete_book_btn = ttk.Button(action_button_frame, text="Delete Selected Book", command=self._delete_book, style="TButton")
        self.delete_book_btn.pack(side="right", padx=5)

    def _populate_books_treeview(self):
        """Populates the books Treeview with current data."""
        for i in self.books_tree.get_children():
            self.books_tree.delete(i)
        
        for book in self.books:
            self.books_tree.insert("", "end", iid=book['id'], values=(
                book['id'], book['title'], book['author'], book['isbn'],
                book['published_year'], book['status'].capitalize()
            ))
        self.master.update_idletasks() # Update UI after populating

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
            self._clear_book_form() # Clear first to ensure no old data remains
            self.book_entries['title'].insert(0, selected_book['title'])
            self.book_entries['author'].insert(0, selected_book['author'])
            self.book_entries['isbn'].insert(0, selected_book['isbn'])
            self.book_entries['published_year'].insert(0, selected_book['published_year'])
            self.selected_book_id = book_id # Store for update operation

            self.add_book_btn.config(state=tk.DISABLED)
            self.update_book_btn.config(state=tk.NORMAL)
        else:
            self._clear_book_form()
            self.add_book_btn.config(state=tk.NORMAL)
            self.update_book_btn.config(state=tk.DISABLED)
        self.master.update_idletasks() # Update UI after selection

    def _clear_book_form(self):
        """Clears all entry fields in the book form."""
        for entry in self.book_entries.values():
            entry.delete(0, tk.END)
        self.selected_book_id = None
        self.add_book_btn.config(state=tk.NORMAL)
        self.update_book_btn.config(state=tk.DISABLED)
        self.books_tree.selection_remove(self.books_tree.focus()) # Deselect item in treeview
        self.master.update_idletasks() # Update UI after clearing

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
            if not (1000 <= published_year <= datetime.now().year + 5): # Reasonable year range
                 messagebox.showerror("Input Error", "Published year must be a valid year.")
                 return
        except ValueError:
            messagebox.showerror("Input Error", "Published Year must be a number.")
            return

        # Check for unique ISBN
        if any(book['isbn'] == isbn for book in self.books):
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
        self.master.update_idletasks() # Ensure UI updates after add

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

        # Check for unique ISBN, excluding the current book being updated
        if any(book['isbn'] == isbn and book['id'] != book_id_to_update for book in self.books):
            messagebox.showerror("Input Error", "Another book with this ISBN already exists.")
            return

        for book in self.books:
            if book['id'] == book_id_to_update:
                book['title'] = title
                book['author'] = author
                book['isbn'] = isbn
                book['published_year'] = published_year
                break
        
        self._save_data()
        self._populate_books_treeview()
        self._clear_book_form()
        messagebox.showinfo("Success", f"Book ID {book_id_to_update} updated successfully!")
        self.master.update_idletasks() # Ensure UI updates after update

    def _delete_book(self):
        """Deletes the selected book from the system."""
        selected_item = self.books_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "No book selected for deletion.")
            return

        book_id_to_delete = int(self.books_tree.item(selected_item, "values")[0])
        
        # Check if the book is currently borrowed
        if any(b['book_id'] == book_id_to_delete and b['return_date'] is None for b in self.borrowings):
            messagebox.showerror("Deletion Error", "This book is currently borrowed and cannot be deleted.")
            return

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Book ID {book_id_to_delete}?"):
            self.books = [book for book in self.books if book['id'] != book_id_to_delete]
            self._save_data()
            self._populate_books_treeview()
            self._clear_book_form() # Clear form in case deleted book was being edited
            messagebox.showinfo("Success", f"Book ID {book_id_to_delete} deleted successfully.")
            self.master.update_idletasks() # Ensure UI updates after delete

    # --- Members Tab UI ---
    def _create_members_tab(self, parent_frame):
        """Creates UI elements for the Members tab."""
        # Input Form Frame
        form_frame = ttk.LabelFrame(parent_frame, text="Member Details", padding="15", style="TFrame")
        form_frame.pack(pady=10, padx=10, fill="x")

        # Labels and Entry widgets for member details
        labels = ["Name:", "Email:", "Phone (Optional):"]
        self.member_entries = {}
        for i, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=5, padx=5)
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
            self.member_entries[label_text.replace(":", "").replace("(Optional)", "").strip().lower().replace(" ", "_")] = entry
        
        form_frame.grid_columnconfigure(1, weight=1)

        # Buttons for Add/Update/Clear
        button_frame = ttk.Frame(form_frame, style="TFrame")
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)

        self.add_member_btn = ttk.Button(button_frame, text="Add Member", command=self._add_member, style="TButton")
        self.add_member_btn.pack(side="left", padx=5)

        self.update_member_btn = ttk.Button(button_frame, text="Update Member", command=self._update_member, state=tk.DISABLED, style="TButton")
        self.update_member_btn.pack(side="left", padx=5)

        self.clear_member_form_btn = ttk.Button(button_frame, text="Clear Form", command=self._clear_member_form, style="TButton")
        self.clear_member_form_btn.pack(side="left", padx=5)

        # Treeview for displaying members
        self.members_tree = ttk.Treeview(parent_frame, columns=("ID", "Name", "Email", "Phone"), show="headings")
        self.members_tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Define column headings and widths
        self.members_tree.heading("ID", text="ID")
        self.members_tree.heading("Name", text="Name")
        self.members_tree.heading("Email", text="Email")
        self.members_tree.heading("Phone", text="Phone")

        self.members_tree.column("ID", width=50, stretch=tk.NO, anchor="center")
        self.members_tree.column("Name", width=200, stretch=tk.YES)
        self.members_tree.column("Email", width=250, stretch=tk.YES)
        self.members_tree.column("Phone", width=100, stretch=tk.NO, anchor="center")

        # Bind selection event to populate form for editing
        self.members_tree.bind("<<TreeviewSelect>>", self._on_member_select)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Buttons for Delete
        action_button_frame = ttk.Frame(parent_frame, style="TFrame")
        action_button_frame.pack(pady=5, padx=10, fill="x", anchor="e")
        
        self.delete_member_btn = ttk.Button(action_button_frame, text="Delete Selected Member", command=self._delete_member, style="TButton")
        self.delete_member_btn.pack(side="right", padx=5)

    def _populate_members_treeview(self):
        """Populates the members Treeview with current data."""
        for i in self.members_tree.get_children():
            self.members_tree.delete(i)
        
        for member in self.members:
            self.members_tree.insert("", "end", iid=member['id'], values=(
                member['id'], member['name'], member['email'], member['phone']
            ))
        self.master.update_idletasks() # Update UI after populating

    def _on_member_select(self, event):
        """Populates the member form when a member is selected in the Treeview."""
        selected_item = self.members_tree.focus()
        if not selected_item:
            self._clear_member_form()
            self.update_member_btn.config(state=tk.DISABLED)
            return

        member_id = int(self.members_tree.item(selected_item, "values")[0])
        selected_member = next((m for m in self.members if m['id'] == member_id), None)

        if selected_member:
            self._clear_member_form()
            self.member_entries['name'].insert(0, selected_member['name'])
            self.member_entries['email'].insert(0, selected_member['email'])
            self.member_entries['phone'].insert(0, selected_member['phone'])
            self.selected_member_id = member_id # Store for update operation

            self.add_member_btn.config(state=tk.DISABLED)
            self.update_member_btn.config(state=tk.NORMAL)
        else:
            self._clear_member_form()
            self.add_member_btn.config(state=tk.NORMAL)
            self.update_member_btn.config(state=tk.DISABLED)
        self.master.update_idletasks() # Update UI after selection

    def _clear_member_form(self):
        """Clears all entry fields in the member form."""
        for entry in self.member_entries.values():
            entry.delete(0, tk.END)
        self.selected_member_id = None
        self.add_member_btn.config(state=tk.NORMAL)
        self.update_member_btn.config(state=tk.DISABLED)
        self.members_tree.selection_remove(self.members_tree.focus())
        self.master.update_idletasks() # Update UI after clearing

    def _add_member(self):
        """Adds a new member to the system."""
        name = self.member_entries['name'].get().strip()
        email = self.member_entries['email'].get().strip()
        phone = self.member_entries['phone'].get().strip() # Phone is optional

        if not all([name, email]):
            messagebox.showerror("Input Error", "Name and Email are required.")
            return

        # Basic email format check
        if "@" not in email or "." not in email:
            messagebox.showerror("Input Error", "Please enter a valid email address.")
            return

        # Check for unique email
        if any(member['email'] == email for member in self.members):
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
        self.master.update_idletasks() # Ensure UI updates after add

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
        
        if "@" not in email or "." not in email:
            messagebox.showerror("Input Error", "Please enter a valid email address.")
            return

        # Check for unique email, excluding the current member being updated
        if any(member['email'] == email and member['id'] != member_id_to_update for member in self.members):
            messagebox.showerror("Input Error", "Another member with this email already exists.")
            return

        for member in self.members:
            if member['id'] == member_id_to_update:
                member['name'] = name
                member['email'] = email
                member['phone'] = phone
                break
        
        self._save_data()
        self._populate_members_treeview()
        self._clear_member_form()
        messagebox.showinfo("Success", f"Member ID {member_id_to_update} updated successfully!")
        self.master.update_idletasks() # Ensure UI updates after update

    def _delete_member(self):
        """Deletes the selected member from the system."""
        selected_item = self.members_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "No member selected for deletion.")
            return

        member_id_to_delete = int(self.members_tree.item(selected_item, "values")[0])
        
        # Check if the member has any outstanding borrowings
        if any(b['member_id'] == member_id_to_delete and b['return_date'] is None for b in self.borrowings):
            messagebox.showerror("Deletion Error", "This member has outstanding borrowed books and cannot be deleted.")
            return

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Member ID {member_id_to_delete}?"):
            self.members = [member for member in self.members if member['id'] != member_id_to_delete]
            self._save_data()
            self._populate_members_treeview()
            self._clear_member_form()
            messagebox.showinfo("Success", f"Member ID {member_id_to_delete} deleted successfully.")
            self.master.update_idletasks() # Ensure UI updates after delete

    # --- Borrow/Return Tab UI ---
    def _create_borrow_return_tab(self, parent_frame):
        """Creates UI elements for the Borrow/Return tab."""
        # Borrow Section
        borrow_frame = ttk.LabelFrame(parent_frame, text="Borrow Book", padding="15", style="TFrame")
        borrow_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(borrow_frame, text="Select Book:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.borrow_book_combo = ttk.Combobox(borrow_frame, width=50, state="readonly")
        self.borrow_book_combo.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        
        ttk.Label(borrow_frame, text="Select Member:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.borrow_member_combo = ttk.Combobox(borrow_frame, width=50, state="readonly")
        self.borrow_member_combo.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        borrow_frame.grid_columnconfigure(1, weight=1)

        borrow_btn = ttk.Button(borrow_frame, text="Borrow Book", command=self._borrow_book, style="TButton")
        borrow_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Return Section
        return_frame = ttk.LabelFrame(parent_frame, text="Return Book", padding="15", style="TFrame")
        return_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(return_frame, text="Select Borrowed Book:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.return_borrowing_combo = ttk.Combobox(return_frame, width=50, state="readonly")
        self.return_borrowing_combo.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        
        return_frame.grid_columnconfigure(1, weight=1)

        return_btn = ttk.Button(return_frame, text="Return Book", command=self._return_book, style="TButton")
        return_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # Treeview for displaying current borrowings (unreturned)
        ttk.Label(parent_frame, text="Currently Borrowed Books:", font=('Inter', 10, 'bold')).pack(pady=(15, 5), padx=10, anchor="w")
        self.borrow_return_tree = ttk.Treeview(parent_frame, columns=("BorrowID", "Book Title", "Member Name", "Borrow Date"), show="headings")
        self.borrow_return_tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.borrow_return_tree.heading("BorrowID", text="Borrow ID")
        self.borrow_return_tree.heading("Book Title", text="Book Title")
        self.borrow_return_tree.heading("Member Name", text="Member Name")
        self.borrow_return_tree.heading("Borrow Date", text="Borrow Date")

        self.borrow_return_tree.column("BorrowID", width=80, stretch=tk.NO, anchor="center")
        self.borrow_return_tree.column("Book Title", width=250, stretch=tk.YES)
        self.borrow_return_tree.column("Member Name", width=200, stretch=tk.YES)
        self.borrow_return_tree.column("Borrow Date", width=120, stretch=tk.NO, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.borrow_return_tree.yview)
        self.borrow_return_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._update_borrow_comboboxes()

    def _update_borrow_comboboxes(self):
        """Populates the book and member comboboxes for borrowing."""
        # Books for borrowing (only available ones)
        available_books = [f"{b['id']} - {b['title']} by {b['author']} (ISBN: {b['isbn']})" for b in self.books if b['status'] == 'available']
        self.borrow_book_combo['values'] = available_books
        if available_books:
            self.borrow_book_combo.set(available_books[0])
        else:
            self.borrow_book_combo.set("No books available")

        # Members for borrowing
        member_options = [f"{m['id']} - {m['name']} ({m['email']})" for m in self.members]
        self.borrow_member_combo['values'] = member_options
        if member_options:
            self.borrow_member_combo.set(member_options[0])
        else:
            self.borrow_member_combo.set("No members registered")

        # Borrowings for returning (only unreturned ones)
        unreturned_borrowings = []
        for b_rec in self.borrowings:
            if b_rec['return_date'] is None:
                book = next((bk for bk in self.books if bk['id'] == b_rec['book_id']), None)
                member = next((m for m in self.members if m['id'] == b_rec['member_id']), None)
                if book and member:
                    unreturned_borrowings.append(
                        f"{b_rec['id']} - {book['title']} (by {member['name']})"
                    )
        self.return_borrowing_combo['values'] = unreturned_borrowings
        if unreturned_borrowings:
            self.return_borrowing_combo.set(unreturned_borrowings[0])
        else:
            self.return_borrowing_combo.set("No books currently borrowed")
        self.master.update_idletasks() # Update UI after comboboxes are populated

    def _populate_borrow_return_treeview(self):
        """Populates the Treeview with currently borrowed books."""
        for i in self.borrow_return_tree.get_children():
            self.borrow_return_tree.delete(i)
        
        for b_rec in self.borrowings:
            if b_rec['return_date'] is None: # Only show unreturned books
                book = next((bk for bk in self.books if bk['id'] == b_rec['book_id']), None)
                member = next((m for m in self.members if m['id'] == b_rec['member_id']), None)
                
                if book and member:
                    self.borrow_return_tree.insert("", "end", iid=b_rec['id'], values=(
                        b_rec['id'], book['title'], member['name'], b_rec['borrow_date']
                    ))
        self.master.update_idletasks() # Update UI after populating

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

        # Find the book and member objects
        book_to_borrow = next((b for b in self.books if b['id'] == book_id), None)
        member_borrowing = next((m for m in self.members if m['id'] == member_id), None)

        if not book_to_borrow or not member_borrowing:
            messagebox.showerror("Borrow Error", "Selected book or member not found. Please refresh.")
            return

        if book_to_borrow['status'] == 'borrowed':
            messagebox.showwarning("Borrow Warning", f"Book '{book_to_borrow['title']}' is already borrowed.")
            return

        borrow_date = datetime.now().strftime("%Y-%m-%d")

        new_borrowing = {
            'id': self.next_borrowing_id,
            'book_id': book_id,
            'member_id': member_id,
            'borrow_date': borrow_date,
            'return_date': None # Mark as not returned yet
        }
        self.borrowings.append(new_borrowing)
        self.next_borrowing_id += 1

        # Update book status
        book_to_borrow['status'] = 'borrowed'

        self._save_data()
        self._populate_books_treeview() # Book status changed
        self._populate_borrow_return_treeview()
        self._populate_all_borrowings_treeview()
        self._update_borrow_comboboxes() # Update available books/borrowings
        messagebox.showinfo("Success", f"'{book_to_borrow['title']}' borrowed by '{member_borrowing['name']}'.")
        self.master.update_idletasks() # Ensure UI updates after borrow

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

        borrowing_to_return = next((b for b in self.borrowings if b['id'] == borrowing_id), None)

        if not borrowing_to_return:
            messagebox.showerror("Return Error", "Selected borrowing record not found. Please refresh.")
            return
        
        if borrowing_to_return['return_date'] is not None:
            messagebox.showwarning("Return Warning", "This book has already been returned.")
            return

        book_id = borrowing_to_return['book_id']
        book_object = next((b for b in self.books if b['id'] == book_id), None)

        if not book_object:
            messagebox.showerror("Return Error", "Associated book not found. Data inconsistency.")
            return

        return_date = datetime.now().strftime("%Y-%m-%d")
        borrowing_to_return['return_date'] = return_date
        book_object['status'] = 'available' # Update book status

        self._save_data()
        self._populate_books_treeview() # Book status changed
        self._populate_borrow_return_treeview()
        self._populate_all_borrowings_treeview()
        self._update_borrow_comboboxes() # Update available books/borrowings
        messagebox.showinfo("Success", f"Book '{book_object['title']}' returned successfully.")
        self.master.update_idletasks() # Ensure UI updates after return

    # --- All Borrowings Tab UI ---
    def _create_all_borrowings_tab(self, parent_frame):
        """Creates UI elements for the All Borrowings tab."""
        ttk.Label(parent_frame, text="Complete Borrowing History:", font=('Inter', 10, 'bold')).pack(pady=(15, 5), padx=10, anchor="w")
        self.all_borrowings_tree = ttk.Treeview(parent_frame, columns=("BorrowID", "Book Title", "ISBN", "Member Name", "Member Email", "Borrow Date", "Return Date", "Status"), show="headings")
        self.all_borrowings_tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.all_borrowings_tree.heading("BorrowID", text="Borrow ID")
        self.all_borrowings_tree.heading("Book Title", text="Book Title")
        self.all_borrowings_tree.heading("ISBN", text="ISBN")
        self.all_borrowings_tree.heading("Member Name", text="Member Name")
        self.all_borrowings_tree.heading("Member Email", text="Member Email")
        self.all_borrowings_tree.heading("Borrow Date", text="Borrow Date")
        self.all_borrowings_tree.heading("Return Date", text="Return Date")
        self.all_borrowings_tree.heading("Status", text="Status")

        self.all_borrowings_tree.column("BorrowID", width=70, stretch=tk.NO, anchor="center")
        self.all_borrowings_tree.column("Book Title", width=180, stretch=tk.YES)
        self.all_borrowings_tree.column("ISBN", width=100, stretch=tk.NO, anchor="center")
        self.all_borrowings_tree.column("Member Name", width=150, stretch=tk.YES)
        self.all_borrowings_tree.column("Member Email", width=200, stretch=tk.YES)
        self.all_borrowings_tree.column("Borrow Date", width=100, stretch=tk.NO, anchor="center")
        self.all_borrowings_tree.column("Return Date", width=100, stretch=tk.NO, anchor="center")
        self.all_borrowings_tree.column("Status", width=80, stretch=tk.NO, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.all_borrowings_tree.yview)
        self.all_borrowings_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def _populate_all_borrowings_treeview(self):
        """Populates the Treeview with all borrowing records."""
        for i in self.all_borrowings_tree.get_children():
            self.all_borrowings_tree.delete(i)
        
        # Sort borrowings by borrow_date descending
        sorted_borrowings = sorted(self.borrowings, key=lambda x: x['borrow_date'], reverse=True)

        for b_rec in sorted_borrowings:
            book = next((bk for bk in self.books if bk['id'] == b_rec['book_id']), None)
            member = next((m for m in self.members if m['id'] == b_rec['member_id']), None)
            
            if book and member:
                status = "Returned" if b_rec['return_date'] else "Borrowed"
                return_date_display = b_rec['return_date'] if b_rec['return_date'] else "N/A"
                self.all_borrowings_tree.insert("", "end", iid=b_rec['id'], values=(
                    b_rec['id'], book['title'], book['isbn'], member['name'], member['email'],
                    b_rec['borrow_date'], return_date_display, status
                ))
        self.master.update_idletasks() # Update UI after populating

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
