import random
import time

import csv

import json
from datetime import datetime

from getpass import getpass

import hashlib

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

 

def verify_password(password, stored_password):
    return hash_password(password) == stored_password

FILE_NAME = "data/customers.json"
#============================
#admin login confirmation
#=============================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("admin123")


print("==============================================")
print(" SMART BANKING MANAGEMENT SYSTEM ")
print("==============================================")

def load_admin_logs():

    try:

        with open(
            "data/admin_logs.json",
            "r"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        return []

    except json.JSONDecodeError:

        return []


def view_admin_logs():

    logs = load_admin_logs()

    print("\n========================================")
    print("           ADMIN AUDIT LOG")
    print("========================================")

    if not logs:

        print("\nNo admin activity recorded.")

        input(
            "\nPress Enter to return..."
        )

        return

    for index, log in enumerate(
        logs,
        start=1
    ):

        print(
            "\n----------------------------------------"
        )

        print(
            "Log Number  :",
            index
        )

        print(
            "Date & Time :",
            log.get(
                "date",
                "Not available"
            )
        )

        print(
            "Action      :",
            log.get(
                "action",
                "Not available"
            )
        )

        print(
            "Account No  :",
            log.get(
                "account_no",
                "Not available"
            )
        )

        print(
            "Details     :",
            log.get(
                "details",
                "Not available"
            )
        )

    print(
        "\n========================================"
    )

    input(
        "\nPress Enter to return..."
    )


def backup_data():

    import shutil
    import os

    backup_folder = "backup"

    if not os.path.exists(
        backup_folder
    ):

        os.makedirs(
            backup_folder
        )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    # Customers backup

    if os.path.exists(
        "customers.json"
    ):

        shutil.copy(
            "customers.json",
            f"{backup_folder}/customers_{timestamp}.json"
        )

    # Admin logs backup

    if os.path.exists(
        "admin_logs.json"
    ):

        shutil.copy(
            "admin_logs.json",
            f"{backup_folder}/admin_logs_{timestamp}.json"
        )

    print(
        "\nBackup created successfully."
    )


def system_health_check():

    print("\n========================================")
    print("         SYSTEM HEALTH CHECK")
    print("========================================")

    # Customers JSON

    try:

        test_customers = load_customers()

        print(
            "\nCustomers Data : OK"
        )

        print(
            "Customer Count :",
            len(test_customers)
        )

    except Exception as e:

        print(
            "\nCustomers Data : ERROR"
        )

        print(
            "Error:",
            e
        )

    # Admin logs

    try:

        logs = load_admin_logs()

        print(
            "\nAdmin Logs     : OK"
        )

        print(
            "Log Count      :",
            len(logs)
        )

    except Exception as e:

        print(
            "\nAdmin Logs     : ERROR"
        )

        print(
            "Error:",
            e
        )

    print(
        "\n========================================"
    )

    input(
        "\nPress Enter to return..."
    )



#=========================
#LOAD CUSTOMERS FROM FILE
#=========================
    
def load_customers():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []
 

#=========================
#SAVE CUSTOMERS 
#=============
def save_customers():
    with open(FILE_NAME,'w') as file:
        json.dump(customers, file,indent=4)

customers = load_customers()

#=========================
#GENERATE ACCOUNT NUMBER
#=========================
def generate_account_number():
    if len(customers)==0:
        return 100001
    return customers[-1]["account_no"] + 1

#===================================
#update_existng_customers
#===================================
def update_existing_accounts():

    changed = False

    for customer in customers:

        if "status" not in customer:

            customer["status"] = "Active"

            changed = True

    if changed:

        save_customers()

        print("Existing accounts updated successfully.")

    else:

        print("All accounts already have a status.")

customers = load_customers()

update_existing_accounts()




#=========================
#REGISTER
#=========================
import re
from datetime import datetime


def register():

    print("\n========================================")
    print("          CUSTOMER REGISTRATION")
    print("========================================")

    # ========================================
    # NAME VALIDATION
    # ========================================

    while True:

        name = input(
            "Enter your name: "
        ).strip()

        if name == "":

            print("\nName cannot be empty.")

        elif not name.replace(" ", "").isalpha():

            print(
                "\nName should contain only letters."
            )

        else:

            break

    # ========================================
    # PASSWORD VALIDATION
    # ========================================

    while True:

        password = input(
            "Enter your password: "
        )

        if len(password) < 4:

            print(
                "\nPassword must contain at least 4 characters."
            )

        else:

            break

    # ========================================
    # MOBILE NUMBER
    # ========================================

    while True:

        mobile = input(
            "Enter Mobile Number: "
        ).strip()

        # Exactly 10 digits
        if not mobile.isdigit():

            print(
                "\nMobile number must contain only digits."
            )
            continue

        if len(mobile) != 10:

            print(
                "\nMobile number must contain exactly 10 digits."
            )
            continue

        # Cannot start with 0
        if mobile[0] == "0":

            print(
                "\nMobile number cannot start with 0."
            )
            continue

        # Indian mobile numbers normally start 6-9
        if mobile[0] not in "6789":

            print(
                "\nInvalid mobile number."
            )
            print(
                "Mobile number must start with 6, 7, 8 or 9."
            )
            continue

        # Duplicate mobile check
        mobile_exists = False

        for customer in customers:

            if customer.get("mobile") == mobile:

                mobile_exists = True
                break

        if mobile_exists:

            print(
                "\nThis mobile number is already registered."
            )
            continue

        break

    # ========================================
    # MOBILE VERIFICATION
    # ========================================
    #
    # For the current JSON version we mark it
    # as verified after successful validation.
    #
    # Real SMS OTP can be added later.
    # ========================================
    # ========================================
    # MOBILE VERIFICATION
    # ========================================

    customer_for_verification = {
        "mobile": mobile,
        "mobile_verified": False
    }

    print("\n========================================")
    print("       MOBILE VERIFICATION")
    print("========================================")

    print(
        "An OTP will be generated for your mobile number."
    )

    mobile_verified = verify_mobile_otp(
        customer_for_verification
    )

    if not mobile_verified:

        print("\n========================================")
        print("       REGISTRATION CANCELLED")
        print("========================================")

        print(
            "Mobile number verification failed."
        )

        print(
            "Customer registration cannot continue."
        )

        print("========================================")

        return

    # ========================================
    # EMAIL TYPE
    # ========================================

    while True:

        print("\nSelect Email Type:")

        print("1. Personal")
        print("2. Company")

        email_type_choice = input(
            "Enter your choice (1-2): "
        ).strip()

        if email_type_choice == "1":

            email_type = "Personal"
            break

        elif email_type_choice == "2":

            email_type = "Company"
            break

        else:

            print(
                "\nInvalid choice. Please select 1 or 2."
            )

    # ========================================
    # EMAIL VALIDATION
    # ========================================

    while True:

        email = input(
            "Enter Email: "
        ).strip().lower()

        # Basic email structure
        email_pattern = (
            r"^[a-zA-Z0-9._%+-]+@"
            r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )

        if not re.match(
            email_pattern,
            email
        ):

            print(
                "\nInvalid email format."
            )
            continue

        # Personal email must be Gmail
        if email_type == "Personal":

            if not email.endswith("@gmail.com"):

                print(
                    "\nPersonal email must end with @gmail.com."
                )

                continue

        # Company email
        elif email_type == "Company":

            if email.endswith("@gmail.com"):

                print(
                    "\nFor a company account, "
                    "please use the company email domain."
                )

                continue

        # Duplicate email check
        email_exists = False

        for customer in customers:

            existing_email = customer.get(
                "email",
                ""
            ).lower()

            if existing_email == email:

                email_exists = True
                break

        if email_exists:

            print(
                "\nThis email is already registered."
            )

            continue

        break

    # ========================================
    # AADHAAR VALIDATION
    # ========================================

    while True:

        aadhaar = input(
            "Enter 12-digit Aadhaar Number: "
        ).strip()

        # Remove spaces if user enters them
        aadhaar = aadhaar.replace(
            " ",
            ""
        )

        if not aadhaar.isdigit():

            print(
                "\nAadhaar must contain only numbers."
            )

            continue

        if len(aadhaar) != 12:

            print(
                "\nAadhaar must contain exactly 12 digits."
            )

            continue

        break

    # ========================================
    # MASK AADHAAR
    # ========================================

    masked_aadhaar = (
        "XXXX-XXXX-" +
        aadhaar[-4:]
    )

    # ========================================
    # INITIAL DEPOSIT
    # ========================================

    while True:

        try:

            balance = float(
                input(
                    "Enter Initial Deposit: ₹"
                )
            )

            if balance <= 0:

                print(
                    "\nInitial deposit must be greater than zero."
                )

            else:

                break

        except ValueError:

            print(
                "\nInvalid input! "
                "Please enter a valid amount."
            )

    # ========================================
    # GENERATE ACCOUNT NUMBER
    # ========================================

    account_no = generate_account_number()

    # ========================================
    # CREATE CUSTOMER
    # ========================================

    customer = {

        "account_no": account_no,

        "name": name,

        "password": hash_password(password),

        "mobile": mobile,

        "mobile_verified": mobile_verified,

        "email": email,

        "email_type": email_type,

        "aadhaar": masked_aadhaar,

        "balance": balance,

        "status": "Active",

        "transactions": []
    }

    # ========================================
    # INITIAL TRANSACTION ID
    # ========================================

    transaction_id = (
        "TXN-" +
        datetime.now().strftime("%Y%m%d") +
        "-" +
        str(len(customers) + 1).zfill(4)
    )

    # ========================================
    # INITIAL DEPOSIT TRANSACTION
    # ========================================

    transaction = {

        "transaction_id": transaction_id,

        "type": "Initial Deposit",

        "amount": balance,

        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    customer["transactions"].append(
        transaction
    )

    # ========================================
    # ADD CUSTOMER
    # ========================================

    customers.append(
        customer
    )

    # ========================================
    # SAVE DATA
    # ========================================

    save_customers()

    # ========================================
    # REGISTRATION SUCCESS
    # ========================================

    print("\n========================================")
    print("      REGISTRATION SUCCESSFUL")
    print("========================================")

    print(
        "Account Number  :",
        account_no
    )

    print(
        "Customer Name   :",
        name
    )

    print(
        "Mobile Number   :",
        mobile
    )

    print(
        "Mobile Verified :",
        "YES" if mobile_verified else "NO"
    )

    print(
        "Email           :",
        email
    )

    print(
        "Email Type      :",
        email_type
    )

    print(
        "Aadhaar         :",
        masked_aadhaar
    )

    print(
        "Initial Deposit : ₹",
        format(
            balance,
            ".2f"
        )
    )

    print(
        "Account Status   :",
        "Active"
    )

    print("========================================")

    print(
        "You can now login using your account number."
    )

    print("========================================")

#=========================
#forgot password
#=========================
def forgot_password():

    import random
    import time
    import threading

    print("\n========================================")
    print("            FORGOT PASSWORD")
    print("========================================")

    # ========================================
    # ACCOUNT NUMBER
    # ========================================

    try:

        account_no = int(
            input("Enter Account Number: ")
        )

    except ValueError:

        print("\nAccount Number must be a number.")
        return

    # ========================================
    # FIND CUSTOMER
    # ========================================

    found_customer = None

    for customer in customers:

        if customer.get("account_no") == account_no:

            found_customer = customer
            break

    if found_customer is None:

        print("\nAccount not found.")
        return

    # ========================================
    # ACCOUNT STATUS
    # ========================================

    account_status = found_customer.get(
        "status",
        "Active"
    )

    if account_status == "Closed":

        print("\nThis account is closed.")
        return

    if account_status == "Inactive":

        print("\nThis account is inactive.")
        return

    # ========================================
    # MOBILE CHECK
    # ========================================

    mobile = found_customer.get(
        "mobile",
        ""
    )

    if not mobile:

        print("\nNo mobile number registered.")

        print(
            "Please add your mobile number "
            "from Customer Profile."
        )

        return

    # ========================================
    # MOBILE VERIFICATION
    # ========================================

    if not found_customer.get(
        "mobile_verified",
        False
    ):

        print(
            "\nYour mobile number is not verified."
        )

        print(
            "Please verify your mobile number "
            "from Customer Profile."
        )

        return

    # ========================================
    # MASK MOBILE
    # ========================================

    masked_mobile = (
        "XXXXXX" + mobile[-4:]
    )

    print(
        "\nOTP will be sent to:",
        masked_mobile
    )

    # ========================================
    # GENERATE OTP
    # ========================================

    otp = random.randint(
        100000,
        999999
    )

    # OTP valid for 2 minutes
    otp_expiry = 120

    # Maximum attempts
    max_attempts = 3

    print("\n[TEST MODE]")
    print("OTP:", otp)

    print(
        "\nOTP is valid for 2 minutes."
    )

    # ========================================
    # FUNCTION FOR INPUT WITH TIMEOUT
    # ========================================

    def get_input_with_timeout(
        prompt,
        timeout
    ):

        result = []

        def take_input():

            value = input(prompt)

            result.append(value)

        input_thread = threading.Thread(
            target=take_input
        )

        input_thread.daemon = True

        input_thread.start()

        input_thread.join(timeout)

        if input_thread.is_alive():

            return None

        return result[0]

    # ========================================
    # OTP VERIFICATION
    # ========================================

    otp_verified = False

    for attempt in range(
        1,
        max_attempts + 1
    ):

        entered_otp = get_input_with_timeout(
            "\nEnter OTP: ",
            otp_expiry
        )

        # ====================================
        # OTP EXPIRED
        # ====================================

        if entered_otp is None:

            print(
                "\n========================================"
            )

            print(
                "             OTP EXPIRED"
            )

            print(
                "========================================"
            )

            print(
                "The OTP was valid for only 2 minutes."
            )

            print(
                "Please try Forgot Password again."
            )

            print(
                "========================================"
            )

            return

        entered_otp = entered_otp.strip()

        # ====================================
        # CHECK OTP
        # ====================================

        if entered_otp == str(otp):

            otp_verified = True

            print(
                "\nOTP verified successfully."
            )

            break

        # ====================================
        # WRONG OTP
        # ====================================

        remaining_attempts = (
            max_attempts - attempt
        )

        if remaining_attempts > 0:

            print(
                "\nIncorrect OTP."
            )

            print(
                "Attempts remaining:",
                remaining_attempts
            )

        else:

            print(
                "\n========================================"
            )

            print(
                "       OTP VERIFICATION FAILED"
            )

            print(
                "========================================"
            )

            print(
                "Maximum OTP attempts exceeded."
            )

            print(
                "Please try Forgot Password again."
            )

            print(
                "========================================"
            )

            return

    # ========================================
    # OTP CHECK
    # ========================================

    if not otp_verified:

        return

    # ========================================
    # NEW PASSWORD
    # ========================================

    new_password = getpass(
        "\nEnter New Password: "
    )

    if len(new_password) < 4:

        print(
            "\nPassword must contain at least 4 characters."
        )

        return

    # ========================================
    # CHECK SAME PASSWORD
    # ========================================

    current_password_hash = found_customer.get(
        "password",
        ""
    )

    new_password_hash = hash_password(
        new_password
    )

    if new_password_hash == current_password_hash:

        print(
            "\n========================================"
        )

        print(
            "          SAME PASSWORD"
        )

        print(
            "========================================"
        )

        print(
            "New password cannot be the same "
            "as your current password."
        )

        print(
            "Please choose a different password."
        )

        print(
            "========================================"
        )

        return

    # ========================================
    # CONFIRM PASSWORD
    # ========================================

    confirm_password = getpass(
        "Confirm New Password: "
    )

    if new_password != confirm_password:

        print(
            "\nPasswords do not match."
        )

        return

    # ========================================
    # SAVE PASSWORD
    # ========================================

    found_customer["password"] = (
        new_password_hash
    )

    save_customers()

    # ========================================
    # SUCCESS
    # ========================================

    print(
        "\n========================================"
    )

    print(
        "       PASSWORD RESET SUCCESSFUL"
    )

    print(
        "========================================"
    )

    print(
        "Your password has been changed successfully."
    )

    print(
        "You can now login using your new password."
    )

    print(
        "========================================"
    )
#=========================
#login
#=========================
def login():

    global customers

    customers = load_customers()

    while True:

        print("\n========================================")
        print("          CUSTOMER LOGIN")
        print("========================================")

        print("1. Login")
        print("2. Forgot Password")
        print("3. Back")

        choice = input(
            "\nEnter your choice (1-3): "
        ).strip()

        # ========================================
        # LOGIN
        # ========================================

        if choice == "1":

            print("\n------Customer Login-----")
            print()

            # ------------------------------------
            # ACCOUNT NUMBER
            # ------------------------------------

            try:

                account_no = int(
                    input("Enter Account Number: ")
                )

            except ValueError:

                print(
                    "\nAccount Number must be a number."
                )

                continue

            # ------------------------------------
            # PASSWORD
            # ------------------------------------

            password = getpass(
                "Enter Password: "
            )

            # ------------------------------------
            # FIND CUSTOMER
            # ------------------------------------

            found_customer = None

            for customer in customers:

                if customer.get(
                    "account_no"
                ) == account_no:

                    found_customer = customer
                    break

            # ------------------------------------
            # ACCOUNT NOT FOUND
            # ------------------------------------

            if found_customer is None:

                print(
                    "\nInvalid Account Number."
                )

                continue

            # ====================================
            # PASSWORD VERIFICATION
            # ====================================

            stored_password = found_customer.get(
                "password",
                ""
            )

            # ------------------------------------
            # HASHED PASSWORD
            # ------------------------------------

            if len(stored_password) == 64:

                entered_password_hash = hash_password(
                    password
                )
                 

                if (
                    entered_password_hash
                    != stored_password
                ):

                    print(
                        "\nIncorrect Password."
                    )

                    continue
                print("\n  PASSWORD VERIFIED SUCCESSFULLY ")

            # ------------------------------------
            # OLD PLAIN-TEXT PASSWORD
            # ------------------------------------

            else:

                if stored_password != password:

                    print(
                        "\nIncorrect Password."
                    )

                    continue

                # Convert old password to hash

                found_customer["password"] = (
                    hash_password(password)
                )

                save_customers()

                print(
                    "\nYour password has been securely updated."
                )

            # ====================================
            # ACCOUNT STATUS
            # ====================================

            account_status = found_customer.get(
                "status",
                "Active"
            )

            print(
                "\nAccount Status:",
                account_status
            )

            # ====================================
            # INACTIVE ACCOUNT
            # ====================================

            if account_status == "Inactive":

                print(
                    "\n========================================"
                )

                print(
                    "             LOGIN BLOCKED"
                )

                print(
                    "========================================"
                )

                print(
                    "Your account status is:",
                    account_status
                )

                print(
                    "Please contact the bank administrator."
                )

                print(
                    "========================================"
                )

                continue

            # ====================================
            # CLOSED ACCOUNT
            # ====================================

            if account_status == "Closed":

                print(
                    "\n========================================"
                )

                print(
                    "          ACCOUNT CLOSED"
                )

                print(
                    "========================================"
                )

                print(
                    "This account has been permanently closed."
                )

                print(
                    "Please contact the bank administrator."
                )

                print(
                    "========================================"
                )

                continue

            # ====================================
            # SUCCESSFUL LOGIN
            # ====================================

            print(
                "\n========================================"
            )

            print(
                "          LOGIN SUCCESSFUL"
            )

            print(
                "========================================"
            )

            print(
                "Welcome,",
                found_customer.get("name")
            )

            print(
                "========================================"
            )

            # ------------------------------------
            # CUSTOMER DASHBOARD
            # ------------------------------------

            customer_dashboard(
                found_customer
            )

            # Return after logout

            return

        # ========================================
        # FORGOT PASSWORD
        # ========================================

        elif choice == "2":

            forgot_password()

        # ========================================
        # BACK
        # ========================================

        elif choice == "3":

            print(
                "\nReturning to main menu."
            )

            return

        # ========================================
        # INVALID CHOICE
        # ========================================

        else:

            print(
                "\nInvalid Choice."
                " Please enter 1, 2 or 3."
            )
#-----------------------------------
#generate transaction ids
#----------------------------------
def generate_transaction_id():

    today = datetime.now().strftime("%Y%m%d")

    transaction_number = 1

    for customer in customers:

        transactions = customer.get(
            "transactions",
            []
        )

        for transaction in transactions:

            transaction_id = transaction.get(
                "transaction_id",
                ""
            )

            # Only check today's transaction IDs
            if transaction_id.startswith(
                f"TXN-{today}-"
            ):

                try:

                    number = int(
                        transaction_id.split("-")[-1]
                    )

                    if number >= transaction_number:

                        transaction_number = (
                            number + 1
                        )

                except ValueError:

                    continue

    return (
        f"TXN-{today}-{transaction_number:04d}"
    )


# add notification
def add_notification(customer, message):

    if "notifications" not in customer:

        customer["notifications"] = []

    notification = {

        "message": message,

        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "read": False
    }

    customer["notifications"].append(
        notification
    )

    save_customers()

#view notification
def view_notifications(customer):

    print("\n========================================")
    print("          NOTIFICATIONS")
    print("========================================")

    notifications = customer.get(
        "notifications",
        []
    )

    if not notifications:

        print("\nNo notifications.")

        input(
            "\nPress Enter to return..."
        )

        return

    unread_count = 0

    for notification in notifications:

        if not notification.get(
            "read",
            False
        ):

            unread_count += 1

    print(
        "\nUnread Notifications:",
        unread_count
    )

    for index, notification in enumerate(
        notifications,
        start=1
    ):

        status = "UNREAD"

        if notification.get(
            "read",
            False
        ):

            status = "READ"

        print(
            "\n----------------------------------------"
        )

        print(
            "Notification:",
            index
        )

        print(
            "Message     :",
            notification.get(
                "message",
                "Not available"
            )
        )

        print(
            "Date & Time :",
            notification.get(
                "date",
                "Not available"
            )
        )

        print(
            "Status      :",
            status
        )

    # Mark all as read
    for notification in notifications:

        notification["read"] = True

    save_customers()

    print(
        "\nAll notifications marked as read."
    )

    print("========================================")

    input(
        "\nPress Enter to return..."
    )


#=========================
#Deposit money
#=========================
def deposit_money(customer):
    if not check_account_active(customer):
        return

    print("\n------Deposit Money------")

    try:
        amount = float(
            input("Enter Deposit Amount: ₹")
        )

        if amount <= 0:
            print("Deposit amount must be greater than zero.")
            return

        customer["balance"] += amount

        transaction = {
            "transaction_id": generate_transaction_id(),
            "type"         : "Deposit",
            "amount"       : amount,
            "date"         : datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        customer["transactions"].append(transaction)

        save_customers()

        print("\nDeposit Successful!")
        print(
            "Deposited Amount: ₹",
            format(amount, ".2f")
        )
        print(
            "New Balance: ₹",
            format(customer["balance"], ".2f")
        )

        # Transaction Receipt
        print("\n========================================")
        print("          TRANSACTION RECEIPT")
        print("========================================")

        print(
            "Customer        :",
            customer.get("name")
        )

        print(
            "Account Number  :",
            customer.get("account_no")
        )

        print("Transaction     : Deposit")

        print(
            "Amount          : ₹",
            format(amount, ".2f")
        )

        print(
            "New Balance     : ₹",
            format(customer.get("balance", 0), ".2f")
        )

        print(
            "Date & Time     :",
            transaction["date"]
        )

        print("Status          : SUCCESS")

        print("========================================")

    except ValueError:

        print(
            "Invalid input! Please enter a valid "
            "number for the deposit amount."
        )
#=========================
#Withdraw Money
#=========================
def withdraw_money(customer):
    if not check_account_active(customer):
        return

    print("\n------Withdraw Money------")
    print()

    try:
        amount = float(
            input("Enter Withdrawal Amount: ₹")
        )

        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
            return

        if amount > customer["balance"]:
            print("Insufficient Balance.")
            return

        # Withdraw amount
        customer["balance"] -= amount

        # Create transaction
        transaction_id = generate_transaction_id()
        transaction = {
            "transaction_id":transaction_id,
            "type": "Withdrawal",
            "amount": amount,
            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        customer["transactions"].append(transaction)

        # Save data
        save_customers()

        print("\nWithdrawal Successful!")
        print(
            "Withdrawn Amount: ₹",
            format(amount, ".2f")
        )
        print(
            "Remaining Balance: ₹",
            format(customer["balance"], ".2f")
        )

        # Withdrawal Receipt
        print("\n========================================")
        print("       WITHDRAWAL TRANSACTION RECEIPT")
        print("========================================")

        print("Customer         :",customer.get("name"))

        print("Account Number   :",customer.get("account_no"))

        print("Transaction      : Withdrawal")

        print("Amount           : ₹",format(amount, ".2f"))

        print("Remaining Balance: ₹",
            format(
                customer.get("balance", 0),
                ".2f"
            )
        )

        print("Date & Time      :",
            transaction["date"]
        )
        print("Status           : SUCCESS")

        print("========================================")

    except ValueError:

        print(
            "Invalid input! Please enter a valid "
            "number for the withdrawal amount."
        )
#=========================
#Transaction History
#=========================
def transaction_history(customer):

    print("\n========================================")
    print("          TRANSACTION HISTORY")
    print("========================================")

    transactions = customer.get("transactions", [])

    if not isinstance(transactions, list):
        print("\nTransaction data is invalid.")
        print("========================================")
        return

    if len(transactions) == 0:
        print("\nNo transactions found.")
        print("========================================")
        return

    for index, transaction in enumerate(transactions, start=1):

        if not isinstance(transaction, dict):
            continue

        transaction_id = transaction.get(
            "transaction_id",
            "Old Transaction"
        )

        transaction_type = transaction.get(
            "type",
            "Unknown"
        )

        amount = transaction.get(
            "amount",
            0
        )

        date = transaction.get(
            "date",
            "Date not available"
        )

        print("\nTransaction", index)
        print("----------------------------------------")

        print("Transaction ID :", transaction_id)
        print("Type           :", transaction_type)

        try:
            print(
                "Amount         : ₹",
                format(float(amount), ".2f")
            )
        except (ValueError, TypeError):
            print("Amount         :", amount)

        print("Date & Time    :", date)
        print("Status         : SUCCESS")

    print("\n========================================")
            
#=========================
#Transfer Money 
#=========================
def transfer_money(customer):

    # Check sender status
    if not check_account_active(customer):
        return

    print("\n----- Transfer Money -----")

    # ========================================
    # GET RECEIVER ACCOUNT NUMBER
    # ========================================

    try:

        receiver_account = int(
            input("Enter Receiver Account Number: ")
        )

    except ValueError:

        print("Account Number must be a number.")
        return

    # ========================================
    # FIND RECEIVER
    # ========================================

    receiver = None

    for account in customers:

        if account.get("account_no") == receiver_account:

            receiver = account
            break

    # Receiver does not exist
    if receiver is None:

        print("Receiver account not found.")
        return

    # ========================================
    # CHECK RECEIVER ACCOUNT STATUS
    # ========================================

    receiver_status = receiver.get(
        "status",
        "Active"
    )

    if receiver_status != "Active":

        print("\n========================================")
        print("          TRANSFER BLOCKED")
        print("========================================")

        if receiver_status == "Inactive":

            print(
                "Receiver account is currently inactive."
            )

        elif receiver_status == "Closed":

            print(
                "Receiver account has been closed."
            )

        else:

            print(
                "Receiver account cannot receive money."
            )

        print("========================================")

        return

    # ========================================
    # CANNOT TRANSFER TO YOURSELF
    # ========================================

    if receiver["account_no"] == customer["account_no"]:

        print(
            "You cannot transfer money to your own account."
        )

        return

    # ========================================
    # GET TRANSFER AMOUNT
    # ========================================

    try:

        amount = float(
            input("Enter Transfer Amount: ₹")
        )

    except ValueError:

        print(
            "Please enter a valid amount."
        )

        return

    # ========================================
    # AMOUNT VALIDATION
    # ========================================

    if amount <= 0:

        print(
            "Transfer amount must be greater than zero."
        )

        return

    # ========================================
    # CHECK BALANCE
    # ========================================

    if amount > customer.get("balance", 0):

        print(
            "Insufficient Balance."
        )

        return

    # ========================================
    # CREATE TRANSACTION ID
    # ========================================

    transaction_id = generate_transaction_id()

    # ========================================
    # CREATE ONE TIMESTAMP
    # ========================================

    transaction_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # ========================================
    # TRANSFER MONEY
    # ========================================

    customer["balance"] -= amount

    receiver["balance"] += amount

    # ========================================
    # SENDER TRANSACTION
    # ========================================

    sender_transaction = {

        "transaction_id": transaction_id,

        "type": "Transfer Sent",

        "amount": amount,

        "date": transaction_date,

        "sender_name": customer["name"],

        "sender_account": customer["account_no"],

        "receiver_name": receiver["name"],

        "receiver_account": receiver["account_no"]
    }

    # ========================================
    # RECEIVER TRANSACTION
    # ========================================

    receiver_transaction = {

        "transaction_id": transaction_id,

        "type": "Transfer Received",

        "amount": amount,

        "date": transaction_date,

        "sender_name": customer["name"],

        "sender_account": customer["account_no"],

        "receiver_name": receiver["name"],

        "receiver_account": receiver["account_no"],

        "status" : "SUCCESS"
    }

    # ========================================
    # MAKE SURE TRANSACTION LISTS EXIST
    # ========================================

    if "transactions" not in customer:

        customer["transactions"] = []

    if "transactions" not in receiver:

        receiver["transactions"] = []

    # ========================================
    # SAVE TRANSACTIONS
    # ========================================

    customer["transactions"].append(
        sender_transaction
    )

    receiver["transactions"].append(
        receiver_transaction
    )

    # ========================================
    # SAVE DATA
    # ========================================

    save_customers()

    # ========================================
    # TRANSFER RECEIPT
    # ========================================

    print("\n========================================")
    print("            TRANSFER RECEIPT")
    print("========================================")

    print(
        "Status              : SUCCESS"
    )

    print(
        "Transaction ID      :",
        transaction_id
    )

    print(
        "Sender Name         :",
        customer["name"]
    )

    print(
        "Sender Account No.  :",
        customer["account_no"]
    )

    print(
        "Receiver Name       :",
        receiver["name"]
    )

    print(
        "Receiver Account No.:",
        receiver["account_no"]
    )

    print(
        "Amount              : ₹",
        format(amount, ".2f")
    )

    print(
        "Remaining Balance   : ₹",
        format(customer["balance"], ".2f")
    )

    print(
        "Date & Time         :",
        transaction_date
    )

    print("========================================")

#=========================================
# ADMIN LOGIN
# ========================================

def admin_login():
    print("\n----------ADMIN LOGING----------")
    print("")
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("\nLogin sucessfull!")
        return True
    print("\nInvalid Admin Username or Password.")

    return False

#==========================================
# admin see all the customers
#==========================================
def view_all_customers():

    print("\n========================================")
    print("          ALL CUSTOMER DETAILS")
    print("========================================")

    if len(customers) == 0:

        print("No customers registered.")
        return

    for customer in customers:

        print("\n----------------------------------------")

        # ================================
        # CUSTOMER DETAILS
        # ================================

        print(
            "Account Number   :",
            customer.get("account_no")
        )

        print(
            "Customer Name    :",
            customer.get("name")
        )

        print(
            "Mobile Number    :",
            customer.get(
                "mobile",
                "Not available"
            )
        )

        # Mobile verification
        if customer.get(
            "mobile_verified",
            False
        ):

            print("Mobile Verified  : YES")

        else:

            print("Mobile Verified  : NO")

        print(
            "Email            :",
            customer.get(
                "email",
                "Not available"
            )
        )

        print(
            "Email Type       :",
            customer.get(
                "email_type",
                "Not available"
            )
        )

        print(
            "Aadhaar          :",
            customer.get(
                "aadhaar",
                "Not available"
            )
        )

        print(
            "Account Status   :",
            customer.get(
                "status",
                "Active"
            )
        )

        print(
            "Balance          : ₹",
            format(
                customer.get(
                    "balance",
                    0
                ),
                ".2f"
            )
        )

        # ================================
        # TRANSACTIONS
        # ================================

        transactions = customer.get(
            "transactions",
            []
        )

        print(
            "Total Transactions:",
            len(transactions)
        )

        if len(transactions) > 0:

            print("\nTransaction History:")

            for transaction in transactions:

                print("DEBUG TRANSACTION:", transaction)

                transaction_id = transaction.get(
                    "transaction_id"
                )

                if transaction_id is None:
                    transaction_id = "ID not avalable"

                # Support both date and timestamp
                date_time = transaction.get(
                    "date",
                    transaction.get(
                        "timestamp",
                        "Date not available"
                    )
                )

                transaction_type = transaction.get(
                    "type",
                    "Unknown"
                )

                amount = transaction.get(
                    "amount",
                    0
                )

                print(
                    "\n  Transaction ID :",
                    transaction_id
                )

                print(
                    "  Date           :",
                    date_time
                )

                print(
                    "  Type           :",
                    transaction_type
                )

                print(
                    "  Amount         : ₹",
                    format(
                        amount,
                        ".2f"
                    )
                )

                print(
                    "  --------------------------"
                )

        else:

            print("No transactions found.")

    print("\n========================================")

    input(
        "\nPress Enter to return to Admin Dashboard..."
    )
#==========================================
#BANKING STATISTICS
#==========================================
def banking_statistics():

    print("\n========================================")
    print("          BANKING STATISTICS")
    print("========================================")

    if len(customers) == 0:

        print("No customers registered.")

        return

    total_customers = len(customers)

    total_balance = 0

    highest_balance = customers[0].get("balance", 0)

    lowest_balance = customers[0].get("balance", 0)

    for customer in customers:

        balance = customer.get("balance", 0)

        total_balance += balance

        if balance > highest_balance:

            highest_balance = balance

        if balance < lowest_balance:

            lowest_balance = balance

    average_balance = total_balance / total_customers

    print("Total Customers    :", total_customers)

    print("Total Bank Balance : ₹", format(total_balance, ".2f"))

    print("Highest Balance    : ₹", format(highest_balance, ".2f"))

    print("Lowest Balance     : ₹", format(lowest_balance, ".2f"))

    print("Average Balance    : ₹", format(average_balance, ".2f"))

    print("========================================")

#=========================================
#Search customer ny account number
#==========================================
def search_customer():

    print("\n========================================")
    print("          SEARCH CUSTOMER")
    print("========================================")

    try:
        account_number = int(
            input("Enter Account Number: ")
        )

    except ValueError:
        print("Account Number must be a number.")
        return

    found_customer = None

    # Search customer
    for customer in customers:

        if customer.get("account_no") == account_number:

            found_customer = customer
            break

    # Customer not found
    if found_customer is None:

        print("\nCustomer not found.")
        return

    # ========================================
    # CUSTOMER DETAILS
    # ========================================

    print("\n========================================")
    print("         CUSTOMER DETAILS")
    print("========================================")

    print(
        "Account Number   :",
        found_customer.get("account_no")
    )

    print(
        "Customer Name    :",
        found_customer.get("name")
    )

    print(
        "Mobile Number    :",
        found_customer.get(
            "mobile",
            "Not available"
        )
    )

    # Mobile verification status
    if found_customer.get(
        "mobile_verified",
        False
    ):

        print("Mobile Verified  : YES")

    else:

        print("Mobile Verified  : NO")

    print(
        "Email            :",
        found_customer.get(
            "email",
            "Not available"
        )
    )

    print(
        "Email Type       :",
        found_customer.get(
            "email_type",
            "Not available"
        )
    )

    print(
        "Aadhaar          :",
        found_customer.get(
            "aadhaar",
            "Not available"
        )
    )

    print(
        "Account Status   :",
        found_customer.get(
            "status",
            "Active"
        )
    )

    print(
        "Balance          : ₹",
        format(
            found_customer.get(
                "balance",
                0
            ),
            ".2f"
        )
    )

    # ========================================
    # TRANSACTION COUNT
    # ========================================

    transactions = found_customer.get(
        "transactions",
        []
    )

    print(
        "Total Transactions:",
        len(transactions)
    )

    # ========================================
    # TRANSACTION HISTORY
    # ========================================

    print("\n========================================")
    print("         TRANSACTION HISTORY")
    print("========================================")

    if not transactions:

        print("No transactions found.")

    else:

        for index, transaction in enumerate(
            transactions,
            start=1
        ):

            # Transaction ID
            transaction_id = transaction.get(
                "transaction_id",
                "Not available"
            )

            # Date / Time
            if "date" in transaction:

                date_time = transaction["date"]

            elif "timestamp" in transaction:

                date_time = transaction["timestamp"]

            else:

                date_time = "Date not available"

            # Transaction type
            transaction_type = transaction.get(
                "type",
                "Unknown"
            )

            # Amount
            amount = transaction.get(
                "amount",
                0
            )

            print(
                "\nTransaction",
                index
            )

            print(
                "Transaction ID :",
                transaction_id
            )

            print(
                "Date           :",
                date_time
            )

            print(
                "Type           :",
                transaction_type
            )

            print(
                "Amount         : ₹",
                format(
                    amount,
                    ".2f"
                )
            )

            print("----------------------------------------")

    print("========================================")

    input(
        "\nPress Enter to return to Admin Dashboard..."
    )

#========================================
#SEARCH TRANSACTIONS
#=========================================
def search_transactions():

    while True:

        print("\n========================================")
        print("       TRANSACTION SEARCH")
        print("========================================")

        print("1. Search Deposits")
        print("2. Search Withdrawals")
        print("3. Search Transfers")
        print("4. Back")

        choice = input(
            "\nEnter your choice (1-4): "
        ).strip()

        if choice == "1":

            search_type = "Deposit"

        elif choice == "2":

            search_type = "Withdrawal"

        elif choice == "3":

            search_type = "Transfer"

        elif choice == "4":

            return

        else:

            print("\nInvalid Choice.")
            continue

        print("\n========================================")
        print("Searching:", search_type)
        print("========================================")

        found = False

        for customer in customers:

            transactions = customer.get(
                "transactions",
                []
            )

            for transaction in transactions:

                transaction_type = transaction.get(
                    "type",
                    ""
                )

                # Get transaction ID
                transaction_id = transaction.get(
                    "transaction_id",
                    "Old Transaction"
                )

                # Get date
                date_time = transaction.get(
                    "date",
                    transaction.get(
                        "timestamp",
                        "Date not available"
                    )
                )

                # Get amount
                amount = transaction.get(
                    "amount",
                    0
                )

                # Transfer search
                if search_type == "Transfer":

                    if "Transfer" in transaction_type:

                        print(
                            "Customer       :",
                            customer.get("name")
                        )

                        print(
                            "Account        :",
                            customer.get("account_no")
                        )

                        print(
                            "Transaction ID :",
                            transaction_id
                        )

                        print(
                            "Date           :",
                            date_time
                        )

                        print(
                            "Type           :",
                            transaction_type
                        )

                        print(
                            "Amount         : ₹",
                            format(
                                amount,
                                ".2f"
                            )
                        )

                        print("----------------------------------------")

                        found = True

                # Deposit / Withdrawal search
                else:

                    if transaction_type == search_type:

                        print(
                            "Customer       :",
                            customer.get("name")
                        )

                        print(
                            "Account        :",
                            customer.get("account_no")
                        )

                        print(
                            "Transaction ID :",
                            transaction_id
                        )

                        print(
                            "Date           :",
                            date_time
                        )

                        print(
                            "Type           :",
                            transaction_type
                        )

                        print(
                            "Amount         : ₹",
                            format(
                                amount,
                                ".2f"
                            )
                        )

                        print("----------------------------------------")

                        found = True

        if not found:

            print(
                "No",
                search_type,
                "transactions found."
            )

        print("========================================")

        input("\nPress Enter to continue...")

#=========================================
#CHANGE ACCOUNT STATUS
#========================================
def change_account_status():

    print("\n========================================")
    print("       CHANGE ACCOUNT STATUS")
    print("========================================")

    try:
        account_number = int(
            input("Enter Account Number: ")
        )

    except ValueError:
        print("Account Number must be a number.")
        return

    found_customer = None

    # Find the customer
    for customer in customers:

        if customer.get("account_no") == account_number:

            found_customer = customer
            break

    # If account does not exist
    if found_customer is None:

        print("\nCustomer not found.")
        return

    # Get current status
    current_status = found_customer.get(
        "status",
        "Active"
    )

    print("\nCustomer Name :", found_customer.get("name"))
    print("Current Status:", current_status)

    print("\n1. Activate Account")
    print("2. Deactivate Account")
    print("3. Cancel")

    choice = input(
        "\nEnter your choice (1-3): "
    ).strip()

    if choice == "1":

        found_customer["status"] = "Active"

        save_customers()

        print("\nAccount activated successfully.")

    elif choice == "2":

        found_customer["status"] = "Inactive"

        save_customers()

        print("\nAccount deactivated successfully.")

    elif choice == "3":

        print("\nOperation cancelled.")

    else:

        print("\nInvalid Choice.")

#===========================================
#closing customer account
#============================================
def close_customer_account():

    print("\n========================================")
    print("        CLOSE CUSTOMER ACCOUNT")
    print("========================================")

    try:
        account_number = int(
            input("Enter Account Number: ")
        )

    except ValueError:
        print("Account Number must be a number.")
        return

    found_customer = None

    # Find customer
    for customer in customers:

        if customer.get("account_no") == account_number:

            found_customer = customer
            break

    # Customer not found
    if found_customer is None:

        print("\nCustomer not found.")
        return

    current_status = found_customer.get(
        "status",
        "Active"
    )

    # Already closed
    if current_status == "Closed":

        print("\n========================================")
        print("       ACCOUNT ALREADY CLOSED")
        print("========================================")

        print(
            "This customer account is already closed."
        )

        return

    # Customer details
    print("\nCustomer Name :",
          found_customer.get("name"))

    print("Account Number:",
          found_customer.get("account_no"))

    print("Current Status:",
          current_status)

    print("Balance       : ₹",
          format(
              found_customer.get("balance", 0),
              ".2f"
          ))

    # Confirmation
    confirmation = input(
        "\nAre you sure you want to close this account? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":

        found_customer["status"] = "Closed"

        save_customers()

        print("\n========================================")
        print("       ACCOUNT CLOSED SUCCESSFULLY")
        print("========================================")

        print(
            "Account Number:",
            found_customer.get("account_no")
        )

        print(
            "Customer Name :",
            found_customer.get("name")
        )

        print(
            "Account Status: Closed"
        )

        print("========================================")

    elif confirmation == "no":

        print(
            "\nAccount closing cancelled."
        )

    else:

        print(
            "\nInvalid choice. "
            "Please enter yes or no."
        )

#====================================
#admin banking summary
#====================================
def banking_summary():

    print("\n========================================")
    print("           BANKING SUMMARY")
    print("========================================")

    total_customers = len(customers)

    active_accounts = 0
    inactive_accounts = 0
    closed_accounts = 0

    total_balance = 0
    total_deposits = 0
    total_withdrawals = 0
    total_transfers = 0
    total_transactions = 0

    for customer in customers:

        # ================================
        # ACCOUNT STATUS
        # ================================

        status = customer.get(
            "status",
            "Active"
        )

        if status == "Active":

            active_accounts += 1

        elif status == "Inactive":

            inactive_accounts += 1

        elif status == "Closed":

            closed_accounts += 1

        # ================================
        # BALANCE
        # ================================

        total_balance += customer.get(
            "balance",
            0
        )

        # ================================
        # TRANSACTIONS
        # ================================

        transactions = customer.get(
            "transactions",
            []
        )

        total_transactions += len(
            transactions
        )

        for transaction in transactions:

            transaction_type = transaction.get(
                "type",
                ""
            )

            amount = transaction.get(
                "amount",
                0
            )

            # ============================
            # DEPOSITS
            # ============================

            if transaction_type in [
                "Deposit",
                "Initial Deposit"
            ]:

                total_deposits += amount

            # ============================
            # WITHDRAWALS
            # ============================

            elif transaction_type == "Withdrawal":

                total_withdrawals += amount

            # ============================
            # TRANSFERS
            # ============================

            elif transaction_type == "Transfer Sent":

                total_transfers += amount

    # ====================================
    # DISPLAY SUMMARY
    # ====================================

    print(
        "Total Customers       :",
        total_customers
    )

    print(
        "Active Accounts       :",
        active_accounts
    )

    print(
        "Inactive Accounts     :",
        inactive_accounts
    )

    print(
        "Closed Accounts       :",
        closed_accounts
    )

    print(
        "\nTotal Bank Balance    : ₹",
        format(
            total_balance,
            ".2f"
        )
    )

    print(
        "Total Deposits        : ₹",
        format(
            total_deposits,
            ".2f"
        )
    )

    print(
        "Total Withdrawals     : ₹",
        format(
            total_withdrawals,
            ".2f"
        )
    )

    print(
        "Total Transfers       : ₹",
        format(
            total_transfers,
            ".2f"
        )
    )

    print(
        "Total Transactions    :",
        total_transactions
    )

    print("========================================")

    input(
        "\nPress Enter to return to Admin Dashboard..."
    )

#==========================================
#detailed customer search
#=======================================
def detailed_customer_search():

    print("\n========================================")
    print("          CUSTOMER SEARCH")
    print("========================================")

    try:
        account_number = int(
            input("Enter Account Number: ")
        )

    except ValueError:
        print("Account Number must be a number.")
        return

    found_customer = None

    for customer in customers:

        if customer.get("account_no") == account_number:
            found_customer = customer
            break

    if found_customer is None:

        print("\nCustomer not found.")
        return

    print("\n========================================")
    print("          CUSTOMER DETAILS")
    print("========================================")

    print(
        "Name           :",
        found_customer.get("name")
    )

    print(
        "Account Number :",
        found_customer.get("account_no")
    )

    print(
        "Status         :",
        found_customer.get("status", "Active")
    )

    print(
        "Balance        : ₹",
        format(
            found_customer.get("balance", 0),
            ".2f"
        )
    )

    transactions = found_customer.get(
        "transactions",
        []
    )

    total_deposits = 0
    total_withdrawals = 0
    total_transfers = 0

    for transaction in transactions:

        transaction_type = transaction.get(
            "type",
            ""
        )

        amount = transaction.get(
            "amount",
            0
        )

        if transaction_type == "Deposit":

            total_deposits += amount

        elif transaction_type == "Withdrawal":

            total_withdrawals += amount

        elif transaction_type == "Transfer Sent":

            total_transfers += amount

    print(
        "\nTotal Transactions :",
        len(transactions)
    )

    print(
        "Total Deposits     : ₹",
        format(total_deposits, ".2f")
    )

    print(
        "Total Withdrawals  : ₹",
        format(total_withdrawals, ".2f")
    )

    print(
        "Total Transfers    : ₹",
        format(total_transfers, ".2f")
    )

    print("\n----------------------------------------")
    print("          TRANSACTION HISTORY")
    print("----------------------------------------")

    if len(transactions) == 0:

        print("No transactions found.")

    else:

        for index, transaction in enumerate(
            transactions,
            start=1
        ):

            print(
                f"\n{index}.",
                transaction.get(
                    "type",
                    "Unknown"
                )
            )

            print(
                "   Amount : ₹",
                format(
                    transaction.get("amount", 0),
                    ".2f"
                )
            )

            print(
                "   Date   :",
                transaction.get(
                    "date",
                    "Date not available"
                )
            )

    print("\n========================================")

#----------------------------------------
#filtering transactions
#---------------------------------------
def filter_transactions():

    print("\n========================================")
    print("       TRANSACTION FILTER")
    print("========================================")

    print("\n1. Deposit")
    print("2. Withdrawal")
    print("3. Transfer Sent")
    print("4. Transfer Received")
    print("5. All Transactions")
    print("6. Back")

    choice = input(
        "\nEnter your choice (1-6): "
    ).strip()

    transaction_types = {
        "1": "Deposit",
        "2": "Withdrawal",
        "3": "Transfer Sent",
        "4": "Transfer Received"
    }

    # Back
    if choice == "6":

        print("\nReturning to Admin Dashboard...")
        return

    # All transactions
    if choice == "5":

        selected_type = None

    # Selected transaction type
    elif choice in transaction_types:

        selected_type = transaction_types[choice]

    else:

        print("\nInvalid Choice.")
        return

    found = False

    print("\n========================================")
    print("          TRANSACTION RESULTS")
    print("========================================")

    for customer in customers:

        transactions = customer.get(
            "transactions",
            []
        )

        for transaction in transactions:

            transaction_type = transaction.get(
                "type",
                "Unknown"
            )

            # =================================
            # CHECK SELECTED TRANSACTION
            # =================================

            if selected_type == "Deposit":

                # Include both Deposit and Initial Deposit
                if transaction_type not in [
                    "Deposit",
                    "Initial Deposit"
                ]:
                    continue

            elif (
                selected_type is not None
                and transaction_type != selected_type
            ):

                continue

            # =================================
            # TRANSACTION FOUND
            # =================================

            found = True

            transaction_id = transaction.get(
                "transaction_id",
                "ID not available"
            )

            # Support date and timestamp
            date_time = transaction.get(
                "date",
                transaction.get(
                    "timestamp",
                    "Date not available"
                )
            )

            amount = transaction.get(
                "amount",
                0
            )

            print("\nCustomer       :",
                  customer.get("name"))

            print("Account Number :",
                  customer.get("account_no"))

            print("Transaction ID :",
                  transaction_id)

            print("Transaction    :",
                  transaction_type)

            print(
                "Amount         : ₹",
                format(
                    amount,
                    ".2f"
                )
            )

            print(
                "Date & Time    :",
                date_time
            )

            print("----------------------------------------")

    if not found:

        if selected_type == "Deposit":

            print(
                "\nNo Deposit transactions found."
            )

        elif selected_type is not None:

            print(
                "\nNo",
                selected_type,
                "transactions found."
            )

        else:

            print(
                "\nNo transactions found."
            )

    print("========================================")

    input(
        "\nPress Enter to return to Admin Dashboard..."
    )

#====================================
#search transaction by transaction id
#====================================
def search_transaction_by_id():

    print("\n========================================")
    print("       SEARCH TRANSACTION BY ID")
    print("========================================")

    transaction_id = input(
        "\nEnter Transaction ID: "
    ).strip()

    if not transaction_id:

        print("\nTransaction ID cannot be empty.")
        return

    found_transactions = []

    # ========================================
    # SEARCH ALL CUSTOMERS
    # ========================================

    for customer in customers:

        transactions = customer.get(
            "transactions",
            []
        )

        for transaction in transactions:

            if transaction.get(
                "transaction_id"
            ) == transaction_id:

                found_transactions.append(
                    transaction
                )

    # ========================================
    # TRANSACTION NOT FOUND
    # ========================================

    if not found_transactions:

        print(
            "\nTransaction not found."
        )

        return

    # ========================================
    # DISPLAY TRANSACTION
    # ========================================

    print("\n========================================")
    print("       TRANSACTION DETAILS")
    print("========================================")

    # Usually a transfer has two records:
    # Transfer Sent
    # Transfer Received

    transaction = found_transactions[0]

    print(
        "Transaction ID   :",
        transaction.get(
            "transaction_id",
            "Not available"
        )
    )

    print(
        "Transaction Type :",
        transaction.get(
            "type",
            "Unknown"
        )
    )

    print(
        "Amount           : ₹",
        format(
            transaction.get(
                "amount",
                0
            ),
            ".2f"
        )
    )

    print(
        "Status           :",
        transaction.get(
            "status",
            "SUCCESS"
        )
    )

    print(
        "Date & Time      :",
        transaction.get(
            "date",
            "Date not available"
        )
    )

    print(
        "Sender Name      :",
        transaction.get(
            "sender_name",
            "Not available"
        )
    )

    print(
        "Sender Account   :",
        transaction.get(
            "sender_account",
            "Not available"
        )
    )

    print(
        "Receiver Name    :",
        transaction.get(
            "receiver_name",
            "Not available"
        )
    )

    print(
        "Receiver Account :",
        transaction.get(
            "receiver_account",
            "Not available"
        )
    )

    print("========================================")



# export all transactions
def export_all_transactions():

    print("\n========================================")
    print("       EXPORT ALL TRANSACTIONS")
    print("========================================")

    filename = "all_transactions.csv"

    total_transactions = 0

    try:

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            # ====================================
            # CSV HEADER
            # ====================================

            writer.writerow([
                "Transaction ID",
                "Customer Name",
                "Customer Account",
                "Transaction Type",
                "Amount",
                "Status",
                "Date & Time",
                "Sender Name",
                "Sender Account",
                "Receiver Name",
                "Receiver Account"
            ])

            # ====================================
            # ALL CUSTOMERS
            # ====================================

            for customer in customers:

                transactions = customer.get(
                    "transactions",
                    []
                )

                for transaction in transactions:

                    writer.writerow([

                        transaction.get(
                            "transaction_id",
                            "Not available"
                        ),

                        customer.get(
                            "name",
                            "Not available"
                        ),

                        customer.get(
                            "account_no",
                            "Not available"
                        ),

                        transaction.get(
                            "type",
                            "Unknown"
                        ),

                        transaction.get(
                            "amount",
                            0
                        ),

                        transaction.get(
                            "status",
                            "SUCCESS"
                        ),

                        transaction.get(
                            "date",
                            "Not available"
                        ),

                        transaction.get(
                            "sender_name",
                            "Not available"
                        ),

                        transaction.get(
                            "sender_account",
                            "Not available"
                        ),

                        transaction.get(
                            "receiver_name",
                            "Not available"
                        ),

                        transaction.get(
                            "receiver_account",
                            "Not available"
                        )
                    ])

                    total_transactions += 1

        # ========================================
        # SUCCESS
        # ========================================

        print("\n========================================")
        print("       EXPORT SUCCESSFUL")
        print("========================================")

        print(
            "File Name:",
            filename
        )

        print(
            "Total Transactions:",
            total_transactions
        )

        print("========================================")

    except Exception as error:

        print("\n========================================")
        print("          EXPORT FAILED")
        print("========================================")

        print(
            "Error:",
            error
        )

        print("========================================")

    input(
        "\nPress Enter to return..."
    
    )

#admin transaction statistics

def admin_transaction_statistics():

    print("\n========================================")
    print("       TRANSACTION STATISTICS")
    print("========================================")

    total_transactions = 0

    # Transaction counts
    deposit_count = 0
    withdrawal_count = 0
    transfer_sent_count = 0
    transfer_received_count = 0

    # Transaction amounts
    total_deposits = 0
    total_withdrawals = 0
    total_transfer_sent = 0
    total_transfer_received = 0

    # ========================================
    # PROCESS ALL CUSTOMERS
    # ========================================

    for customer in customers:

        transactions = customer.get(
            "transactions",
            []
        )

        for transaction in transactions:

            transaction_type = transaction.get(
                "type",
                ""
            )

            amount = transaction.get(
                "amount",
                0
            )

            try:

                amount = float(amount)

            except (ValueError, TypeError):

                amount = 0

            total_transactions += 1

            # ====================================
            # DEPOSIT
            # ====================================

            if transaction_type == "Deposit":

                deposit_count += 1

                total_deposits += amount

            # ====================================
            # WITHDRAWAL
            # ====================================

            elif transaction_type == "Withdrawal":

                withdrawal_count += 1

                total_withdrawals += amount

            # ====================================
            # TRANSFER SENT
            # ====================================

            elif transaction_type == "Transfer Sent":

                transfer_sent_count += 1

                total_transfer_sent += amount

            # ====================================
            # TRANSFER RECEIVED
            # ====================================

            elif transaction_type == "Transfer Received":

                transfer_received_count += 1

                total_transfer_received += amount

    # ========================================
    # DISPLAY SUMMARY
    # ========================================

    print(
        "\nTotal Transactions      :",
        total_transactions
    )

    print("\n----------------------------------------")
    print("          TRANSACTION COUNTS")
    print("----------------------------------------")

    print(
        "Deposit Count           :",
        deposit_count
    )

    print(
        "Withdrawal Count        :",
        withdrawal_count
    )

    print(
        "Transfer Sent Count     :",
        transfer_sent_count
    )

    print(
        "Transfer Received Count:",
        transfer_received_count
    )

    print("\n----------------------------------------")
    print("          TRANSACTION AMOUNTS")
    print("----------------------------------------")

    print(
        "Total Deposits          : ₹",
        format(
            total_deposits,
            ".2f"
        )
    )

    print(
        "Total Withdrawals       : ₹",
        format(
            total_withdrawals,
            ".2f"
        )
    )

    print(
        "Total Transfer Sent     : ₹",
        format(
            total_transfer_sent,
            ".2f"
        )
    )

    print(
        "Total Transfer Received : ₹",
        format(
            total_transfer_received,
            ".2f"
        )
    )

    print("\n========================================")

    input(
        "\nPress Enter to return..."
    )

# admin customer statistics

def admin_customer_statistics():

    print("\n========================================")
    print("       CUSTOMER STATISTICS")
    print("========================================")

    total_customers = len(customers)

    active_accounts = 0
    inactive_accounts = 0
    closed_accounts = 0

    total_balance = 0

    # ========================================
    # PROCESS CUSTOMERS
    # ========================================

    for customer in customers:

        status = customer.get(
            "status",
            "Active"
        )

        balance = customer.get(
            "balance",
            0
        )

        try:
            balance = float(balance)

        except (ValueError, TypeError):
            balance = 0

        total_balance += balance

        # ====================================
        # ACCOUNT STATUS
        # ====================================

        if status == "Active":

            active_accounts += 1

        elif status == "Inactive":

            inactive_accounts += 1

        elif status == "Closed":

            closed_accounts += 1

    # ========================================
    # AVERAGE BALANCE
    # ========================================

    if total_customers > 0:

        average_balance = (
            total_balance / total_customers
        )

    else:

        average_balance = 0

    # ========================================
    # DISPLAY
    # ========================================

    print(
        "\nTotal Customers      :",
        total_customers
    )

    print("\n----------------------------------------")
    print("          ACCOUNT STATUS")
    print("----------------------------------------")

    print(
        "Active Accounts      :",
        active_accounts
    )

    print(
        "Inactive Accounts    :",
        inactive_accounts
    )

    print(
        "Closed Accounts      :",
        closed_accounts
    )

    print("\n----------------------------------------")
    print("          BALANCE SUMMARY")
    print("----------------------------------------")

    print(
        "Total Bank Balance   : ₹",
        format(
            total_balance,
            ".2f"
        )
    )

    print(
        "Average Balance      : ₹",
        format(
            average_balance,
            ".2f"
        )
    )

    print("\n========================================")

    input(
        "\nPress Enter to return..."
    )
#admin dashboard summary

def admin_dashboard_summary():

    print("\n========================================")
    print("        BANKING SYSTEM SUMMARY")
    print("========================================")

    total_customers = len(customers)

    active_accounts = 0
    inactive_accounts = 0
    closed_accounts = 0

    total_balance = 0

    total_transactions = 0

    total_deposits = 0
    total_withdrawals = 0
    total_transfer_sent = 0
    total_transfer_received = 0

    # ========================================
    # PROCESS ALL CUSTOMERS
    # ========================================

    for customer in customers:

        # ------------------------------------
        # ACCOUNT STATUS
        # ------------------------------------

        status = customer.get(
            "status",
            "Active"
        )

        if status == "Active":

            active_accounts += 1

        elif status == "Inactive":

            inactive_accounts += 1

        elif status == "Closed":

            closed_accounts += 1

        # ------------------------------------
        # BALANCE
        # ------------------------------------

        balance = customer.get(
            "balance",
            0
        )

        try:

            balance = float(balance)

        except (ValueError, TypeError):

            balance = 0

        total_balance += balance

        # ------------------------------------
        # TRANSACTIONS
        # ------------------------------------

        transactions = customer.get(
            "transactions",
            []
        )

        for transaction in transactions:

            total_transactions += 1

            transaction_type = transaction.get(
                "type",
                ""
            )

            amount = transaction.get(
                "amount",
                0
            )

            try:

                amount = float(amount)

            except (ValueError, TypeError):

                amount = 0

            if transaction_type == "Deposit":

                total_deposits += amount

            elif transaction_type == "Withdrawal":

                total_withdrawals += amount

            elif transaction_type == "Transfer Sent":

                total_transfer_sent += amount

            elif transaction_type == "Transfer Received":

                total_transfer_received += amount

    # ========================================
    # AVERAGE BALANCE
    # ========================================

    if total_customers > 0:

        average_balance = (
            total_balance / total_customers
        )

    else:

        average_balance = 0

    # ========================================
    # DISPLAY CUSTOMER SUMMARY
    # ========================================

    print("\n----------------------------------------")
    print("          CUSTOMER SUMMARY")
    print("----------------------------------------")

    print(
        "Total Customers       :",
        total_customers
    )

    print(
        "Active Accounts       :",
        active_accounts
    )

    print(
        "Inactive Accounts     :",
        inactive_accounts
    )

    print(
        "Closed Accounts       :",
        closed_accounts
    )

    # ========================================
    # BALANCE SUMMARY
    # ========================================

    print("\n----------------------------------------")
    print("          BALANCE SUMMARY")
    print("----------------------------------------")

    print(
        "Total Bank Balance    : ₹",
        format(
            total_balance,
            ".2f"
        )
    )

    print(
        "Average Customer Balance: ₹",
        format(
            average_balance,
            ".2f"
        )
    )

    # ========================================
    # TRANSACTION SUMMARY
    # ========================================

    print("\n----------------------------------------")
    print("        TRANSACTION SUMMARY")
    print("----------------------------------------")

    print(
        "Total Transactions    :",
        total_transactions
    )

    print(
        "Total Deposits        : ₹",
        format(
            total_deposits,
            ".2f"
        )
    )

    print(
        "Total Withdrawals     : ₹",
        format(
            total_withdrawals,
            ".2f"
        )
    )

    print(
        "Total Transfer Sent   : ₹",
        format(
            total_transfer_sent,
            ".2f"
        )
    )

    print(
        "Total Transfer Received: ₹",
        format(
            total_transfer_received,
            ".2f"
        )
    )

    print("\n========================================")

    input(
        "\nPress Enter to return..."
    )

#advanced customer search
def advanced_customer_search():

    print("\n========================================")
    print("        CUSTOMER SEARCH")
    print("========================================")

    print("\n1. Search by Account Number")
    print("2. Search by Name")
    print("3. Search by Mobile Number")
    print("4. Search by Email")
    print("5. Back")

    choice = input(
        "\nEnter your choice (1-5): "
    ).strip()

    # ========================================
    # BACK
    # ========================================

    if choice == "5":

        return

    # ========================================
    # SEARCH VALUE
    # ========================================

    search_value = input(
        "\nEnter search value: "
    ).strip()

    if not search_value:

        print("\nSearch value cannot be empty.")

        return

    found_customers = []

    # ========================================
    # SEARCH CUSTOMERS
    # ========================================

    for customer in customers:

        # ------------------------------------
        # ACCOUNT NUMBER
        # ------------------------------------

        if choice == "1":

            try:

                account_no = int(
                    search_value
                )

            except ValueError:

                print(
                    "\nAccount number must be a number."
                )

                return

            if customer.get(
                "account_no"
            ) == account_no:

                found_customers.append(
                    customer
                )

        # ------------------------------------
        # NAME
        # ------------------------------------

        elif choice == "2":

            customer_name = str(
                customer.get(
                    "name",
                    ""
                )
            )

            if search_value.lower() in \
                    customer_name.lower():

                found_customers.append(
                    customer
                )

        # ------------------------------------
        # MOBILE
        # ------------------------------------

        elif choice == "3":

            mobile = str(
                customer.get(
                    "mobile",
                    ""
                )
            )

            if mobile == search_value:

                found_customers.append(
                    customer
                )

        # ------------------------------------
        # EMAIL
        # ------------------------------------

        elif choice == "4":

            email = str(
                customer.get(
                    "email",
                    ""
                )
            )

            if email.lower() == \
                    search_value.lower():

                found_customers.append(
                    customer
                )

        else:

            print("\nInvalid choice.")

            return

    # ========================================
    # NO RESULTS
    # ========================================

    if not found_customers:

        print("\nNo customers found.")

        input(
            "\nPress Enter to return..."
        )

        return

    # ========================================
    # DISPLAY RESULTS
    # ========================================

    print("\n========================================")
    print("        SEARCH RESULTS")
    print("========================================")

    for customer in found_customers:

        print("\n----------------------------------------")

        print(
            "Name          :",
            customer.get(
                "name",
                "Not available"
            )
        )

        print(
            "Account Number:",
            customer.get(
                "account_no",
                "Not available"
            )
        )

        print(
            "Mobile        :",
            customer.get(
                "mobile",
                "Not available"
            )
        )

        print(
            "Email         :",
            customer.get(
                "email",
                "Not available"
            )
        )

        print(
            "Status        :",
            customer.get(
                "status",
                "Active"
            )
        )

        print(
            "Balance       : ₹",
            format(
                customer.get(
                    "balance",
                    0
                ),
                ".2f"
            )
        )

    print("\n========================================")

    print(
        "Customers Found:",
        len(found_customers)
    )

    print("========================================")

    input(
        "\nPress Enter to return..."
    )
#++++++++++++++++++++++++++++++
#admin view customer details
#+++++++++++++++++++++++++++++++
def admin_view_customer_details():

    print("\n========================================")
    print("       CUSTOMER DETAILS")
    print("========================================")

    try:

        account_no = int(
            input("Enter Customer Account Number: ")
        )

    except ValueError:

        print("\nAccount Number must be a number.")
        return

    # ========================================
    # FIND CUSTOMER
    # ========================================

    found_customer = None

    for customer in customers:

        if customer.get("account_no") == account_no:

            found_customer = customer
            break

    if found_customer is None:

        print("\nCustomer account not found.")

        input(
            "\nPress Enter to return..."
        )

        return

    # ========================================
    # CUSTOMER PROFILE
    # ========================================

    print("\n========================================")
    print("          CUSTOMER PROFILE")
    print("========================================")

    print(
        "Name             :",
        found_customer.get(
            "name",
            "Not available"
        )
    )

    print(
        "Account Number   :",
        found_customer.get(
            "account_no",
            "Not available"
        )
    )
    # ========================================
# MASK MOBILE NUMBER
# ========================================

    mobile = found_customer.get(
            "mobile",
                ""
        )

    if mobile:

        mobile = str(mobile)

        if len(mobile) >= 4:

            masked_mobile = (
            "XXXXXX" + mobile[-4:]
            )

        else:

            masked_mobile = "XXXXXX"

    else:

        masked_mobile = "Not available"

    print(
        "Mobile Number    :",
        masked_mobile
        )


     
    

    if found_customer.get(
        "mobile_verified",
        False
    ):

        print("Mobile Verified  : YES")

    else:

        print("Mobile Verified  : NO")

    print(
        "Email            :",
        found_customer.get(
            "email",
            "Not available"
        )
    )

    print(
        "Email Type       :",
        found_customer.get(
            "email_type",
            "Not available"
        )
    )

    # ========================================
    # MASK AADHAAR
    # ========================================

    aadhaar = found_customer.get(
        "aadhaar",
        ""
    )

    if aadhaar:

        aadhaar_string = str(aadhaar)

        if len(aadhaar_string) >= 4:

            masked_aadhaar = (
                "XXXX-XXXX-"
                + aadhaar_string[-4:]
            )

        else:

            masked_aadhaar = "XXXX"

    else:

        masked_aadhaar = "Not available"

    print(
        "Aadhaar          :",
        masked_aadhaar
    )

    print(
        "Account Status   :",
        found_customer.get(
            "status",
            "Active"
        )
    )

    print(
        "Balance          : ₹",
        format(
            found_customer.get(
                "balance",
                0
            ),
            ".2f"
        )
    )

    print("========================================")

    # ========================================
    # TRANSACTION HISTORY
    # ========================================

    transactions = found_customer.get(
        "transactions",
        []
    )

    print("\n========================================")
    print("        TRANSACTION HISTORY")
    print("========================================")

    if not transactions:

        print("\nNo transactions found.")

    else:

        for transaction in transactions:

            print(
                "\n----------------------------------------"
            )

            print(
                "Transaction ID :",
                transaction.get(
                    "transaction_id",
                    "Not available"
                )
            )

            print(
                "Type           :",
                transaction.get(
                    "type",
                    "Unknown"
                )
            )

            print(
                "Amount         : ₹",
                format(
                    transaction.get(
                        "amount",
                        0
                    ),
                    ".2f"
                )
            )

            print(
                "Status         :",
                transaction.get(
                    "status",
                    "SUCCESS"
                )
            )

            print(
                "Date & Time    :",
                transaction.get(
                    "date",
                    "Not available"
                )
            )

    print("\n========================================")

    print(
        "Total Transactions:",
        len(transactions)
    )

    print("========================================")

    input(
        "\nPress Enter to return..."
    )

#def validate_transaction(transaction):

    # ========================================
    # REQUIRED FIELDS
    # ========================================

    required_fields = [
        "transaction_id",
        "type",
        "amount",
        "date"
    ]

    for field in required_fields:

        if field not in transaction:

            print(
                f"Invalid transaction: "
                f"missing {field}"
            )

            return False

    # ========================================
    # VALID TRANSACTION TYPES
    # ========================================

    valid_types = [
        "Deposit",
        "Withdrawal",
        "Transfer Sent",
        "Transfer Received"
    ]

    if transaction["type"] not in valid_types:

        print(
            "Invalid transaction type:",
            transaction["type"]
        )

        return False

    # ========================================
    # VALIDATE AMOUNT
    # ========================================

    try:

        amount = float(
            transaction["amount"]
        )

    except (ValueError, TypeError):

        print(
            "Transaction amount is invalid."
        )

        return False

    # ========================================
    # AMOUNT MUST BE POSITIVE
    # ========================================

    if amount <= 0:

        print(
            "Transaction amount must be "
            "greater than zero."
        )

        return False

    # ========================================
    # MAXIMUM TRANSACTION LIMIT
    # ========================================

    if amount > 1000000:

        print(
            "Transaction exceeds the "
            "maximum allowed amount."
        )

        return False

    return True

#====================================
#validate transactions
#==============================
def validate_transaction(transaction):

    # ========================================
    # REQUIRED FIELDS
    # ========================================

    required_fields = [
        "transaction_id",
        "type",
        "amount",
        "date"
    ]

    for field in required_fields:

        if field not in transaction:

            print(
                f"Invalid transaction: "
                f"missing {field}"
            )

            return False

    # ========================================
    # VALID TRANSACTION TYPES
    # ========================================

    valid_types = [
        "Deposit",
        "Withdrawal",
        "Transfer Sent",
        "Transfer Received"
    ]

    if transaction["type"] not in valid_types:

        print(
            "Invalid transaction type:",
            transaction["type"]
        )

        return False

    # ========================================
    # VALIDATE AMOUNT
    # ========================================

    try:

        amount = float(
            transaction["amount"]
        )

    except (ValueError, TypeError):

        print(
            "Transaction amount is invalid."
        )

        return False

    # ========================================
    # AMOUNT MUST BE POSITIVE
    # ========================================

    if amount <= 0:

        print(
            "Transaction amount must be "
            "greater than zero."
        )

        return False

    # ========================================
    # MAXIMUM TRANSACTION LIMIT
    # ========================================

    if amount > 1000000:

        print(
            "Transaction exceeds the "
            "maximum allowed amount."
        )

        return False

    return True
#=====================
#transaction id exists
#====================
def transaction_id_exists(transaction_id):

    for customer in customers:

        transactions = customer.get(
            "transactions",
            []
        )

        for transaction in transactions:

            if transaction.get(
                "transaction_id"
            ) == transaction_id:

                return True

    return False

#check account is active or not or closed

def check_account_active(customer):

    status = customer.get(
        "status",
        "Active"
    )

    if status == "Inactive":

        print("\n========================================")
        print("          ACCOUNT INACTIVE")
        print("========================================")

        print(
            "This account is currently inactive."
        )

        print(
            "Please contact the bank administrator."
        )

        print("========================================")

        return False

    if status == "Closed":

        print("\n========================================")
        print("           ACCOUNT CLOSED")
        print("========================================")

        print(
            "This account has been permanently closed."
        )

        print(
            "Please contact the bank administrator."
        )

        print("========================================")

        return False

    return True
#==========================================
#admin dashboard
#=========================================

def admin_dashboard():

    while True:

        print("\n================================")
        print("        ADMIN DASHBOARD")
        print("================================")
        print("")

        print("1. View All Customers")
        print("2. Total Customers")
        print("3. Search Customer")
        print("4. Search Transactions")
        print("5. Filter Transactions")
        print("6. Search Transaction by ID")
        print("7. Change Account Status")
        print("8. Close Customer Account")
        print("9. Banking Summary")
        print("10.Export all transactions")
        print("11.Admin transaction statistics")
        print("12.Customer Statistics")
        print("13.Banking System Summary")
        print("14.Advanced Customer Search")
        print("15.Admin View Customers Only")
        print("19.Backup Data")
        print("20.System_health_check")
        print("21. Logout")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            view_all_customers()

        elif choice == "2":

            banking_statistics()

        elif choice == "3":
            search_customer()

        elif choice == "4":
            search_transactions()

        elif choice == "5":
            filter_transactions()

        elif choice == "6":
            search_transaction_by_id()

        elif choice == "7":
            change_account_status()

        elif choice == "8":
            close_customer_account()

        elif choice =="9":
            banking_summary()

        elif choice == "10":
            export_all_transactions()
        elif choice == "11":
            admin_transaction_statistics()
        elif choice == "12":
            admin_customer_statistics()
        elif choice == "13":
            admin_dashboard_summary()
        elif choice == "14":
            advanced_customer_search()
        elif choice == "15":
            admin_view_customer_details()


        elif choice == "19":
            backup_data()
        elif choice == "20":
            system_health_check()
        elif choice == "21":
    
            print("\nAdmin logged out successfully.")

            break

        else:

            print(
                "\nInvalid Choice."
                "Please Enter 1 to 10. 3" 
              )

#=====================================
#change password
#=====================================
# =====================================
# CHANGE PASSWORD
# =====================================

def change_password(customer):

    print("\n========================================")
    print("          CHANGE PASSWORD")
    print("========================================")

    # ========================================
    # CURRENT PASSWORD
    # ========================================

    current_password = getpass(
        "Enter Current Password: "
    )

    stored_password = customer.get(
        "password",
        ""
    )

    # Hash the entered current password
    current_password_hash = hash_password(
        current_password
    )

    # Compare hashed password
    if current_password_hash != stored_password:

        print(
            "\nIncorrect current password."
        )

        return

    # ========================================
    # NEW PASSWORD
    # ========================================

    new_password = getpass(
        "Enter New Password: "
    )

    # Minimum password length
    if len(new_password) < 4:

        print(
            "\nPassword must contain at least 4 characters."
        )

        return

    # ========================================
    # CHECK SAME PASSWORD
    # ========================================

    new_password_hash = hash_password(
        new_password
    )

    if new_password_hash == stored_password:

        print(
            "\nNew password cannot be the same "
            "as your current password."
        )

        return

    # ========================================
    # CONFIRM NEW PASSWORD
    # ========================================

    confirm_password = getpass(
        "Confirm New Password: "
    )

    if new_password != confirm_password:

        print(
            "\nPasswords do not match."
        )

        return

    # ========================================
    # SAVE HASHED PASSWORD
    # ========================================

    customer["password"] = new_password_hash

    save_customers()

    # ========================================
    # SUCCESS
    # ========================================

    print("\n========================================")
    print("    PASSWORD CHANGED SUCCESSFULLY")
    print("========================================")

    print(
        "Your password has been changed securely."
    )

    print("========================================")
#=================================
#account statement
#=================================

def account_statement(customer):

    print("\n========================================")
    print("          ACCOUNT STATEMENT")
    print("========================================")

    print(
        "Customer Name  :",
        customer.get("name", "Not available")
    )

    print(
        "Account Number :",
        customer.get("account_no", "Not available")
    )

    print(
        "Account Status :",
        customer.get("status", "Active")
    )

    print(
        "Current Balance: ₹",
        format(
            customer.get("balance", 0),
            ".2f"
        )
    )

    transactions = customer.get(
        "transactions",
        []
    )

    print("\n========================================")
    print("        TRANSACTION STATEMENT")
    print("========================================")

    if not transactions:

        print("\nNo transactions found.")

        print("========================================")

        input(
            "\nPress Enter to return..."
        )

        return

    for transaction in transactions:

        print("\n----------------------------------------")

        print(
            "Transaction ID :",
            transaction.get(
                "transaction_id",
                "Not available"
            )
        )

        print(
            "Date & Time    :",
            transaction.get(
                "date",
                "Date not available"
            )
        )

        print(
            "Type           :",
            transaction.get(
                "type",
                "Unknown"
            )
        )

        print(
            "Amount         : ₹",
            format(
                transaction.get(
                    "amount",
                    0
                ),
                ".2f"
            )
        )

        print(
            "Status         :",
            transaction.get(
                "status",
                "SUCCESS"
            )
        )

        # ====================================
        # TRANSFER DETAILS
        # ====================================

        transaction_type = transaction.get(
            "type",
            ""
        )

        if transaction_type in [
            "Transfer Sent",
            "Transfer Received"
        ]:

            print(
                "Sender Name    :",
                transaction.get(
                    "sender_name",
                    "Not available"
                )
            )

            print(
                "Sender Account :",
                transaction.get(
                    "sender_account",
                    "Not available"
                )
            )

            print(
                "Receiver Name  :",
                transaction.get(
                    "receiver_name",
                    "Not available"
                )
            )

            print(
                "Receiver Account:",
                transaction.get(
                    "receiver_account",
                    "Not available"
                )
            )

        print("----------------------------------------")

    print(
        "\nTotal Transactions:",
        len(transactions)
    )

    print(
        "Current Balance   : ₹",
        format(
            customer.get("balance", 0),
            ".2f"
        )
    )

    print("========================================")

    input(
        "\nPress Enter to return..."
    )
#============================
#verify mobile otp
#===========================

def verify_mobile_otp(customer):

    import random
    import time

    print("\n========================================")
    print("        MOBILE OTP VERIFICATION")
    print("========================================")

    mobile = customer.get("mobile")

    if not mobile:

        print("\nNo mobile number registered.")
        return False

    # Generate 6-digit OTP
    otp = random.randint(100000, 999999)

    # Record OTP creation time
    otp_created_time = time.time()

    # OTP validity = 2 minutes
    otp_expiry = 120

    # Maximum attempts
    max_attempts = 3

    print("\n[TEST MODE]")
    print("OTP:", otp)

    for attempt in range(1, max_attempts + 1):

        # Check expiry
        elapsed_time = time.time() - otp_created_time

        if elapsed_time > otp_expiry:

            print("\nOTP has expired.")
            print("Please request a new OTP.")

            return False

        entered_otp = input(
            "\nEnter OTP: "
        ).strip()

        # Check OTP
        if entered_otp == str(otp):

            customer["mobile_verified"] = True

            save_customers()

            print("\n========================================")
            print("       MOBILE VERIFIED SUCCESSFULLY")
            print("========================================")

            print(
                "Mobile Number  :",
                mobile
            )

            print(
                "Mobile Verified: YES"
            )

            print("========================================")

            return True

        remaining_attempts = (
            max_attempts - attempt
        )

        if remaining_attempts > 0:

            print(
                "\nIncorrect OTP."
            )

            print(
                "Attempts remaining:",
                remaining_attempts
            )

    print("\n========================================")
    print("       OTP VERIFICATION FAILED")
    print("========================================")

    print(
        "Maximum OTP attempts exceeded."
    )

    print(
        "Please request a new OTP."
    )

    print("========================================")

    return False

#=============================
#customer profile
#=============================
def customer_profile(customer):

    while True:

        print("\n========================================")
        print("          CUSTOMER PROFILE")
        print("========================================")

        print(
            "Name             :",
            customer.get("name", "Not available")
        )

        print(
            "Account Number   :",
            customer.get("account_no", "Not available")
        )

        # ========================================
        # MOBILE
        # ========================================

        mobile = customer.get("mobile")

        if mobile:
            print(
                "Mobile Number    :",
                mobile
            )
        else:
            print(
                "Mobile Number    : Not Registered"
            )

        if customer.get("mobile_verified", False):
            print("Mobile Verified  : YES")
        else:
            print("Mobile Verified  : NO")

        # ========================================
        # EMAIL
        # ========================================

        print(
            "Email            :",
            customer.get("email", "Not available")
        )

        print(
            "Email Type       :",
            customer.get("email_type", "Not available")
        )

        # ========================================
        # AADHAAR
        # ========================================

        print(
            "Aadhaar          :",
            customer.get("aadhaar", "Not available")
        )

        # ========================================
        # ACCOUNT DETAILS
        # ========================================

        print(
            "Account Status   :",
            customer.get("status", "Active")
        )

        print(
            "Balance          : ₹",
            format(
                customer.get("balance", 0),
                ".2f"
            )
        )

        print("========================================")

        print("\n1. Add / Update Mobile")
        print("2. Add / Update Email")
        print("3. Add / Update Aadhaar")
        print("4. Back")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        # ========================================
        # MOBILE
        # ========================================

        if choice == "1":

            print("\n------ ADD / UPDATE MOBILE ------")

            while True:

                mobile = input(
                    "Enter Mobile Number: "
                ).strip()

                if not mobile.isdigit():

                    print(
                        "Mobile number must contain only digits."
                    )

                    continue

                if len(mobile) != 10:

                    print(
                        "Mobile number must contain exactly 10 digits."
                    )

                    continue

                if mobile[0] not in "6789":

                    print(
                        "Mobile number must start with 6, 7, 8 or 9."
                    )

                    continue

                # Check duplicate mobile

                mobile_exists = False

                for existing_customer in customers:

                    if (
                        existing_customer.get("mobile")
                        == mobile
                        and existing_customer.get("account_no")
                        != customer.get("account_no")
                    ):

                        mobile_exists = True

                        break

                if mobile_exists:

                    print(
                        "This mobile number is already "
                        "registered with another account."
                    )

                    continue

                break

            customer["mobile"] = mobile

            # Mobile needs verification
            customer["mobile_verified"] = False

            save_customers()

            print(
                "\nMobile number saved successfully."
            )

            print(
                "Mobile Verified is required."
            )
            verify_mobile_otp(customer)

           

        # ========================================
        # EMAIL
        # ========================================

        elif choice == "2":

            print("\n------ ADD / UPDATE EMAIL ------")

            while True:

                email = input(
                    "Enter Email: "
                ).strip().lower()

                if email.count("@") != 1:

                    print(
                        "Invalid email format."
                    )

                    continue

                if not email.endswith("@gmail.com"):

                    print(
                        "Personal email must end with @gmail.com."
                    )

                    continue

                # Basic validation before @gmail.com
                username = email.split("@")[0]

                if username == "":

                    print(
                        "Invalid email format."
                    )

                    continue

                break

            customer["email"] = email
            customer["email_type"] = "Personal"

            save_customers()

            print(
                "\nEmail updated successfully."
            )

        # ========================================
        # AADHAAR
        # ========================================

        elif choice == "3":

            print("\n------ ADD / UPDATE AADHAAR ------")

            while True:

                aadhaar = input(
                    "Enter 12-digit Aadhaar Number: "
                ).strip()

                # Check digits only

                if not aadhaar.isdigit():

                    print(
                        "Aadhaar must contain only digits."
                    )

                    continue

                # Check exactly 12 digits

                if len(aadhaar) != 12:

                    print(
                        "Aadhaar must contain exactly 12 digits."
                    )

                    continue

                break

            # ------------------------------------
            # MASK AADHAAR
            # ------------------------------------

            masked_aadhaar = (
                "XXXX-XXXX-" + aadhaar[-4:]
            )

            customer["aadhaar"] = masked_aadhaar

            save_customers()

            print(
                "\nAadhaar updated successfully."
            )

            print(
                "Stored Aadhaar:",
                masked_aadhaar
            )

        # ========================================
        # BACK
        # ========================================

        elif choice == "4":

            return

        else:

            print(
                "\nInvalid choice."
            )

#========================
#filter transaction by date
#==========================
def filter_transactions_by_date(customer):

    print("\n========================================")
    print("       TRANSACTION DATE FILTER")
    print("========================================")

    date_input = input(
        "\nEnter Date (YYYY-MM-DD): "
    ).strip()

    if not date_input:

        print("\nDate cannot be empty.")
        return

    # Validate date format
    try:

        datetime.strptime(
            date_input,
            "%Y-%m-%d"
        )

    except ValueError:

        print(
            "\nInvalid date format."
        )

        print(
            "Please use YYYY-MM-DD."
        )

        return

    transactions = customer.get(
        "transactions",
        []
    )

    found = False

    print("\n========================================")
    print("       TRANSACTIONS ON", date_input)
    print("========================================")

    for transaction in transactions:

        transaction_date = transaction.get(
            "date",
            ""
        )

        # Get only YYYY-MM-DD
        transaction_day = transaction_date[:10]

        if transaction_day == date_input:

            found = True

            print("\n----------------------------------------")

            print(
                "Transaction ID :",
                transaction.get(
                    "transaction_id",
                    "Not available"
                )
            )

            print(
                "Type           :",
                transaction.get(
                    "type",
                    "Unknown"
                )
            )

            print(
                "Amount         : ₹",
                format(
                    transaction.get(
                        "amount",
                        0
                    ),
                    ".2f"
                )
            )

            print(
                "Status         :",
                transaction.get(
                    "status",
                    "SUCCESS"
                )
            )

            print(
                "Date & Time    :",
                transaction.get(
                    "date",
                    "Date not available"
                )
            )

    if not found:

        print(
            "\nNo transactions found "
            "for this date."
        )

    print("\n========================================")

    input(
        "\nPress Enter to return..."
    
    )

#========================
#filter transactions by date range
#==========================
def filter_transactions_by_date_range(customer):

    print("\n========================================")
    print("       TRANSACTION DATE RANGE")
    print("========================================")

    start_date_input = input(
        "\nEnter Start Date (YYYY-MM-DD): "
    ).strip()

    end_date_input = input(
        "Enter End Date (YYYY-MM-DD): "
    ).strip()

    # ========================================
    # VALIDATE START DATE
    # ========================================

    try:

        start_date = datetime.strptime(
            start_date_input,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        print("\nInvalid start date.")

        print(
            "Please use YYYY-MM-DD."
        )

        return

    # ========================================
    # VALIDATE END DATE
    # ========================================

    try:

        end_date = datetime.strptime(
            end_date_input,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        print("\nInvalid end date.")

        print(
            "Please use YYYY-MM-DD."
        )

        return

    # ========================================
    # CHECK DATE RANGE
    # ========================================

    if start_date > end_date:

        print(
            "\nStart date cannot be greater "
            "than end date."
        )

        return

    transactions = customer.get(
        "transactions",
        []
    )

    found = False

    print("\n========================================")
    print("       TRANSACTION RESULTS")
    print("========================================")

    for transaction in transactions:

        transaction_date = transaction.get(
            "date",
            ""
        )

        if not transaction_date:

            continue

        try:

            transaction_day = datetime.strptime(
                transaction_date[:10],
                "%Y-%m-%d"
            ).date()

        except ValueError:

            continue

        # ====================================
        # CHECK DATE RANGE
        # ====================================

        if start_date <= transaction_day <= end_date:

            found = True

            print(
                "\n----------------------------------------"
            )

            print(
                "Transaction ID :",
                transaction.get(
                    "transaction_id",
                    "Not available"
                )
            )

            print(
                "Type           :",
                transaction.get(
                    "type",
                    "Unknown"
                )
            )

            print(
                "Amount         : ₹",
                format(
                    transaction.get(
                        "amount",
                        0
                    ),
                    ".2f"
                )
            )

            print(
                "Status         :",
                transaction.get(
                    "status",
                    "SUCCESS"
                )
            )

            print(
                "Date & Time    :",
                transaction.get(
                    "date",
                    "Date not available"
                )
            )

    # ========================================
    # NO TRANSACTIONS
    # ========================================

    if not found:

        print(
            "\nNo transactions found "
            "within this date range."
        )

    print(
        "\n========================================"
    )

    input(
        "\nPress Enter to return..."
    )

#=======================
#sorting transactions
#=======================
def sort_transactions(customer):

    print("\n========================================")
    print("       SORT TRANSACTIONS")
    print("========================================")

    print("\n1. Newest to Oldest")
    print("2. Oldest to Newest")

    choice = input(
        "\nEnter your choice (1-2): "
    ).strip()

    transactions = customer.get(
        "transactions",
        []
    )

    if not transactions:

        print("\nNo transactions found.")

        input(
            "\nPress Enter to return..."
        )

        return

    # ========================================
    # SORT NEWEST TO OLDEST
    # ========================================

    if choice == "1":

        sorted_transactions = sorted(
            transactions,
            key=lambda transaction:
                transaction.get(
                    "date",
                    ""
                ),
            reverse=True
        )

        title = "NEWEST TO OLDEST"

    # ========================================
    # SORT OLDEST TO NEWEST
    # ========================================

    elif choice == "2":

        sorted_transactions = sorted(
            transactions,
            key=lambda transaction:
                transaction.get(
                    "date",
                    ""
                )
        )

        title = "OLDEST TO NEWEST"

    else:

        print("\nInvalid choice.")

        return

    # ========================================
    # DISPLAY
    # ========================================

    print("\n========================================")
    print(
        "       TRANSACTIONS -",
        title
    )
    print("========================================")

    for transaction in sorted_transactions:

        print("\n----------------------------------------")

        print(
            "Transaction ID :",
            transaction.get(
                "transaction_id",
                "Not available"
            )
        )

        print(
            "Type           :",
            transaction.get(
                "type",
                "Unknown"
            )
        )

        print(
            "Amount         : ₹",
            format(
                transaction.get(
                    "amount",
                    0
                ),
                ".2f"
            )
        )

        print(
            "Status         :",
            transaction.get(
                "status",
                "SUCCESS"
            )
        )

        print(
            "Date & Time    :",
            transaction.get(
                "date",
                "Date not available"
            )
        )

    print("\n========================================")

    input(
        "\nPress Enter to return..."
    )

#================================
# filter transactions_by_type and date
#============================ #

def filter_transactions_by_type_and_date(customer):

    print("\n========================================")
    print("   TRANSACTION TYPE + DATE FILTER")
    print("========================================")

    print("\n1. Deposit")
    print("2. Withdrawal")
    print("3. Transfer Sent")
    print("4. Transfer Received")
    print("5. All Transactions")

    choice = input(
        "\nEnter your choice (1-5): "
    ).strip()

    transaction_types = {

        "1": "Deposit",

        "2": "Withdrawal",

        "3": "Transfer Sent",

        "4": "Transfer Received"
    }

    # ========================================
    # SELECT TRANSACTION TYPE
    # ========================================

    if choice == "5":

        selected_type = None

    elif choice in transaction_types:

        selected_type = transaction_types[choice]

    else:

        print("\nInvalid choice.")

        return

    # ========================================
    # GET START DATE
    # ========================================

    start_date_input = input(
        "\nEnter Start Date (YYYY-MM-DD): "
    ).strip()

    # ========================================
    # GET END DATE
    # ========================================

    end_date_input = input(
        "Enter End Date (YYYY-MM-DD): "
    ).strip()

    # ========================================
    # VALIDATE START DATE
    # ========================================

    try:

        start_date = datetime.strptime(
            start_date_input,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        print(
            "\nInvalid start date."
        )

        print(
            "Please use YYYY-MM-DD."
        )

        return

    # ========================================
    # VALIDATE END DATE
    # ========================================

    try:

        end_date = datetime.strptime(
            end_date_input,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        print(
            "\nInvalid end date."
        )

        print(
            "Please use YYYY-MM-DD."
        )

        return

    # ========================================
    # CHECK DATE RANGE
    # ========================================

    if start_date > end_date:

        print(
            "\nStart date cannot be greater "
            "than end date."
        )

        return

    transactions = customer.get(
        "transactions",
        []
    )

    found = False

    # ========================================
    # DISPLAY HEADER
    # ========================================

    print("\n========================================")
    print("       FILTERED TRANSACTIONS")
    print("========================================")

    if selected_type is None:

        print(
            "Transaction Type : All Transactions"
        )

    else:

        print(
            "Transaction Type :",
            selected_type
        )

    print(
        "Start Date       :",
        start_date_input
    )

    print(
        "End Date         :",
        end_date_input
    )

    print("========================================")

    # ========================================
    # SEARCH TRANSACTIONS
    # ========================================

    for transaction in transactions:

        transaction_type = transaction.get(
            "type",
            ""
        )

        transaction_date = transaction.get(
            "date",
            ""
        )

        # ------------------------------------
        # Skip transaction without date
        # ------------------------------------

        if not transaction_date:

            continue

        # ------------------------------------
        # Convert transaction date
        # ------------------------------------

        try:

            transaction_day = datetime.strptime(
                transaction_date[:10],
                "%Y-%m-%d"
            ).date()

        except ValueError:

            continue

        # ====================================
        # TYPE CHECK
        # ====================================

        type_matches = (
            selected_type is None
            or transaction_type == selected_type
        )

        # ====================================
        # DATE CHECK
        # ====================================

        date_matches = (
            start_date
            <= transaction_day
            <= end_date
        )

        # ====================================
        # FINAL CHECK
        # ====================================

        if type_matches and date_matches:

            found = True

            print(
                "\n----------------------------------------"
            )

            print(
                "Transaction ID :",
                transaction.get(
                    "transaction_id",
                    "Not available"
                )
            )

            print(
                "Type           :",
                transaction_type
            )

            print(
                "Amount         : ₹",
                format(
                    transaction.get(
                        "amount",
                        0
                    ),
                    ".2f"
                )
            )

            print(
                "Status         :",
                transaction.get(
                    "status",
                    "SUCCESS"
                )
            )

            print(
                "Date & Time    :",
                transaction_date
            )

            # --------------------------------
            # TRANSFER DETAILS
            # --------------------------------

            if transaction_type in [
                "Transfer Sent",
                "Transfer Received"
            ]:

                print(
                    "Sender Name    :",
                    transaction.get(
                        "sender_name",
                        "Not available"
                    )
                )

                print(
                    "Sender Account :",
                    transaction.get(
                        "sender_account",
                        "Not available"
                    )
                )

                print(
                    "Receiver Name  :",
                    transaction.get(
                        "receiver_name",
                        "Not available"
                    )
                )

                print(
                    "Receiver Account:",
                    transaction.get(
                        "receiver_account",
                        "Not available"
                    )
                )

    # ========================================
    # NO RESULTS
    # ========================================

    if not found:

        print(
            "\nNo transactions found "
            "for the selected filter."
        )

    print(
        "\n========================================"
    )

    input(
        "\nPress Enter to return..."
    )

#====================================
# transaction summary
#==================================#
def customer_transaction_summary(customer):

    print("\n========================================")
    print("       TRANSACTION SUMMARY")
    print("========================================")

    transactions = customer.get(
        "transactions",
        []
    )

    total_deposits = 0
    total_withdrawals = 0
    total_sent = 0
    total_received = 0

    deposit_count = 0
    withdrawal_count = 0
    sent_count = 0
    received_count = 0

    # ========================================
    # PROCESS TRANSACTIONS
    # ========================================

    for transaction in transactions:

        transaction_type = transaction.get(
            "type",
            ""
        )

        amount = transaction.get(
            "amount",
            0
        )

        try:

            amount = float(amount)

        except (ValueError, TypeError):

            amount = 0

        # ------------------------------------
        # DEPOSIT
        # ------------------------------------

        if transaction_type == "Deposit":

            total_deposits += amount

            deposit_count += 1

        # ------------------------------------
        # WITHDRAWAL
        # ------------------------------------

        elif transaction_type == "Withdrawal":

            total_withdrawals += amount

            withdrawal_count += 1

        # ------------------------------------
        # TRANSFER SENT
        # ------------------------------------

        elif transaction_type == "Transfer Sent":

            total_sent += amount

            sent_count += 1

        # ------------------------------------
        # TRANSFER RECEIVED
        # ------------------------------------

        elif transaction_type == "Transfer Received":

            total_received += amount

            received_count += 1

    # ========================================
    # DISPLAY CUSTOMER
    # ========================================

    print(
        "Customer Name       :",
        customer.get(
            "name",
            "Not available"
        )
    )

    print(
        "Account Number      :",
        customer.get(
            "account_no",
            "Not available"
        )
    )

    print(
        "Account Status      :",
        customer.get(
            "status",
            "Active"
        )
    )

    print("\n----------------------------------------")

    # ========================================
    # TRANSACTION COUNTS
    # ========================================

    print(
        "Total Transactions  :",
        len(transactions)
    )

    print(
        "Deposit Count       :",
        deposit_count
    )

    print(
        "Withdrawal Count    :",
        withdrawal_count
    )

    print(
        "Transfer Sent Count :",
        sent_count
    )

    print(
        "Transfer Received   :",
        received_count
    )

    print("\n----------------------------------------")

    # ========================================
    # AMOUNT SUMMARY
    # ========================================

    print(
        "Total Deposits      : ₹",
        format(
            total_deposits,
            ".2f"
        )
    )

    print(
        "Total Withdrawals   : ₹",
        format(
            total_withdrawals,
            ".2f"
        )
    )

    print(
        "Total Sent          : ₹",
        format(
            total_sent,
            ".2f"
        )
    )

    print(
        "Total Received      : ₹",
        format(
            total_received,
            ".2f"
        )
    )

    print("\n----------------------------------------")

    # ========================================
    # CURRENT BALANCE
    # ========================================

    print(
        "Current Balance     : ₹",
        format(
            customer.get(
                "balance",
                0
            ),
            ".2f"
        )
    )

    print(
        "========================================"
    )

    input(
        "\nPress Enter to return..."
    )

#===========================
# export account statement
# ++++++++++++++++++++++++++#
def export_account_statement(customer):

    print("\n========================================")
    print("       EXPORT ACCOUNT STATEMENT")
    print("========================================")

    transactions = customer.get(
        "transactions",
        []
    )

    if not transactions:

        print("\nNo transactions available to export.")

        input(
            "\nPress Enter to return..."
        )

        return

    account_no = customer.get(
        "account_no",
        "unknown"
    )

    filename = (
        f"account_statement_{account_no}.csv"
    )

    try:

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            # ====================================
            # CSV HEADER
            # ====================================

            writer.writerow([
                "Transaction ID",
                "Date & Time",
                "Transaction Type",
                "Amount",
                "Status",
                "Sender Name",
                "Sender Account",
                "Receiver Name",
                "Receiver Account"
            ])

            # ====================================
            # TRANSACTIONS
            # ====================================

            for transaction in transactions:

                writer.writerow([

                    transaction.get(
                        "transaction_id",
                        "Not available"
                    ),

                    transaction.get(
                        "date",
                        "Not available"
                    ),

                    transaction.get(
                        "type",
                        "Unknown"
                    ),

                    transaction.get(
                        "amount",
                        0
                    ),

                    transaction.get(
                        "status",
                        "SUCCESS"
                    ),

                    transaction.get(
                        "sender_name",
                        "Not available"
                    ),

                    transaction.get(
                        "sender_account",
                        "Not available"
                    ),

                    transaction.get(
                        "receiver_name",
                        "Not available"
                    ),

                    transaction.get(
                        "receiver_account",
                        "Not available"
                    )
                ])

        print("\n========================================")
        print("       EXPORT SUCCESSFUL")
        print("========================================")

        print(
            "File Name:",
            filename
        )

        print(
            "Transactions Exported:",
            len(transactions)
        )

        print("========================================")

    except Exception as error:

        print("\n========================================")
        print("          EXPORT FAILED")
        print("========================================")

        print(
            "Error:",
            error
        )

        print("========================================")

    input(
        "\nPress Enter to return..."
    )
#=========================
#CUSTOMER DASHBOARD 
#=========================
def customer_dashboard(customer):

    while True:

        print("\n===============================")
        print("CUSTOMER DASHBOARD")
        print("===============================")

        print("Welcome,", customer["name"])

        print("\n 1.Check Balance")
        print("   2.Deposit Money")
        print("   3.Withdraw Money ")
        print("   4.Transfer Money ")
        print("   5.Transaction History ")
        print("   6.Change Password")
        print("   7.Account Statement")
        print("   8.Customer Profile")
        print("   9.Filter Transaction By Date")
        print("   10.Filter Transaction By Date Range ")
        print("   11.Sort Transactions ")
        print("   12.Filter transaction by type and date")
        print("   13.Transaction Summary")
        print("   14.Export Account Statement")
        print("   15.Add notification")
        print("   16.View notification")
        print("   17.Logout ")

        print("")
        choice =input("Enter your Choice(1-17): ")

        if choice == "1":

            print("\n------Account Balance-----")
            print("")
            print("Account Number:", customer["account_no"])
            print("Account Holder:",customer["name"])
            print("Current Balance:₹", format(customer["balance"],".2f"))

            
        elif choice == "2":
            deposit_money(customer)
        elif choice == "3":
            withdraw_money(customer)
        elif choice == "4" :
            transfer_money(customer)
        elif choice == "5":
            transaction_history(customer)
        elif choice == "6":
            change_password(customer)
        elif choice == "7":
            account_statement(customer)
        elif choice == "8":
            customer_profile(customer)
        elif choice == "9":
            filter_transactions_by_date(customer)
        elif choice == "10":
            filter_transactions_by_date_range(customer)
        elif choice == "11":
            sort_transactions(customer)
        elif choice == "12":
            filter_transactions_by_type_and_date(customer)
        elif choice == "13":
            customer_transaction_summary(customer)
        elif choice == "14":
            export_account_statement(customer)
        elif choice == "15":
            message = input("\nEnter notification message: ").strip()
            if not message:
                print("\nNotification message cannot be empty.")  
            else:
                add_notification(customer,message)  
        elif choice == "16":
            view_notifications(customer)
        elif choice == "17":
            print("\nLogout from the system.")
            break

        else:
            print("Invalid choice! Please try again.")


#=========================
#MAIN MENU
#=========================

while True:

    print("\n MAIN MENU")

    print("1. Register")
    print("2. Login")
    print("3. Admin Login")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        register()
    elif choice == '2':
        logged_in_customer = login()

        if logged_in_customer is not None:
            customer_dashboard(logged_in_customer)
    elif choice == "3":
        admin_logged_in = admin_login()

        if admin_logged_in:
            admin_dashboard()
            
    elif choice == '4':
        print("\n Thankyou for using smart banking system!")
        break
    else:
        print("\nInvalid choice ! Please try again.")
    