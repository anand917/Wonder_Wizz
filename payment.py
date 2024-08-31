import tkinter as tk
from tkinter import messagebox
import mysql.connector

class PaymentInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Payment Interface")
        self.window.geometry("400x250")  # Set the window size to 400x250

        # Create a main frame to hold all the widgets
        self.main_frame = tk.Frame(self.window, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        # Create a label frame for the card number input
        self.card_number_frame = tk.LabelFrame(self.main_frame, text="Card Number", bg="white")
        self.card_number_frame.pack(fill="x", padx=10, pady=10)
        self.card_number_label = tk.Label(self.card_number_frame, text="Card Number:")
        self.card_number_label.pack(side=tk.LEFT)
        self.card_number_entry = tk.Entry(self.card_number_frame, width=20)
        self.card_number_entry.pack(side=tk.LEFT, padx=10)

        # Create a label frame for the expiration date input
        self.expiration_date_frame = tk.LabelFrame(self.main_frame, text="Expiration Date", bg="white")
        self.expiration_date_frame.pack(fill="x", padx=10, pady=10)
        self.expiration_date_label = tk.Label(self.expiration_date_frame, text="MM/YYYY:")
        self.expiration_date_label.pack(side=tk.LEFT)
        self.expiration_month_entry = tk.Entry(self.expiration_date_frame, width=2)
        self.expiration_month_entry.pack(side=tk.LEFT, padx=5)
        self.expiration_year_entry = tk.Entry(self.expiration_date_frame, width=4)
        self.expiration_year_entry.pack(side=tk.LEFT, padx=5)

        # Create a label frame for the CVV input
        self.cvv_frame = tk.LabelFrame(self.main_frame, text="CVV", bg="white")
        self.cvv_frame.pack(fill="x", padx=10, pady=10)
        self.cvv_label = tk.Label(self.cvv_frame, text="CVV:")
        self.cvv_label.pack(side=tk.LEFT)
        self.cvv_entry = tk.Entry(self.cvv_frame, width=3)
        self.cvv_entry.pack(side=tk.LEFT, padx=10)

        # Create a submit button
        self.submit_button = tk.Button(self.main_frame, text="Submit Payment", command=self.submit_payment)
        self.submit_button.pack(pady=20)

        # Simulated MySQL database connection
        self.db_config = {
            'user': 'root',
            'password': '1234',
            'host': 'localhost',
            'database': 'payments_DB'
        }
        self.cnx = mysql.connector.connect(**self.db_config)
        self.cursor = self.cnx.cursor()

        # Create table for simulated database
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INT PRIMARY KEY,
                card_number VARCHAR(20),
                expiration_date VARCHAR(10),
                cvv VARCHAR(3)
            )
        """)

        # Insert sample data into the table
        self.cursor.execute("""
            INSERT INTO accounts (id, card_number, expiration_date, cvv)
            VALUES
                (1, '4111111111111111', '12-2025', '123'),
                (2, '5105105105105100', '06-2025', '456'),
                (3, '378282246310005', '02-2025', '789')
                
            ON DUPLICATE KEY UPDATE
                card_number = VALUES(card_number),
                expiration_date = VALUES(expiration_date),
                cvv = VALUES(cvv)
        """)
        self.cnx.commit()

    def submit_payment(self):
        # Get the card number, expiration date, and CVV from the entry fields
        card_number = self.card_number_entry.get()
        expiration_month = self.expiration_month_entry.get()
        expiration_year = self.expiration_year_entry.get()
        cvv = self.cvv_entry.get()

        # Retrieve account details from the simulated database
        self.cursor.execute("SELECT * FROM accounts WHERE id = 1")  # Replace with the actual user ID
        account_details = self.cursor.fetchone()

        # Validate user input against account details
        if not self.validate_card_number(card_number, account_details[1]):
            messagebox.showerror("Invalid Card Number", "Invalid card number")
            return
        if not self.validate_expiration_date(expiration_month, expiration_year, account_details[2]):
            messagebox.showerror("Invalid Expiration Date", "Invalid expiration date")
            return
        if not self.validate_cvv(cvv, account_details[3]):
            messagebox.showerror("Invalid CVV", "Invalid CVV")
            return


        # Process the payment (e.g., update the simulated database with the payment information)
        try:
            print("Payment successful!")
            messagebox.showinfo("Payment Successful", "Payment successful!")
        except Exception as e:
            messagebox.showerror("Payment Error", str(e))

    def validate_card_number(self, input_card_number, stored_card_number):
        # Replace this with your own card number validation logic
        return input_card_number == stored_card_number

    def validate_expiration_date(self, input_expiration_month, input_expiration_year, stored_expiration_date):
        # Replace this with your own expiration date validation logic
        return input_expiration_month == stored_expiration_date[:2] and input_expiration_year == stored_expiration_date[3:]

    def validate_cvv(self, input_cvv, stored_cvv):
        # Replace this with your own CVV validation logic
        return input_cvv == stored_cvv

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    payment_interface = PaymentInterface()
    payment_interface.run()