import random
from datetime import date, datetime, timedelta
import mysql.connector as mysql

myAccount_Number = None

db = mysql.connect(
    host='localhost',
    user='root',
    database="bank",
    password="root",
    port=3306
)

cursor = db.cursor(buffered=True)


# Commands
# cursor.execute("CREATE TABLE IF NOT EXISTS customer (account_number INT PRIMARY KEY, name VARCHAR(255), username VARCHAR(255), age INT, address VARCHAR(255), phone VARCHAR(10), balance INT, verification_way VARCHAR(255), verification_number VARCHAR(255), password VARCHAR(4))")
# cursor.execute("CREATE TABLE IF NOT EXISTS loan_details (account_number INT PRIMARY KEY, loan_type VARCHAR(255), loan_amount INT, remaining_amount INT, paid_amount INT, amount_to_pay INT, loan_date DATE, premium_date DATE, repayment_type VARCHAR(255), final_payment_date DATE, college_name VARCHAR(255), college_address VARCHAR(255), graduate_year DATE, FOREIGN KEY(account_number) REFERENCES customer(account_number))")
# cursor.execute("CREATE TABLE IF NOT EXISTS transaction_history (account_number INT, name VARCHAR(255), username VARCHAR(255), description VARCHAR(255), debit FLOAT(10,2), credit FLOAT(10,2), balance FLOAT(10,2), transaction_date DATE, FOREIGN KEY (account_number) REFERENCES customer (account_number))")

# db.commit()

# exit()


def checkAccountNumber(account_number):

    cursor.execute(
        "SELECT account_number FROM customer WHERE account_number = %s", (account_number,))

    if(cursor.fetchone() != None):
        account_number = random.randint(1000000, 9999999)
        checkAccountNumber(account_number)

    return account_number


def get_details():
    print("Enter the details of the customer")

    # Generate random account number for every users

    account_number = random.randint(1000000, 9999999)

    checkAccountNumber(account_number)

    name = None
    username = None
    age = None
    address = None
    phone = None
    verification_number = None
    verification_way = None
    password = None

    while(True):
        if name == None:
            name = input("Enter the name of the customer: ")
            if name == "" or name.isspace():
                print("Name cannot be empty")
                name = None
                continue
        if username == None and (name != None or name != ""):
            username = input("Enter the username of the customer: ")
            if username == "" or username.isspace():
                print("Username cannot be empty")
                username = None
                continue
        if age == None and username != None:
            age = input("Enter the age of the customer: ")
            if age == "" or age.isspace():
                print("Age cannot be empty")
                age = None
                continue
            if not age.isdigit():
                print("Age should be a number")
                age = None
                continue
            age = int(age)
            if age < 18:
                print("Age should be greater than 18")
                age = None
                continue
        if address == None and age != None:
            address = input("Enter the address of the customer: ")
            if address == "" or address.isspace():
                print("Address cannot be empty")
                address = None
                continue
        if phone == None and address != None:
            phone = input("Enter the phone number of the customer: ")
            if len(phone) != 10:
                print("Phone number should be of 10 digits")
                phone = None
                continue
        if phone != None:
            while(True):
                print("CHOOSE A VERIFICATION METHOD")
                print("1. Aadhar Card")
                print("2. PAN Card")
                choose = input("Enter the verification way: ")
                if(choose == '1'):
                    if verification_way == None:
                        verification_way = "Aadhar Card"
                    if verification_number == None:
                        verification_number = input(
                            "Enter the Aadhar Card number: ")
                    if(len(verification_number) != 12):
                        print("Invalid Aadhar Card number")
                        verification_number = None
                        continue
                    else:
                        break
                elif(choose == '2'):
                    if verification_way == None:
                        verification_way = "PAN Card"
                    if verification_number == None:
                        verification_number = input(
                            "Enter the PAN Card number: ")
                    if(len(verification_number) != 10):
                        print("Invalid PAN Card number")
                        verification_number = None
                        continue
                    else:
                        break
                else:
                    print("Invalid choice")
                    continue
            while(True):
                password = input("Enter the password: ")
                if password == "" or password.isspace():
                    print("Invalid password")
                    password = None
                    continue
                elif len(password) > 4 or len(password) < 4:
                    print("Password Should be of 4 numbers")
                    password = None
                    continue
                else:
                    break
        if(name != None and username != None and age != None and address != None and phone != None and verification_way != None and verification_number != None and password != None):
            break
    return account_number, name, username, age, address, phone, verification_way, verification_number, password


