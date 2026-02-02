import mysql.connector

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="siva123",
    database="atm_db"
)

cursor = db.cursor()


class Personal:
    def __init__(self, name, pan):
        self.Name = name
        self.Pan = pan


class Bank(Personal):
    def __init__(self, name, pan, acno, ifsc, bal):
        super().__init__(name, pan)
        self.Accno = acno
        self.IFSC = ifsc
        self.Balance = bal

    def deposit(self, amt):
        self.Balance += amt
        cursor.execute(
            "UPDATE accounts SET balance=%s WHERE accno=%s",
            (self.Balance, self.Accno)
        )
        db.commit()
        print("Deposit successful.")
        print("Current Balance:", self.Balance)

    def withdraw(self, amt):
        if amt > self.Balance:
            print("Insufficient Funds!")
        else:
            self.Balance -= amt
            cursor.execute(
                "UPDATE accounts SET balance=%s WHERE accno=%s",
                (self.Balance, self.Accno)
            )
            db.commit()
            print("Withdrawal successful.")
            print("Current Balance:", self.Balance)

    def display(self):
        print("\n--- Account Details ---")
        print("Account Number:", self.Accno)
        print("Name:", self.Name)
        print("IFSC Code:", self.IFSC)
        print("PAN Number:", self.Pan)
        print("Balance:", self.Balance)


while True:
    print("\n===== ATM MENU =====")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter Name: ")
        pan = input("Enter PAN: ")
        acno = input("Enter Account Number: ")
        ifsc = input("Enter IFSC Code: ")
        bal = int(input("Enter Initial Balance: "))

        cursor.execute(
            "INSERT INTO accounts VALUES (%s,%s,%s,%s,%s)",
            (acno, name, pan, ifsc, bal)
        )
        db.commit()
        print("Account created successfully!")

    elif choice == "2":
        acno = input("Enter Account Number: ")

        cursor.execute("SELECT * FROM accounts WHERE accno=%s", (acno,))
        data = cursor.fetchone()

        if data:
            user = Bank(data[1], data[2], data[0], data[3], data[4])

            while True:
                print("\n--- ATM Operations ---")
                print("1. Display Account")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Logout")

                op = input("Choose operation: ")

                if op == "1":
                    user.display()
                elif op == "2":
                    amt = int(input("Enter deposit amount: "))
                    user.deposit(amt)
                elif op == "3":
                    amt = int(input("Enter withdrawal amount: "))
                    user.withdraw(amt)
                elif op == "4":
                    print("Logged out successfully.")
                    break
                else:
                    print("Invalid option!")

        else:
            print("Account not found!")

    elif choice == "3":
        print("Thank you for using ATM.")
        break

    else:
        print("Invalid choice!")
