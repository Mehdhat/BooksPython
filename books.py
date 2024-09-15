import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Function to connect to the MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="",  # Replace with your MySQL password
            database="bookdb"  # Replace with your MySQL database name
        )
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            title VARCHAR(255) NOT NULL,
                            author VARCHAR(255) NOT NULL,
                            year INT NOT NULL,
                            isbn VARCHAR(255) NOT NULL)''')
        connection.commit()
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Connection Error", f"Error: {err}")
        return None

# Function to insert a book into the database
def add_book():
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()
    isbn = entry_isbn.get()

    if title and author and year and isbn:
        try:
            year = int(year)  # Year must be an integer
        except ValueError:
            messagebox.showerror("Input Error", "Year must be an integer.")
            return

        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO books (title, author, year, isbn) VALUES (%s, %s, %s, %s)",
                               (title, author, year, isbn))
                connection.commit()
                messagebox.showinfo("Success", "Book added successfully!")
                clear_fields()
                fetch_inventory()  # Refresh Treeview
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to add book: {err}")
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Connection Error", "Failed to connect to the database.")
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

# Function to fetch inventory data from the database
def fetch_inventory():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()

            # Clear previous data in the treeview
            tree.delete(*tree.get_children())

            if len(rows) != 0:
                for row in rows:
                    tree.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("No Data", "No records found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching data: {err}")
        finally:
            cursor.close()
            connection.close()

# Function to delete a selected book from the database
def delete_book():
    selected_item = tree.selection()
    if selected_item:
        book_id = tree.item(selected_item)['values'][0]  # Get the ID of the selected book

        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
                connection.commit()
                messagebox.showinfo("Success", "Book deleted successfully!")
                fetch_inventory()  # Refresh Treeview
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to delete book: {err}")
            finally:
                cursor.close()
                connection.close()
    else:
        messagebox.showwarning("Selection Error", "Please select a book to delete.")

# Function to clear input fields
def clear_fields():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_isbn.delete(0, tk.END)

# Function to select a book from the Treeview and load its details into the form for editing
def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        book = tree.item(selected_item)['values']
        entry_title.delete(0, tk.END)
        entry_title.insert(tk.END, book[1])
        entry_author.delete(0, tk.END)
        entry_author.insert(tk.END, book[2])
        entry_year.delete(0, tk.END)
        entry_year.insert(tk.END, book[3])
        entry_isbn.delete(0, tk.END)
        entry_isbn.insert(tk.END, book[4])

        global selected_book_id
        selected_book_id = book[0]  # Store the selected book ID for updating

# Function to edit/update the selected book in the database
def edit_book():
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()
    isbn = entry_isbn.get()

    if title and author and year and isbn:
        try:
            year = int(year)  # Year must be an integer
        except ValueError:
            messagebox.showerror("Input Error", "Year must be an integer.")
            return

        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("UPDATE books SET title = %s, author = %s, year = %s, isbn = %s WHERE id = %s",
                               (title, author, year, isbn, selected_book_id))
                connection.commit()
                messagebox.showinfo("Success", "Book updated successfully!")
                clear_fields()
                fetch_inventory()  # Refresh Treeview
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update book: {err}")
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Connection Error", "Failed to connect to the database.")
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

# Create the main window
root = tk.Tk()
root.title("Bookstore Inventory Management")
root.geometry("700x700")
root.configure(bg="#f0f0f0")
# Set the icon for the application
root.iconbitmap(r'C:\Users\Admin\Downloads\pythonProject1\pngtree-white-bubble-speech-png-image_10162559.ico')  # Replace 'your_icon.ico' with the actual file name


# Create a frame for the form
frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame.pack(pady=20)

# Create labels and entry fields
tk.Label(frame, text="Book Title:", bg="#ffffff", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
entry_title = tk.Entry(frame, font=("Arial", 12))
entry_title.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Author:", bg="#ffffff", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
entry_author = tk.Entry(frame, font=("Arial", 12))
entry_author.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Year:", bg="#ffffff", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
entry_year = tk.Entry(frame, font=("Arial", 12))
entry_year.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame, text="ISBN:", bg="#ffffff", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
entry_isbn = tk.Entry(frame, font=("Arial", 12))
entry_isbn.grid(row=3, column=1, padx=10, pady=5)

# Buttons for different actions
button_frame = tk.Frame(frame, bg="#ffffff")
button_frame.grid(row=4, column=0, columnspan=2, pady=20)

add_button = tk.Button(button_frame, text="Add Book", command=add_book, bg="#001f41", fg="#ffffff", font=("Arial", 12), padx=20, pady=5)
add_button.grid(row=0, column=0, padx=10)

edit_button = tk.Button(button_frame, text="Edit Book", command=edit_book, bg="#008000", fg="#ffffff", font=("Arial", 12), padx=20, pady=5)
edit_button.grid(row=0, column=1, padx=10)

delete_button = tk.Button(button_frame, text="Delete Book", command=delete_book, bg="#ff0000", fg="#ffffff", font=("Arial", 12), padx=20, pady=5)
delete_button.grid(row=0, column=2, padx=10)

clear_button = tk.Button(button_frame, text="Clear", command=clear_fields, bg="#001f41", fg="#ffffff", font=("Arial", 12), padx=20, pady=5)
clear_button.grid(row=0, column=3, padx=10)

# Create a frame for the treeview
tree_frame = tk.Frame(root)
tree_frame.pack(pady=20)

# Create the Treeview widget
tree = ttk.Treeview(tree_frame, columns=("ID", "Title", "Author", "Year", "ISBN"), show='headings', height=8)
tree.heading("ID", text="ID")
tree.heading("Title", text="Title")
tree.heading("Author", text="Author")
tree.heading("Year", text="Year")
tree.heading("ISBN", text="ISBN")
tree.column("ID", anchor=tk.CENTER, width=50)
tree.column("Title", anchor=tk.CENTER, width=150)
tree.column("Author", anchor=tk.CENTER, width=150)
tree.column("Year", anchor=tk.CENTER, width=100)
tree.column("ISBN", anchor=tk.CENTER, width=100)
tree.pack()

# Function to select a book from the Treeview and load its details into the form for editing
def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        book = tree.item(selected_item)['values']
        entry_title.delete(0, tk.END)
        entry_title.insert(tk.END, book[1])
        entry_author.delete(0, tk.END)
        entry_author.insert(tk.END, book[2])
        entry_year.delete(0, tk.END)
        entry_year.insert(tk.END, book[3])
        entry_isbn.delete(0, tk.END)
        entry_isbn.insert(tk.END, book[4])

        global selected_book_id
        selected_book_id = book[0]  # Store the selected book ID for updating

# Bind the Treeview selection event to load the book details for editing
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Fetch inventory from the database and populate the treeview when the app starts
fetch_inventory()

# Start the main loop
root.mainloop()