def login():
    print("LOGIN")
    username = None
    password = None
    while(True):
        if username == None:
            username = input("Enter the username: ")
        if username == "" or username.isspace():
            print("Username cannot be empty")
            username = None
            continue
        if password == None and username != None:
            password = input("Enter the password: ")
        if password == "" or password == None or password.isspace():
            print("Password cannot be empty")
            password = None
            continue
        if username != None and password != None:
            break
    cursor.execute(
        "SELECT account_number, username, password FROM customer WHERE username = %s AND password = %s", (username, password))

    data = cursor.fetchone()

    if(data != None):
        global myAccount_Number
        myAccount_Number = data[0]
        print("Login Successful")
        return True
    else:
        print("Login Failed")
        return False


def withdraw():
    cursor.execute(
        "SELECT account_number FROM customer WHERE account_number = %s", (myAccount_Number,))
    if(cursor.fetchone() == None):
        print("Account number does not exist")
        return
    amount = int(input("Enter the amount to be withdrawn: "))
    cursor.execute(
        "SELECT balance FROM customer WHERE account_number = %s", (myAccount_Number,))
    usersData = cursor.fetchone()
    if usersData == None:
        print("Account number does not exist")
        return
    if(amount > usersData[0]):
        print("Insufficient balance")
        return
    cursor.execute(
        "UPDATE customer SET balance = balance - %s WHERE account_number = %s", (amount, myAccount_Number))
    cursor.execute(
        "SELECT * FROM customer WHERE account_number = %s", (myAccount_Number,))
    usersData = cursor.fetchone()
    if usersData == None:
        print("Account number does not exist")
        return
    cursor.execute(
        "INSERT INTO transaction_history VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (myAccount_Number, usersData[1], usersData[2], "WITHDRAW {} FROM SELF".format(amount), amount, 0.00, usersData[6], datetime.now()))
    db.commit()
    print("Amount withdrawn successfully\n")
    print("Your current balance is {}".format(usersData[6]))


def deposit():
    cursor.execute(
        "SELECT account_number FROM customer WHERE account_number = %s", (myAccount_Number,))
    if(cursor.fetchone() == None):
        print("Account number does not exist")
        return
    amount = float(input("Enter the amount to be deposited: "))
    cursor.execute(
        "UPDATE customer SET balance = balance + %s WHERE account_number = %s", (amount, myAccount_Number))
    cursor.execute(
        "SELECT * FROM customer WHERE account_number = %s", (myAccount_Number,))
    usersData = cursor.fetchone()
    if usersData == None:
        print("Account number does not exist")
        return
    cursor.execute(
        "INSERT INTO transaction_history VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (myAccount_Number, usersData[1], usersData[2], "DEPOSIT {} TO SELF".format(amount), 0.00, amount, usersData[6], datetime.now()))
    db.commit()
    print("Amount deposited successfully\n")
    print("Your current balance is: {}".format(usersData[6]))
    return


def transfer():
    account_number = input("Enter account number to transfer : ")
    password = int(input("Enter your password: "))

    cursor.execute(
        "SELECT account_number FROM customer WHERE account_number = %s", (myAccount_Number,))

    if(cursor.fetchone() == None):
        print("Account number does not exist")
        exit()

    cursor.execute(
        "SELECT password FROM customer WHERE account_number = %s", (myAccount_Number,))
    paslist = cursor.fetchone()
    if paslist == None:
        print("Account number does not exist")
        exit()
    if(paslist[0] != '{}'.format(password)):
        print("Invalid password")
        exit()

    amount = int(input("Enter the amount to be transferred: "))

    # check weather the amount is greater than the balance

    cursor.execute(
        "SELECT balance FROM customer WHERE account_number = %s", (myAccount_Number,))
    usersData = cursor.fetchone()
    if usersData == None:
        print("Account number does not exist")
        exit()

    if(usersData[0] < amount):
        print("Insufficient balance")
        exit()

    cursor.execute(
        "UPDATE customer SET balance = balance - %s WHERE account_number = %s", (amount, myAccount_Number))

    cursor.execute(
        "UPDATE customer SET balance = balance + %s WHERE account_number = %s", (amount, account_number))

    # update the transaction History

    cursor.execute(
        "SELECT * from customer WHERE account_number = %s", (account_number,))
    receiverList = cursor.fetchone()
    if receiverList == None:
        print("Account number does not exist")
        exit()

    cursor.execute(
        "SELECT * FROM customer WHERE account_number = %s", (myAccount_Number,))
    senderList = cursor.fetchone()
    if senderList == None:
        print("Account number does not exist")
        exit()

    cursor.execute("INSERT INTO transaction_history VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                   (myAccount_Number, senderList[1], senderList[2], "SEND {} TO {}".format(
                       amount, account_number), amount, 0.00, senderList[6], date.today()))

    cursor.execute("INSERT INTO transaction_history VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                   (account_number, receiverList[1], receiverList[2], "RECEIVE {} FROM {}".format(
                       amount, myAccount_Number), 0.00, amount, receiverList[6], date.today()))

    db.commit()
    print("Amount transferred successfully")
    print("Your current balance is {}".format(senderList[6]))


