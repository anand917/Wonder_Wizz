import tkinter as tk
from tkinter import messagebox, Button, Label, Entry, Toplevel
import mysql.connector
import random
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='User_Login'
)
cursor = conn.cursor()

# Tkinter main window
root = tk.Tk()
root.title("Login System")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Custom font settings
label_font = ("Arial", 12)
entry_font = ("Arial", 11)
button_font = ("Arial", 12, "bold")

# Function Definitions

def generate_otp(length=6):
    """Generate a random OTP of a given length (default is 6 digits)."""
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

def send_otp_email(to_email, otp):
    """Send an OTP to the user's email address."""
    from_email = "skrhari2020@gmail.com"
    from_password = "aueq tfzq qypp sxee"

    subject = "Your OTP for Email Verification"
    body = f"Your OTP for email verification is {otp}. It is valid for 10 minutes."

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("OTP sent successfully to", to_email)
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        messagebox.showerror("Error", f"Failed to send OTP: {e}")

def open_login_window():
    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x250")
    login_window.configure(bg="#ffffff")

    # Labels and Entries with padding
    Label(login_window, text="Email", font=label_font, bg="#ffffff").pack(pady=(20, 5))
    email_entry = Entry(login_window, font=entry_font)
    email_entry.pack(pady=5, padx=20)

    Label(login_window, text="Password", font=label_font, bg="#ffffff").pack(pady=(10, 5))
    password_entry = Entry(login_window, show="*", font=entry_font)
    password_entry.pack(pady=5, padx=20)

    def login():
        email = email_entry.get()
        password = password_entry.get()

        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        if cursor.fetchone():
            messagebox.showinfo("Success", "Login successful.")
            login_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    Button(login_window, text="Login", font=button_font, bg="#4CAF50", fg="white", command=login).pack(pady=20)

def open_signup_window():
    signup_window = Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry("300x300")
    signup_window.configure(bg="#ffffff")

    Label(signup_window, text="Email", font=label_font, bg="#ffffff").pack(pady=(20, 5))
    email_entry = Entry(signup_window, font=entry_font)
    email_entry.pack(pady=5, padx=20)

    Label(signup_window, text="Password", font=label_font, bg="#ffffff").pack(pady=(10, 5))
    password_entry = Entry(signup_window, show="*", font=entry_font)
    password_entry.pack(pady=5, padx=20)

    def signup():
        email = email_entry.get()
        password = password_entry.get()

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Email already exists.")
        else:
            otp = generate_otp()
            send_otp_email(email, otp)

            messagebox.showinfo("OTP Sent", f"An OTP has been sent to {email}. Please verify it.")
            signup_window.destroy()
            open_otp_verification_window(email, password, otp)

    Button(signup_window, text="Sign Up", font=button_font, bg="#2196F3", fg="white", command=signup).pack(pady=20)

def open_forgot_password_window():
    forgot_password_window = Toplevel(root)
    forgot_password_window.title("Forgot Password")
    forgot_password_window.geometry("300x200")
    forgot_password_window.configure(bg="#ffffff")

    Label(forgot_password_window, text="Email", font=label_font, bg="#ffffff").pack(pady=(20, 5))
    email_entry = Entry(forgot_password_window, font=entry_font)
    email_entry.pack(pady=5, padx=20)

    def forgot_password():
        email = email_entry.get()

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            otp = generate_otp()
            valid_until = datetime.now() + timedelta(minutes=10)
            cursor.execute("UPDATE users SET otp=%s, otp_valid_until=%s WHERE email=%s", (otp, valid_until, email))
            conn.commit()
            send_otp_email(email, otp)
            messagebox.showinfo("OTP Sent", f"An OTP has been sent to {email}.")
            forgot_password_window.destroy()
            open_otp_verification_window(email)
        else:
            messagebox.showerror("Error", "Email not found.")

    Button(forgot_password_window, text="Submit", font=button_font, bg="#FF5722", fg="white", command=forgot_password).pack(pady=20)

def open_otp_verification_window(email, password=None, expected_otp=None):
    otp_verification_window = Toplevel(root)
    otp_verification_window.title("Verify OTP")
    otp_verification_window.geometry("300x200")
    otp_verification_window.configure(bg="#ffffff")

    Label(otp_verification_window, text="Enter OTP", font=label_font, bg="#ffffff").pack(pady=(20, 5))
    otp_entry = Entry(otp_verification_window, font=entry_font)
    otp_entry.pack(pady=5, padx=20)

    def verify_otp():
        otp = otp_entry.get()

        if expected_otp:
            if otp == expected_otp:
                cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
                conn.commit()
                messagebox.showinfo("Success", "OTP verified and account created successfully.")
                otp_verification_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid OTP.")
        else:
            cursor.execute("SELECT * FROM users WHERE email=%s AND otp=%s AND otp_valid_until > NOW()", (email, otp))
            if cursor.fetchone():
                messagebox.showinfo("Success", "OTP verified. You can now set a new password.")
                cursor.execute("UPDATE users SET otp=NULL, otp_valid_until=NULL WHERE email=%s", (email,))
                conn.commit()
                otp_verification_window.destroy()
                open_new_password_window(email)
            else:
                messagebox.showerror("Error", "Invalid or expired OTP.")

    Button(otp_verification_window, text="Verify OTP", font=button_font, bg="#4CAF50", fg="white", command=verify_otp).pack(pady=20)

def open_new_password_window(email):
    new_password_window = Toplevel(root)
    new_password_window.title("New Password")
    new_password_window.geometry("300x200")
    new_password_window.configure(bg="#ffffff")

    Label(new_password_window, text="New Password", font=label_font, bg="#ffffff").pack(pady=(20, 5))
    new_password_entry = Entry(new_password_window, show="*", font=entry_font)
    new_password_entry.pack(pady=5, padx=20)

    def set_new_password():
        new_password = new_password_entry.get()

        if new_password:
            cursor.execute("UPDATE users SET password=%s WHERE email=%s", (new_password, email))
            conn.commit()
            messagebox.showinfo("Success", "Password updated successfully.")
            new_password_window.destroy()
        else:
            messagebox.showerror("Error", "New password cannot be empty.")

    Button(new_password_window, text="Set New Password", font=button_font, bg="#FF5722", fg="white", command=set_new_password).pack(pady=20)

# Main page buttons
Button(root, text="Login", font=button_font, bg="#4CAF50", fg="white", command=open_login_window).pack(pady=20, padx=20)
Button(root, text="Sign Up", font=button_font, bg="#2196F3", fg="white", command=open_signup_window).pack(pady=10, padx=20)
Button(root, text="Forgot Password", font=button_font, bg="#FF5722", fg="white", command=open_forgot_password_window).pack(pady=10, padx=20)

root.mainloop()

# Closing the database connection
conn.close()

