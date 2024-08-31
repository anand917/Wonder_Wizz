import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',  # Replace with your MySQL root password
    database='User_Details'  # Ensure this matches the database you created
)
cursor = conn.cursor()

# Tkinter main window
root = tk.Tk()
root.title("User Details Form")

# Function to submit details
def submit_details():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    grade = grade_entry.get()
    address = address_text.get("1.0", tk.END)
    membership = membership_var.get()

    # Validate the form fields
    if not (grade and age and name and gender and address and membership):
        messagebox.showerror("Error", "All fields are required.")
        return

    # Store details in the database
    cursor.execute(
        "INSERT INTO users (grade, age, name, gender, address, membership) VALUES (%s, %s, %s, %s, %s, %s)",
        (grade, age, name, gender, address, membership)
    )
    conn.commit()
    messagebox.showinfo("Success", "User details submitted successfully.")

    # Clear form fields after submission
    grade_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    gender_var.set(None)
    address_text.delete("1.0", tk.END)
    membership_var.set(None)

# Form fields

tk.Label(root, text="Name").grid(row=2, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=2, column=1)

tk.Label(root, text="Age").grid(row=1, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1)

tk.Label(root, text="Gender").grid(row=3, column=0)
gender_var = tk.StringVar()
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male").grid(row=3, column=1, sticky=tk.W)
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female").grid(row=3, column=2, sticky=tk.W)
tk.Radiobutton(root, text="Other", variable=gender_var, value="Other").grid(row=3, column=3, sticky=tk.W)


tk.Label(root, text="Grade").grid(row=0, column=0)
grade_entry = tk.Entry(root)
grade_entry.grid(row=0, column=1)


tk.Label(root, text="Address").grid(row=4, column=0)
address_text = tk.Text(root, height=4, width=30)
address_text.grid(row=4, column=1, columnspan=3)

tk.Label(root, text="Membership Plan").grid(row=5, column=0)
membership_var = tk.StringVar()
tk.Radiobutton(root, text="Monthly", variable=membership_var, value="Monthly").grid(row=5, column=1, sticky=tk.W)
tk.Radiobutton(root, text="Yearly", variable=membership_var, value="Yearly").grid(row=5, column=2, sticky=tk.W)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_details)
submit_button.grid(row=6, column=1, columnspan=2)

# Start the main loop
root.mainloop()

# Close the database connection when done
conn.close()