def displayBalance():
    cursor.execute(
        "SELECT account_number FROM customer WHERE account_number = %s", (myAccount_Number,))
    if(cursor.fetchone() == None):
        print("Account number does not exist")
        exit()
    cursor.execute(
        "SELECT account_number, name, balance FROM customer WHERE account_number = %s", (myAccount_Number,))
    usersData = cursor.fetchone()
    if usersData == None:
        print("Account number does not exist")
        exit()
    print("YOUR BALANCE DETAILS")
    print("Name : {} \n Account Number : {} \n Balance: {}\n".format(
        usersData[1], usersData[0], usersData[2]))
    print("\n")


def historyTransaction():
    cursor.execute(
        "SELECT account_number FROM customer WHERE account_number = %s", (myAccount_Number,))
    if(cursor.fetchone() == None):
        print("Account number does not exist")
        return
    cursor.execute(
        "SELECT * FROM transaction_history WHERE account_number = %s", (myAccount_Number,))

    data = cursor.fetchall()

    if data == None or data == []:
        print("\n\nNo transaction history\n\n")
        return

    data.reverse()

    for row in data:
        usersData = row
        print("--------------------------------------------------", end="\n\n")
        print("Account Number: ", usersData[0])
        print("Name: ", usersData[1])
        print("UserName: ", usersData[2])
        print("Transaction: ", usersData[3])
        print("Debit: ", usersData[4])
        print("Credit: ", usersData[5])
        print("New Balance: ", usersData[6])
        print("Date: ", usersData[7], end="\n\n")
        print("--------------------------------------------------")


