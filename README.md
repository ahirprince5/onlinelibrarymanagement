# onlinelibrarymanagement
📚 Library Management System (Tkinter + CSV)

A simple Library Management System built with Python Tkinter for GUI and CSV files for data storage.
It provides functionality to manage books, members, borrowing and returning records, with a secure login system.

✨ Features

🔑 Login System (default: admin / admin123)

📖 Book Management

Add, update, delete books

Prevent duplicate ISBNs

Mark availability when borrowed/returned

👥 Member Management

Add, update, delete members

Prevent duplicate emails

📦 Borrow & Return

Borrow books for registered members

Return borrowed books

Auto status update (available/borrowed)

📜 Borrowing History

View all past and current borrowings

Track return status and dates

💾 CSV-based Storage

books.csv, members.csv, borrowings.csv

🛠️ Requirements

Python 3.8+

Tkinter (comes with Python)

How to Run

Clone or download this project.

Make sure Python is installed:

python --version


Run the program:

python library_system.py


Login using:

Username: admin
Password: admin123

📂 File Structure
library_system.py   # Main program
books.csv           # Book records
members.csv         # Member records
borrowings.csv      # Borrow history
README.md           # Documentation

📸 UI Preview

Login Window

Books Tab – manage books

Members Tab – manage members

Borrow/Return Tab – borrow & return books

All Borrowings Tab – view full history

🔮 Future Improvements

Export reports to PDF/Excel

Add search & filter options

Implement due dates and fines

Multi-user authentication