def applyLoan():
    cursor.execute(
        "SELECT account_number FROM customer WHERE account_number = %s", (myAccount_Number,))
    if(cursor.fetchone() == None):
        print("Account number does not exist")
        return

    cursor.execute(
        "SELECT loan_type FROM loan_details WHERE account_number = %s ", (myAccount_Number,))

    if(cursor.fetchone() != None):
        print("You already have a Loan")
        return

    print("Type of Loan : ")
    print("1. Personal Loan")
    print("2. Education Loan")
    ltc = int(input("Enter your choice: "))

    loan_type = None
    college_name = None
    college_address = None
    graduate_year = None
    final_payment_date = None
    starting_date = None
    remaining_amount = None
    paid_amount = None
    loaned_date = None
    amount_to_pay = None
    loan_amount = None
    repayment_type = None
    if(ltc == 1):
        loan_type = "Personal Loan"

        ld = int(
            input("Enter the duration of loan in months (Minimum = 5 months, Maximum = 68 months ): "))
        if(ld < 5 or ld > 68):
            print("Invalid duration")
            return
        loan_amount = int(input(
            "Enter the amount to be loaned (Minimum: 50,000 and Maximum: ( 20Lakhs or 20,00000 ) : "))
        if loan_amount < 50000:
            print("Minimum loan amount is 50,000")
            return
        elif loan_amount > 2000000:
            print("Maximum loan amount is 20,00000")
            return
        repayment_type = input(
            "Enter the type of repayment (Monthly or Yearly) : ")
        if(repayment_type != "Monthly" and repayment_type != "Yearly"):
            print("Invalid repayment type")
            return
        starting_date = date.today() + timedelta(days=365)
        final_payment_date = starting_date + timedelta(days=(ld*30))
        remaining_amount = loan_amount
        paid_amount = 0
        loaned_date = date.today()
        if(repayment_type == "Monthly"):
            amount_to_pay = (remaining_amount/ld) + \
                ((remaining_amount/ld)*0.08)
        elif(repayment_type == "Yearly"):
            amount_to_pay = (remaining_amount/ld) + ((remaining_amount/ld)*0.1)
    elif(ltc == 2):
        loan_type = "Education Loan"
        # college details
        college_name = input("Enter the name of college: ")
        college_address = input("Enter the full address of college: ")
        gradyear = input("Enter the year of graduation ( YYYY/MM/DD ): ")
        ld = int(input("Enter the duration of loan in years ( Minimum 5 years ): "))
        if(ld < 5):
            print("Minimum duration of loan is 5 years")
            return
        loaned_date = date.today()
        format = "%Y/%m/%d"
        x = datetime.strptime(gradyear, format)
        graduate_year = x.date()
        tempgradyear = gradyear.split("/")
        starting_date = loaned_date + timedelta(days=(int(tempgradyear[0])-loaned_date.year)*365) + timedelta(
            days=(int(tempgradyear[0])-loaned_date.month)*30*5)
        final_payment_date = loaned_date + \
            timedelta(days=ld*365) + timedelta(days=5*30)
        loan_amount = float(input("Enter the amount to be loaned: "))
        remaining_amount = loan_amount
        paid_amount = 0
        loaned_date = date.today()
        repayment_type = input(
            "Enter the type of repayment ( Monthly, Yearly ): ")
        if(repayment_type == "Monthly"):
            amount_to_pay = (remaining_amount/ld) + \
                ((remaining_amount/ld)*0.075)
        elif(repayment_type == "Yearly"):
            amount_to_pay = (remaining_amount/ld) + \
                ((remaining_amount/ld)*0.09)
    else:
        print("Invalid choice")
        return
    cursor.execute("INSERT INTO loan_details values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (myAccount_Number, loan_type, loan_amount, remaining_amount, paid_amount, amount_to_pay, loaned_date, starting_date, repayment_type,  final_payment_date, college_name, college_address, graduate_year))

    # update the balance
    cursor.execute(
        "SELECT balance, name, username FROM customer WHERE account_number = %s", (myAccount_Number,))

    data = cursor.fetchone()
    if data == None:
        print("Account number does not exist")
        return
    balance = data[0]
    name = data[1]
    username = data[2]

    balance = balance + loan_amount

    cursor.execute("UPDATE customer SET balance = %s WHERE account_number = %s",
                   (balance, myAccount_Number))

    # Update the transaction history
    cursor.execute("INSERT INTO transaction_history values (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (myAccount_Number, name, username, "Loan", 0, loan_amount, balance, date.today()))

    db.commit()
    print("Loan Applied Successfully")


def checkLoanStatus():
    cursor.execute(
        "SELECT account_number FROM customer WHERE account_number = %s", (myAccount_Number,))
    if(cursor.fetchone() == None):
        print("Account number does not exist")
        return
    cursor.execute(
        "SELECT * FROM loan_details WHERE account_number = %s", (myAccount_Number,))
    data = cursor.fetchall()
    if data == None:
        print("You don't have any loan")
        return
    if(len(data) == 0):
        print("No loans applied")
        return
    for row in data:
        usersData = row
        print("--------------------------------------------------", end="\n\n")
        print("Account Number: ", usersData[0])
        print("Loan Type: ", usersData[1])
        print("Loan Amount: ", usersData[2])
        print("Remaining Amount: ", usersData[3])
        print("Paid Amount: ", usersData[4])
        print("Amount to Pay: ", usersData[5])
        print("Loaned Date: ", usersData[6])
        print("Next Premium Date: ", usersData[7])
        print("Repayment Type: ", usersData[8])
        print("Final Payment Date: ", usersData[9])
        if usersData[1] == "Education Loan":
            print("College Name: ", usersData[10])
            print("College Address: ", usersData[11])
            print("Graduation Year: ", usersData[12])
        print(end="\n\n")
        print("-------------------------------------------------- \n\n")


def payLoan():
    loan_type = None
    next_premium_date = None
    cursor.execute(
        "SELECT account_number FROM customer WHERE account_number = %s", (myAccount_Number,))
    if(cursor.fetchone() == None):
        print("Account number does not exist")
        return
    print("Which loan do you want to pay?")
    print("1. Personal Loan")
    print("2. Education Loan")
    ltc = int(input("Enter your choice: "))
    if(ltc == 1):
        loan_type = "Personal Loan"
    elif ltc == 2:
        loan_type = "Education Loan"
    else:
        print("Invalid choice")
        return
    cursor.execute(
        "SELECT * FROM loan_details WHERE account_number = %s AND loan_type = %s", (myAccount_Number, loan_type))
    loanData = cursor.fetchone()
    if loanData == None:
        print("No {} applied".format(loan_type))
        return
    DATA = []
    DATA = list(loanData)

    today_date = date.today()

    if DATA[7] == None:
        print("You have already paid the loan")
        return

    if(DATA[8] == "Monthly"):
        if(DATA[7] > today_date):
            print(
                "You can't pay now, Next Monthly Premium Date is {}".format(DATA[7]))
            return
        if DATA[7] < today_date:
            # add interest to the remaining amount
            DATA[5] = DATA[5] + (DATA[5]*0.075)
            print(
                "You are paying the loan after the due date so you have to pay extra interest")
            print("Amount to pay: ", DATA[5])

        next_premium_date = DATA[7] + timedelta(days=30)

    elif(DATA[8] == "Yearly"):
        if(DATA[7] > today_date):
            print(
                "You can't pay now, Next Yearly Premium Date is {}".format(DATA[7]))
            return
        if DATA[7] < today_date:
            # add interest to the remaining amount
            DATA[5] = DATA[5] + (DATA[5]*0.09)
            print(
                "You are paying the loan after the due date so you have to pay extra interest")
            print("Amount to pay: ", DATA[5])
        next_premium_date = DATA[7] + timedelta(days=365)

    if(DATA[3] <= 0):
        print("Loan is already paid")
        return

    print("--------------------------------------------------", end="\n\n")
    print("Account Number: ", DATA[0])
    print("Loan Type: ", DATA[1])
    print("Loan Amount: ", DATA[2])
    print("Remaining Amount: ", DATA[3])
    print("Paid Amount: ", DATA[4])
    print("Amount to Pay: ", DATA[5])
    print("Loaned Date: ", DATA[6])
    print("Next Premium Date: ", DATA[7])
    print("Repayment Type: ", DATA[8])
    print("Final Payment Date: ", DATA[9])
    if DATA[1] == "Education Loan":
        print("College Name: ", DATA[10])
        print("College Address: ", DATA[11])
        print("Graduation Year: ", DATA[12])
    print(end="\n\n")
    print("-------------------------------------------------- \n\n")

    amount_to_pay = DATA[5]
    str = "Do You Want To Pay {} (y/n) ".format(amount_to_pay)
    choice = input(str)
    if(choice == 'y' or choice == 'Y'):
        remaining_amount = DATA[3]-amount_to_pay
        if remaining_amount < 0:
            remaining_amount = 0
            amount_to_pay = 0
            next_premium_date = None
        paid_amount = DATA[4]+amount_to_pay
        cursor.execute("UPDATE loan_details SET premium_date = %s, amount_to_pay = %s, remaining_amount = %s, paid_amount = %s WHERE account_number = %s AND loan_type = %s",
                       (next_premium_date, amount_to_pay, remaining_amount, paid_amount, myAccount_Number, loan_type))

        # update the balance
        cursor.execute(
            "SELECT balance, name, username FROM customer WHERE account_number = %s", (myAccount_Number,))

        data = cursor.fetchone()
        if data == None:
            print("Something went wrong try again")
            return
        balance = data[0]
        name = data[1]
        username = data[2]
        balance = balance - amount_to_pay
        cursor.execute("INSERT INTO transaction_history values (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (myAccount_Number, name, username, "Loan Payment", DATA[5], 0, balance, date.today()))

        db.commit()
        print("Loan Paid Successfully")
    else:
        print("Loan Payment Cancelled")


def loan():
    while(True):
        print("1. Apply for loan")
        print("2. Check loan status")
        print("3. Pay loan")
        print("4. Back")
        choice = int(input("Enter your choice: "))
        if(choice == 1):
            applyLoan()
        elif(choice == 2):
            checkLoanStatus()
        elif(choice == 3):
            payLoan()
        elif(choice == 4):
            break
        else:
            print("Invalid choice")
    return


def loginOption(choose):
    if(choose == '1'):
        withdraw()
    elif(choose == '2'):
        deposit()
    elif(choose == '3'):
        transfer()
    elif(choose == '4'):
        displayBalance()
    elif(choose == '5'):
        historyTransaction()
    elif(choose == '6'):
        loan()


# # get details from
while(True):
    print("WELCOME")
    print("1. Create a new account")
    print("2. Login")
    print("3. Exit")
    choose = input("Enter your choice: ")
    # choose = '4'

    if(choose == '1'):
        account_number, name, username, age, address, phone, verification_way, verification_number, password = get_details()
        cursor.execute("INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (account_number, name, username, age, address, phone, 0, verification_way, verification_number, password))
        db.commit()
        print("Account created successfully")
        # Print all the data of the registered User
        cursor.execute(
            "SELECT * FROM customer WHERE account_number = %s", (account_number,))
        usersData = cursor.fetchone()
        if usersData == None:
            print("Some Error Occured")
            continue
        print(usersData)
        print("\nYour Details are: \n")
        print("Account Number: ", usersData[0])
        print("Name: ", usersData[1])
        print("UserName: ", usersData[2])
        print("Age: ", usersData[3])
        print("Address: ", usersData[4])
        print("Phone Number: ", usersData[5])
        print("Balance: ", usersData[6])
        print("Verification Number: ", usersData[8])
        print("Login to your account to continue")
    elif(choose == '2'):
        if login():
            while(True):
                print("1. Withdraw Money")
                print("2. Deposit Money")
                print("3. Transfer Money")
                print("4. Display Balance")
                print("5. History of transactions")
                print("6. Loans")
                print("7. Back")
                choose = input("Enter your choice: ")
                if(choose == '7'):
                    myAccount_Number = None
                    break
                elif choose > '7' or choose < '1' or type(choose) != str:
                    print("Invalid choice\n")
                else:
                    loginOption(choose)
    elif choose == '3':
        print("Thank you for using our services")
        exit()
    else:
        print("Invalid choice")
        choice = input("Do you want to continue? (y/n): ")
        if(choice == 'n'):
            print("Thank you for using our services")
            exit()
