import random
import time

import os

import re
from datetime import datetime

import csv

import json
from datetime import datetime

from getpass import getpass
from decimal import Decimal, InvalidOperation


import psycopg2
import hashlib

#DATABASE CONNECTION

def get_db_connection():

    try:

        connection = psycopg2.connect(
            host="localhost",
            database="smart_banking",
            user="postgres",
            password="481141",
            port="5432"
        )

        return connection

    except psycopg2.Error as error:

        print("\nDatabase connection error:")
        print(error)

        return None


    
# ========================================
# MONEY CONVERSION
# ========================================

def to_decimal(value):

    try:

        return Decimal(
            str(value)
        ).quantize(
            Decimal("0.01")
        )

    except (
        InvalidOperation,
        ValueError,
        TypeError
    ):

        return Decimal("0.00")


 # ========================================
# CONVERT DECIMAL VALUES FOR JSON
# ========================================

def decimal_to_float(value):

    if isinstance(
        value,
        Decimal
    ):

        return float(value)

    return value



import hashlib

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

 

def verify_password(password, stored_password):
    return hash_password(password) == stored_password

FILE_NAME = "data/customers.json"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("admin123")


print("==============================================")
print(" SMART BANKING MANAGEMENT SYSTEM ")
print("==============================================")

def load_admin_logs():

    try:

        with open(
            "admin_logs.json",
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
#==============================
#BACKUP DATA
#=============================
def backup_data():

    import os
    import csv

    print("\n========================================")
    print("             BACKUP DATA")
    print("========================================")

    backup_folder = "backup"

    os.makedirs(
        backup_folder,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    created = []

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to PostgreSQL."
        )

        input(
            "\nPress Enter to return..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # BACKUP CUSTOMERS
        # ========================================

        cursor.execute(
            """
            SELECT
                customer_id,
                account_no,
                name,
                password_hash,
                mobile,
                mobile_verified,
                email,
                email_type,
                aadhaar_hash,
                aadhaar_masked,
                balance,
                status,
                created_at
            FROM customers
            ORDER BY customer_id
            """
        )

        customers_data = cursor.fetchall()

        customer_path = os.path.join(
            backup_folder,
            f"customers_{timestamp}.csv"
        )

        with open(
            customer_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "customer_id",
                "account_no",
                "name",
                "password_hash",
                "mobile",
                "mobile_verified",
                "email",
                "email_type",
                "aadhaar_hash",
                "aadhaar_masked",
                "balance",
                "status",
                "created_at"
            ])

            writer.writerows(
                customers_data
            )

        created.append(
            customer_path
        )

        print(
            "\nCustomer data backup created:"
        )

        print(
            customer_path
        )

        # ========================================
        # BACKUP TRANSACTIONS
        # ========================================

        cursor.execute(
            """
            SELECT
                transaction_id,
                customer_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                date,
                status
            FROM transactions
            ORDER BY date
            """
        )

        transactions_data = cursor.fetchall()

        transaction_path = os.path.join(
            backup_folder,
            f"transactions_{timestamp}.csv"
        )

        with open(
            transaction_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "transaction_id",
                "customer_id",
                "transaction_type",
                "amount",
                "sender_account",
                "receiver_account",
                "sender_name",
                "receiver_name",
                "date",
                "status"
            ])

            writer.writerows(
                transactions_data
            )

        created.append(
            transaction_path
        )

        print(
            "\nTransaction data backup created:"
        )

        print(
            transaction_path
        )

        # ========================================
        # BACKUP NOTIFICATIONS
        # ========================================

        cursor.execute(
            """
            SELECT
                notification_id,
                customer_id,
                message,
                transaction_id,
                is_read,
                created_at
            FROM notifications
            ORDER BY notification_id
            """
        )

        notifications_data = cursor.fetchall()

        notification_path = os.path.join(
            backup_folder,
            f"notifications_{timestamp}.csv"
        )

        with open(
            notification_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "notification_id",
                "customer_id",
                "message",
                "transaction_id",
                "is_read",
                "created_at"
            ])

            writer.writerows(
                notifications_data
            )

        created.append(
            notification_path
        )

        print(
            "\nNotification backup created:"
        )

        print(
            notification_path
        )

        # ========================================
        # BACKUP ADMIN ACTIVITY
        # ========================================

        cursor.execute(
            """
            SELECT
                activity_id,
                action,
                details,
                date
            FROM admin_activity
            ORDER BY activity_id
            """
        )

        admin_activity_data = cursor.fetchall()

        admin_activity_path = os.path.join(
            backup_folder,
            f"admin_activity_{timestamp}.csv"
        )

        with open(
            admin_activity_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "activity_id",
                "action",
                "details",
                "date"
            ])

            writer.writerows(
                admin_activity_data
            )

        created.append(
            admin_activity_path
        )

        print(
            "\nAdmin activity backup created:"
        )

        print(
            admin_activity_path
        )

        # ========================================
        # BACKUP RESULT
        # ========================================

        if created:

            print(
                "\n========================================"
            )

            print(
                "       BACKUP CREATED SUCCESSFULLY"
            )

            print(
                "========================================"
            )

            print(
                f"Total backup files created: {len(created)}"
            )

        else:

            print(
                "\n========================================"
            )

            print(
                "          BACKUP FAILED"
            )

            print(
                "========================================"
            )

    except psycopg2.Error as error:

        print(
            "\nDatabase error during backup."
        )

        print(
            "Error:",
            error
        )

    except Exception as error:

        print(
            "\nUnexpected error during backup."
        )

        print(
            "Error:",
            error
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()

    input(
        "\nPress Enter to return..."
    )



#=============================
#SYSTEM HEALTH CHECK
#==============================
def system_health_check():

    print("\n========================================")
    print("         SYSTEM HEALTH CHECK")
    print("========================================")

    connection = get_db_connection()

    if connection is None:

        print("\nDatabase Connection : ERROR")
        print("Unable to connect to PostgreSQL.")

        print("\n========================================")

        input(
            "\nPress Enter to return..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # DATABASE CONNECTION
        # ========================================

        print(
            "\nDatabase Connection : OK"
        )

        # ========================================
        # CUSTOMERS TABLE
        # ========================================

        try:

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM customers
                """
            )

            customer_count = cursor.fetchone()[0]

            print(
                "\nCustomers Data      : OK"
            )

            print(
                "Customer Count      :",
                customer_count
            )

        except psycopg2.Error as error:

            print(
                "\nCustomers Data      : ERROR"
            )

            print(
                "Error:",
                error
            )

        # ========================================
        # TRANSACTIONS TABLE
        # ========================================

        try:

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM transactions
                """
            )

            transaction_count = cursor.fetchone()[0]

            print(
                "\nTransactions Data   : OK"
            )

            print(
                "Transaction Count   :",
                transaction_count
            )

        except psycopg2.Error as error:

            print(
                "\nTransactions Data   : ERROR"
            )

            print(
                "Error:",
                error
            )

        # ========================================
        # NOTIFICATIONS TABLE
        # ========================================

        try:

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM notifications
                """
            )

            notification_count = cursor.fetchone()[0]

            print(
                "\nNotifications Data  : OK"
            )

            print(
                "Notification Count  :",
                notification_count
            )

        except psycopg2.Error as error:

            print(
                "\nNotifications Data  : ERROR"
            )

            print(
                "Error:",
                error
            )

        # ========================================
        # ADMIN ACTIVITY TABLE
        # ========================================

        try:

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM admin_activity
                """
            )

            activity_count = cursor.fetchone()[0]

            print(
                "\nAdmin Activity Data : OK"
            )

            print(
                "Activity Log Count  :",
                activity_count
            )

        except psycopg2.Error as error:

            print(
                "\nAdmin Activity Data : ERROR"
            )

            print(
                "Error:",
                error
            )

        print(
            "\n========================================"
        )

    except psycopg2.Error as error:

        print(
            "\nDatabase Health     : ERROR"
        )

        print(
            "Error:",
            error
        )

        print(
            "\n========================================"
        )

    except Exception as error:

        print(
            "\nSystem Health       : ERROR"
        )

        print(
            "Error:",
            error
        )

        print(
            "\n========================================"
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()

    input(
        "\nPress Enter to return..."
    )

    
# ========================================
# LOAD CUSTOMERS FROM FILE
# ========================================

def load_customers():

    import os
    import json

    # ========================================
    # FILE DOES NOT EXIST
    # ========================================

    if not os.path.exists(FILE_NAME):

        return []

    # ========================================
    # READ CUSTOMER DATA
    # ========================================

    try:

        with open(
            FILE_NAME,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError as error:

        print("\n========================================")
        print("       CUSTOMER DATA ERROR")
        print("========================================")

        print(
            "The customer data file contains"
        )

        print(
            "invalid or corrupted JSON."
        )

        print(
            "\nFile:",
            FILE_NAME
        )

        print(
            "\nError:",
            error
        )

        print(
            "\nThe existing customer data has NOT"
        )

        print(
            "been replaced."
        )

        print("========================================")

        return []

    except OSError as error:

        print("\n========================================")
        print("       CUSTOMER DATA ERROR")
        print("========================================")

        print(
            "Unable to read the customer data file."
        )

        print(
            "\nFile:",
            FILE_NAME
        )

        print(
            "\nError:",
            error
        )

        print("========================================")

        return []

    # ========================================
    # VALIDATE TOP-LEVEL DATA TYPE
    # ========================================

    if not isinstance(data, list):

        print("\n========================================")
        print("       INVALID CUSTOMER DATA")
        print("========================================")

        print(
            "customers.json must contain a JSON list."
        )

        print(
            "\nExample:"
        )

        print(
            "["
        )

        print(
            '    {"name": "Customer"}'
        )

        print(
            "]"
        )

        print("========================================")

        return []
    # ========================================
    # CONVERT CUSTOMER MONEY VALUES
    # ========================================

    for customer in data:

        # ========================================
        # CUSTOMER BALANCE
        # ========================================

        if "balance" in customer:

            customer["balance"] = to_decimal(
                customer["balance"]
            )

        # ========================================
        # TRANSACTION AMOUNTS
        # ========================================

        transactions = customer.get(
            "transactions",
            []
        )

        for transaction in transactions:

            if "amount" in transaction:

                transaction["amount"] = to_decimal(
                    transaction["amount"]
                )


    # ========================================
    # RETURN VALID DATA
    # ========================================

    return data


# ========================================
# VALID TRANSACTION TYPES
# ========================================

VALID_TRANSACTION_TYPES = {
    "Initial Deposit",
    "Deposit",
    "Withdrawal",
    "Transfer Sent",
    "Transfer Received"
}

# ========================================
# REPAIR DUPLICATE TRANSACTION IDs
# ========================================

def repair_duplicate_transaction_ids():

    seen_transaction_ids = set()
    repaired_count = 0

    for customer in customers:

        account_no = customer.get(
            "account_no",
            "UNKNOWN"
        )

        transactions = customer.get(
            "transactions",
            []
        )

        if not isinstance(
            transactions,
            list
        ):
            continue

        for transaction in transactions:

            if not isinstance(
                transaction,
                dict
            ):
                continue

            transaction_id = transaction.get(
                "transaction_id",
                ""
            )

            # Ignore empty IDs.
            # Missing IDs will be handled separately.
            if not transaction_id:
                continue

            # ========================================
            # NEW TRANSACTION ID
            # ========================================

            if transaction_id in seen_transaction_ids:

                old_transaction_id = transaction_id

                new_transaction_id = (
                    generate_transaction_id()
                )

                # Make absolutely sure
                # the new ID is unique.
                while new_transaction_id in seen_transaction_ids:

                    new_transaction_id = (
                        generate_transaction_id()
                    )

                transaction[
                    "transaction_id"
                ] = new_transaction_id

                seen_transaction_ids.add(
                    new_transaction_id
                )

                repaired_count += 1

                print("\n========================================")
                print("DUPLICATE TRANSACTION ID REPAIRED")
                print("========================================")

                print(
                    "Account:",
                    account_no
                )

                print(
                    "Old Transaction ID:",
                    old_transaction_id
                )

                print(
                    "New Transaction ID:",
                    new_transaction_id
                )

                print("========================================")

            else:

                seen_transaction_ids.add(
                    transaction_id
                )

    # ========================================
    # SAVE CHANGES
    # ========================================

    if repaired_count > 0:

        save_customers()

        print("\n========================================")
        print("DUPLICATE ID REPAIR COMPLETE")
        print("========================================")

        print(
            "Transactions repaired:",
            repaired_count
        )

        print("========================================")

    else:

        print(
            "\nNo duplicate transaction IDs found."
        )

    return repaired_count

# ========================================
# REPAIR MISSING TRANSACTION IDs
# ========================================

def repair_missing_transaction_ids():

    repaired_count = 0

    # ========================================
    # COLLECT ALL EXISTING IDs
    # ========================================

    existing_ids = set()

    for customer in customers:

        transactions = customer.get(
            "transactions",
            []
        )

        if not isinstance(
            transactions,
            list
        ):
            continue

        for transaction in transactions:

            if not isinstance(
                transaction,
                dict
            ):
                continue

            transaction_id = transaction.get(
                "transaction_id",
                ""
            )

            if transaction_id:

                existing_ids.add(
                    transaction_id
                )

    # ========================================
    # FIND MISSING IDs
    # ========================================

    for customer in customers:

        account_no = customer.get(
            "account_no",
            "UNKNOWN"
        )

        transactions = customer.get(
            "transactions",
            []
        )

        if not isinstance(
            transactions,
            list
        ):
            continue

        for transaction_index, transaction in enumerate(
            transactions,
            start=1
        ):

            if not isinstance(
                transaction,
                dict
            ):
                continue

            transaction_id = transaction.get(
                "transaction_id",
                ""
            )

            # ========================================
            # MISSING TRANSACTION ID
            # ========================================

            if not transaction_id:

                while True:

                    current_date = datetime.now().strftime(
                        "%Y%m%d"
                    )

                    # Use current timestamp to create
                    # a unique transaction ID
                    timestamp_part = datetime.now().strftime(
                        "%H%M%S%f"
                    )

                    new_transaction_id = (
                        f"TXN-{current_date}-{timestamp_part}"
                    )

                    if new_transaction_id not in existing_ids:

                        break

                # ========================================
                # SAVE NEW ID
                # ========================================

                transaction[
                    "transaction_id"
                ] = new_transaction_id

                existing_ids.add(
                    new_transaction_id
                )

                repaired_count += 1

                print("\n========================================")
                print("MISSING TRANSACTION ID REPAIRED")
                print("========================================")

                print(
                    "Account:",
                    account_no
                )

                print(
                    "Transaction:",
                    transaction_index
                )

                print(
                    "Transaction Type:",
                    transaction.get(
                        "type",
                        "UNKNOWN"
                    )
                )

                print(
                    "Amount: ₹",
                    transaction.get(
                        "amount",
                        0
                    )
                )

                print(
                    "New Transaction ID:",
                    new_transaction_id
                )

                print("========================================")

    # ========================================
    # SAVE
    # ========================================

    if repaired_count > 0:

        save_customers()

        print("\n========================================")
        print("MISSING ID REPAIR COMPLETE")
        print("========================================")

        print(
            "Transactions repaired:",
            repaired_count
        )

        print("========================================")

    else:

        print(
            "\nNo missing transaction IDs found."
        )

    return repaired_count


# ========================================
# TRANSACTION DATA CONSISTENCY CHECK
# ========================================

def check_transaction_consistency():

    print("\n========================================")
    print("     TRANSACTION DATA CONSISTENCY")
    print("========================================")

    total_customers = 0
    total_transactions = 0
    total_errors = 0

    # Store transaction IDs and their locations
    transaction_id_records = {}

    # ========================================
    # VALID TRANSACTION TYPES
    # ========================================

    valid_transaction_types = {
        "Initial Deposit",
        "Deposit",
        "Withdrawal",
        "Transfer Sent",
        "Transfer Received"
    }

    # ========================================
    # CHECK ALL CUSTOMERS
    # ========================================

    for customer in customers:

        total_customers += 1

        account_no = customer.get(
            "account_no",
            "UNKNOWN"
        )

        customer_name = customer.get(
            "name",
            "UNKNOWN"
        )

        transactions = customer.get(
            "transactions",
            []
        )

        # ========================================
        # CHECK TRANSACTION LIST
        # ========================================

        if not isinstance(
            transactions,
            list
        ):

            print("\nERROR")
            print(
                f"Account {account_no}"
            )

            print(
                f"Customer: {customer_name}"
            )

            print(
                "Problem: Transactions must be a list."
            )

            total_errors += 1

            continue

        # ========================================
        # CHECK EACH TRANSACTION
        # ========================================

        for transaction_index, transaction in enumerate(
            transactions,
            start=1
        ):

            total_transactions += 1

            location = (
                f"Account {account_no} | "
                f"Transaction {transaction_index}"
            )

            # ========================================
            # TRANSACTION MUST BE DICTIONARY
            # ========================================

            if not isinstance(
                transaction,
                dict
            ):

                print("\nERROR")
                print(location)

                print(
                    "Transaction must be a dictionary."
                )

                total_errors += 1

                continue

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

                    print("\nERROR")
                    print(location)

                    print(
                        f"Missing field: {field}"
                    )

                    total_errors += 1

            # ========================================
            # TRANSACTION ID
            # ========================================

            transaction_id = transaction.get(
                "transaction_id",
                ""
            )

            if not transaction_id:

                print("\nERROR")
                print(location)

                print(
                    "Transaction ID is empty."
                )

                total_errors += 1

            else:

                # Save transaction ID information
                if transaction_id not in transaction_id_records:

                    transaction_id_records[
                        transaction_id
                    ] = []

                transaction_id_records[
                    transaction_id
                ].append(
                    {
                        "account_no": account_no,
                        "transaction_index": transaction_index,
                        "type": transaction.get(
                            "type",
                            ""
                        )
                    }
                )

            # ========================================
            # TRANSACTION TYPE
            # ========================================

            transaction_type = transaction.get(
                "type",
                ""
            )

            if transaction_type not in valid_transaction_types:

                print("\nERROR")
                print(location)

                print(
                    "Invalid transaction type:",
                    transaction_type
                )

                total_errors += 1

            # ========================================
            # TRANSACTION AMOUNT
            # ========================================

            if "amount" in transaction:

                try:

                    amount = to_decimal(
                        transaction.get(
                            "amount"
                        )
                    )

                    if amount <= Decimal("0.00"):

                        print("\nERROR")
                        print(location)

                        print(
                            "Transaction amount "
                            "must be greater than zero."
                        )

                        total_errors += 1

                except Exception:

                    print("\nERROR")
                    print(location)

                    print(
                        "Invalid transaction amount:",
                        transaction.get(
                            "amount"
                        )
                    )

                    total_errors += 1

            # ========================================
            # TRANSACTION DATE
            # ========================================

            if "date" in transaction:

                transaction_date = transaction.get(
                    "date"
                )

                if not transaction_date:

                    print("\nERROR")
                    print(location)

                    print(
                        "Transaction date is empty."
                    )

                    total_errors += 1

                else:

                    try:

                        datetime.strptime(
                            transaction_date,
                            "%Y-%m-%d %H:%M:%S"
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        print("\nERROR")
                        print(location)

                        print(
                            "Invalid transaction date:",
                            transaction_date
                        )

                        total_errors += 1

    # ========================================
    # CHECK DUPLICATE TRANSACTION IDs
    # ========================================

    for transaction_id, records in (
        transaction_id_records.items()
    ):

        # A transaction ID appearing once is normal
        if len(records) <= 1:

            continue

        transaction_types = {
            record["type"]
            for record in records
        }

        account_numbers = {
            str(record["account_no"])
            for record in records
        }

        transfer_types = {
            "Transfer Sent",
            "Transfer Received"
        }

        # ========================================
        # VALID TRANSFER PAIR
        # ========================================

        if (
            transaction_types == transfer_types
            and
            len(records) == 2
            and
            len(account_numbers) == 2
        ):

            # Same transaction ID is expected
            # for sender and receiver.
            continue

        # ========================================
        # REAL DUPLICATE TRANSACTION ID
        # ========================================

        print("\n========================================")
        print("DUPLICATE TRANSACTION ID")
        print("========================================")

        print(
            "Transaction ID:",
            transaction_id
        )

        print("Found in:")

        for record in records:

            print(
                f" - Account {record['account_no']} "
                f"| Transaction "
                f"{record['transaction_index']} "
                f"| Type: {record['type']}"
            )

        total_errors += 1

    # ========================================
    # FINAL RESULT
    # ========================================

    print("\n========================================")
    print("       CONSISTENCY CHECK COMPLETE")
    print("========================================")

    print(
        "Total Customers    :",
        total_customers
    )

    print(
        "Total Transactions :",
        total_transactions
    )

    print(
        "Total Errors       :",
        total_errors
    )

    if total_errors == 0:

        print(
            "\nSTATUS: ALL TRANSACTIONS ARE CONSISTENT."
        )

    else:

        print(
            "\nSTATUS: TRANSACTION DATA NEEDS ATTENTION."
        )

    print("========================================")

    return total_errors == 0




def prepare_for_json(data):

    # Decimal value
    if isinstance(data, Decimal):

        return float(data)

    # Dictionary
    if isinstance(data, dict):

        return {
            key: prepare_for_json(value)
            for key, value in data.items()
        }

    # List
    if isinstance(data, list):

        return [
            prepare_for_json(item)
            for item in data
        ]

    # Other values
    return data

# ========================================
# SAVE CUSTOMERS SAFELY
# ========================================

def save_customers():

    import os
    import json
    import tempfile

    try:

        # ========================================
        # ENSURE DATA FOLDER EXISTS
        # ========================================

        data_folder = os.path.dirname(FILE_NAME)

        if data_folder:

            os.makedirs(
                data_folder,
                exist_ok=True
            )

        # ========================================
        # CREATE TEMPORARY FILE
        # ========================================

        temp_file = None

        try:

            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                delete=False,
                dir=data_folder if data_folder else None,
                prefix="customers_",
                suffix=".tmp"
            ) as file:

                temp_file = file.name

                json.dump(
                    prepare_for_json(customers),
                    file,
                    indent=4,
                    ensure_ascii=False
                )

                file.flush()

                os.fsync(
                    file.fileno()
                )

            # ========================================
            # VERIFY TEMPORARY JSON
            # ========================================

            with open(
                temp_file,
                "r",
                encoding="utf-8"
            ) as file:

                json.load(file)

            # ========================================
            # REPLACE ORIGINAL FILE
            # ========================================

            os.replace(
                temp_file,
                FILE_NAME
            )

            temp_file = None

        finally:

            # ========================================
            # REMOVE TEMP FILE IF SOMETHING FAILED
            # ========================================

            if (
                temp_file
                and os.path.exists(temp_file)
            ):

                os.remove(
                    temp_file
                )

    except (
        OSError,
        TypeError,
        ValueError,
        json.JSONDecodeError
    ) as error:

        print(
            "\n========================================"
        )

        print(
            "          DATA SAVE FAILED"
        )

        print(
            "========================================"
        )

        print(
            "Unable to save customer data."
        )

        print(
            "Error:",
            error
        )

        print(
            "========================================"
        )

        return False

    return True

customers = load_customers()

#=========================
#GENERATE ACCOUNT NUMBER
#=========================
def generate_account_number():

    connection = get_db_connection()

    if connection is None:
        return None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COALESCE(MAX(account_no), 100000)
            FROM customers
            """
        )

        last_account_no = cursor.fetchone()[0]

        return last_account_no + 1

    except psycopg2.Error as error:

        print("\nUnable to generate account number.")
        print("Database Error:", error)

        return None

    finally:
        cursor.close()
        connection.close()

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



 
# ========================================
# CUSTOMER REGISTRATION
# ========================================

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

        password = getpass(
            "Enter your password: "
        )

        if len(password) < 4:

            print(
                "\nPassword must contain at least 4 characters."
            )

            continue

        break

    # ========================================
    # MOBILE NUMBER
    # ========================================

    while True:

        mobile = input(
            "Enter Mobile Number: "
        ).strip()

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

        if mobile[0] == "0":

            print(
                "\nMobile number cannot start with 0."
            )

            continue

        if mobile[0] not in "6789":

            print(
                "\nInvalid mobile number."
            )

            print(
                "Mobile number must start with 6, 7, 8 or 9."
            )

            continue

        # ========================================
        # DUPLICATE MOBILE CHECK
        # ========================================

        mobile_exists = False

        for existing_customer in customers:

            if existing_customer.get(
                "mobile"
            ) == mobile:

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

    verification_customer = {

        "mobile": mobile,

        "mobile_verified": False

    }

    mobile_verified = verify_mobile_otp(
        verification_customer,
        save_changes=False
    )

    if not mobile_verified:

        print(
            "\n========================================"
        )

        print(
            "       REGISTRATION CANCELLED"
        )

        print(
            "========================================"
        )

        print(
            "Mobile number verification failed."
        )

        print(
            "Customer registration cannot continue."
        )

        print(
            "========================================"
        )

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

        # ========================================
        # PERSONAL EMAIL
        # ========================================

        if email_type == "Personal":

            if not email.endswith("@gmail.com"):

                print(
                    "\nPersonal email must end with @gmail.com."
                )

                continue

        # ========================================
        # COMPANY EMAIL
        # ========================================

        elif email_type == "Company":

            if email.endswith("@gmail.com"):

                print(
                    "\nFor a company account, "
                    "please use the company email domain."
                )

                continue

        # ========================================
        # DUPLICATE EMAIL CHECK
        # ========================================

        email_exists = False

        for existing_customer in customers:

            existing_email = existing_customer.get(
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

            balance = Decimal(
                input(
                    "Enter Initial Deposit: ₹"
                ).strip()
            ).quantize(
                Decimal("0.01")
            )

            if balance <= Decimal("0.00"):

                print(
                    "\nInitial deposit must be greater than zero."
                )

                continue

            break

        except (
            InvalidOperation,
            ValueError
        ):

            print(
                "\nInvalid input!"
            )

            print(
                "Please enter a valid amount."
            )

    # ========================================
    # GENERATE ACCOUNT NUMBER
    # ========================================

    account_no = generate_account_number()

    if account_no is None:

        print(
            "\nUnable to generate account number."
        )

        return

    # ========================================
    # GENERATE INITIAL TRANSACTION ID
    # ========================================

    transaction_id = generate_transaction_id()

    if transaction_id is None:

        print(
            "\nUnable to generate transaction ID."
        )

        return

    # ========================================
    # HASH PASSWORD
    # ========================================

    password_hash = hash_password(
        password
    )

    # ========================================
    # HASH AADHAAR
    # ========================================

    aadhaar_hash = hashlib.sha256(
        aadhaar.encode()
    ).hexdigest()

    # ========================================
    # CREATE CUSTOMER DICTIONARY
    # ========================================

    customer = {

        "account_no": account_no,

        "name": name,

        "password": password_hash,

        "mobile": mobile,

        "mobile_verified": mobile_verified,

        "email": email,

        "email_type": email_type,

        "aadhaar": masked_aadhaar,

        "aadhaar_hash": aadhaar_hash,

        "balance": balance,

        "status": "Active",

        "transactions": []

    }

    # ========================================
    # CREATE INITIAL TRANSACTION
    # ========================================

    transaction_date = datetime.now()

    transaction = {

        "transaction_id": transaction_id,

        "type": "Initial Deposit",

        "amount": balance,

        "date": transaction_date.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "balance_after": balance

    }

    customer["transactions"].append(
        transaction
    )

    # ========================================
    # CONNECT TO POSTGRESQL
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print(
            "\nRegistration could not be saved."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # INSERT CUSTOMER
        # ========================================

        cursor.execute(
            """
            INSERT INTO customers
            (
                account_no,
                name,
                password_hash,
                mobile,
                mobile_verified,
                email,
                email_type,
                aadhaar_hash,
                aadhaar_masked,
                balance,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            RETURNING customer_id
            """,
            (
                account_no,
                name,
                password_hash,
                mobile,
                mobile_verified,
                email,
                email_type,
                aadhaar_hash,
                masked_aadhaar,
                balance,
                "Active"
            )
        )

        customer_id = cursor.fetchone()[0]

        # ========================================
        # INSERT INITIAL TRANSACTION
        # ========================================

        cursor.execute(
            """
            INSERT INTO transactions
            (
                transaction_id,
                customer_id,
                transaction_type,
                amount,
                date,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                transaction_id,
                customer_id,
                "Initial Deposit",
                balance,
                transaction_date,
                "SUCCESS"
            )
        )

        # ========================================
        # COMMIT
        # ========================================

        connection.commit()

        # ========================================
        # KEEP CUSTOMER IN MEMORY
        # ========================================

        customer["customer_id"] = customer_id

        customers.append(
            customer
        )

        print(
            "\nCustomer registered successfully "
            "in PostgreSQL."
        )

    except psycopg2.Error as error:

        connection.rollback()

        print(
            "\nRegistration could not be saved."
        )

        print(
            "Database Error:",
            error
        )

        return

    finally:

        if cursor is not None:

            cursor.close()

        connection.close()

    # ========================================
    # REGISTRATION SUCCESS
    # ========================================

    print(
        "\n========================================"
    )

    print(
        "       REGISTRATION SUCCESSFUL"
    )

    print(
        "========================================"
    )

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
        "Transaction ID  :",
        transaction_id
    )

    print(
        "Account Status  :",
        "Active"
    )

    print(
        "========================================"
    )

    print(
        "You can now login using your account number."
    )

    print(
        "========================================"
    )
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
# ========================================
# CUSTOMER LOGIN
# ========================================
def login():

    global customers

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
                    input(
                        "Enter Account Number: "
                    ).strip()
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

            # ====================================
            # CONNECT TO POSTGRESQL
            # ====================================

            connection = get_db_connection()

            if connection is None:

                print(
                    "\nUnable to connect to database."
                )

                continue

            cursor = None

            try:

                cursor = connection.cursor()

                # ====================================
                # FIND CUSTOMER IN POSTGRESQL
                # ====================================

                cursor.execute(
                    """
                    SELECT
                        customer_id,
                        account_no,
                        name,
                        password_hash,
                        mobile,
                        mobile_verified,
                        email,
                        email_type,
                        aadhaar_hash,
                        aadhaar_masked,
                        balance,
                        status,
                        created_at
                    FROM customers
                    WHERE account_no = %s
                    """,
                    (
                        account_no,
                    )
                )

                row = cursor.fetchone()

                # ------------------------------------
                # ACCOUNT NOT FOUND
                # ------------------------------------

                if row is None:

                    print(
                        "\nInvalid Account Number."
                    )

                    continue

                # ====================================
                # CONVERT DATABASE ROW TO CUSTOMER
                # DICTIONARY
                # ====================================

                found_customer = {

                    "customer_id": row[0],

                    "account_no": row[1],

                    "name": row[2],

                    "password": row[3],

                    "mobile": row[4],

                    "mobile_verified": row[5],

                    "email": row[6],

                    "email_type": row[7],

                    "aadhaar_hash": row[8],

                    "aadhaar": row[9],

                    "balance": row[10],

                    "status": row[11],

                    "created_at": row[12],

                    "transactions": []

                }

                # ====================================
                # ACCOUNT STATUS CHECK
                # ====================================

                account_status = found_customer.get(
                    "status",
                    "Active"
                )

                print(
                    "\nAccount Status:",
                    account_status
                )

                # ------------------------------------
                # CLOSED ACCOUNT
                # ------------------------------------

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

                # ------------------------------------
                # INACTIVE ACCOUNT
                # ------------------------------------

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
                        "Your account is currently inactive."
                    )

                    print(
                        "Please contact the bank administrator."
                    )

                    print(
                        "========================================"
                    )

                    continue

                # ====================================
                # PASSWORD VERIFICATION
                # ====================================

                stored_password = found_customer.get(
                    "password",
                    ""
                )

                max_attempts = 3

                password_verified = False

                # ====================================
                # PASSWORD ATTEMPTS
                # ====================================

                for attempt in range(
                    1,
                    max_attempts + 1
                ):

                    if attempt == 1:

                        entered_password = password

                    else:

                        print(
                            f"\nPassword Attempt "
                            f"{attempt} of {max_attempts}"
                        )

                        entered_password = getpass(
                            "Enter Password: "
                        )

                    # --------------------------------
                    # HASHED PASSWORD
                    # --------------------------------

                    if len(stored_password) == 64:

                        entered_password_hash = (
                            hash_password(
                                entered_password
                            )
                        )

                        if (
                            entered_password_hash
                            == stored_password
                        ):

                            password_verified = True

                            break

                    # --------------------------------
                    # WRONG PASSWORD
                    # --------------------------------

                    remaining_attempts = (
                        max_attempts - attempt
                    )

                    if remaining_attempts > 0:

                        print(
                            "\nIncorrect Password."
                        )

                        print(
                            "Remaining attempts:",
                            remaining_attempts
                        )

                    else:

                        print(
                            "\n========================================"
                        )

                        print(
                            "       LOGIN ATTEMPTS EXCEEDED"
                        )

                        print(
                            "========================================"
                        )

                        print(
                            "You have entered the wrong "
                            "password 3 times."
                        )

                        print(
                            "Please try again later or use "
                            "Forgot Password."
                        )

                        print(
                            "========================================"
                        )

                # ====================================
                # PASSWORD FAILED
                # ====================================

                if not password_verified:

                    continue

                # ====================================
                # PASSWORD VERIFIED
                # ====================================

                print(
                    "\n  PASSWORD VERIFIED SUCCESSFULLY "
                )

                # ====================================
                # LOGIN SUCCESSFUL
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
                    found_customer.get(
                        "name",
                        "Customer"
                    )
                )

                print(
                    "========================================"
                )

                # ====================================
                # STORE CUSTOMER IN MEMORY
                # ====================================

                customers = [found_customer]

                # ====================================
                # CUSTOMER DASHBOARD
                # ====================================

                customer_dashboard(
                    found_customer
                )

                # Return after logout

                return

            except psycopg2.Error as error:

                print(
                    "\nDatabase Error:",
                    error
                )

                continue

            finally:

                if cursor is not None:

                    cursor.close()

                connection.close()

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
# ========================================
# ADD NOTIFICATION
# ========================================
def add_notification(customer, message, transaction_id=None):

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to create notification.")

        return False

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # GET CUSTOMER ID
        # ========================================

        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE account_no = %s
            """,
            (customer.get("account_no"),)
        )

        result = cursor.fetchone()

        if result is None:

            print("\nCustomer account not found.")

            return False

        customer_id = result[0]

        # ========================================
        # INSERT NOTIFICATION
        # ========================================

        cursor.execute(
            """
            INSERT INTO notifications
            (
                customer_id,
                message,
                transaction_id,
                is_read
            )
            VALUES
            (
                %s,
                %s,
                %s,
                FALSE
            )
            """,
            (
                customer_id,
                message,
                transaction_id
            )
        )

        connection.commit()

        return True

    except psycopg2.Error as error:

        if connection:
            connection.rollback()

        print(
            "\nDatabase error while creating notification."
        )

        print(
            "Database Error:",
            error
        )

        return False

    finally:

        if cursor:
            cursor.close()

        connection.close()
        

# ========================================
# REPAIR DUPLICATE TRANSACTION IDs
# ========================================

def repair_duplicate_transaction_ids():

    seen_transaction_ids = set()

    repaired_count = 0

    # ========================================
    # COLLECT ALL EXISTING TRANSACTION IDs
    # ========================================

    highest_number = 0

    for customer in customers:

        transactions = customer.get(
            "transactions",
            []
        )

        if not isinstance(
            transactions,
            list
        ):
            continue

        for transaction in transactions:

            if not isinstance(
                transaction,
                dict
            ):
                continue

            transaction_id = transaction.get(
                "transaction_id",
                ""
            )

            if not transaction_id:
                continue

            # Store existing ID
            seen_transaction_ids.add(
                transaction_id
            )

            # Try to extract numeric part
            try:

                number = int(
                    transaction_id.split("-")[-1]
                )

                if number > highest_number:

                    highest_number = number

            except (
                ValueError,
                AttributeError
            ):

                continue

    # ========================================
    # SECOND PASS
    # FIND DUPLICATES
    # ========================================

    processed_ids = set()

    for customer in customers:

        account_no = customer.get(
            "account_no",
            "UNKNOWN"
        )

        transactions = customer.get(
            "transactions",
            []
        )

        if not isinstance(
            transactions,
            list
        ):
            continue

        for transaction in transactions:

            if not isinstance(
                transaction,
                dict
            ):
                continue

            transaction_id = transaction.get(
                "transaction_id",
                ""
            )

            if not transaction_id:
                continue

            # ========================================
            # FIRST OCCURRENCE
            # ========================================

            if transaction_id not in processed_ids:

                processed_ids.add(
                    transaction_id
                )

                continue

            # ========================================
            # DUPLICATE FOUND
            # ========================================

            old_transaction_id = transaction_id

            while True:

                highest_number += 1

                date_part = datetime.now().strftime(
                    "%Y%m%d"
                )

                new_transaction_id = (
                    f"TXN-{date_part}-{highest_number:04d}"
                )

                if new_transaction_id not in seen_transaction_ids:

                    break

            transaction[
                "transaction_id"
            ] = new_transaction_id

            seen_transaction_ids.add(
                new_transaction_id
            )

            processed_ids.add(
                new_transaction_id
            )

            repaired_count += 1

            print("\n========================================")
            print("DUPLICATE TRANSACTION ID REPAIRED")
            print("========================================")

            print(
                "Account:",
                account_no
            )

            print(
                "Old Transaction ID:",
                old_transaction_id
            )

            print(
                "New Transaction ID:",
                new_transaction_id
            )

            print("========================================")

    # ========================================
    # SAVE
    # ========================================

    if repaired_count > 0:

        save_customers()

        print("\n========================================")
        print("DUPLICATE ID REPAIR COMPLETE")
        print("========================================")

        print(
            "Transactions repaired:",
            repaired_count
        )

        print("========================================")

    else:

        print(
            "\nNo duplicate transaction IDs found."
        )

    return repaired_count
#===========================
#check account is active
#===========================
def check_account_active(customer):

    status = customer.get(
        "status",
        "Active"
    )

    if status == "Inactive":

        print("\n========================================")
        print("          TRANSACTION BLOCKED")
        print("========================================")
        print("Your account is currently inactive.")
        print("Please contact the bank administrator.")
        print("========================================")

        return False

    if status == "Closed":

        print("\n========================================")
        print("          TRANSACTION BLOCKED")
        print("========================================")
        print("Your account has been closed.")
        print("Please contact the bank administrator.")
        print("========================================")

        return False

    return True


# ========================================
# CUSTOMER NOTIFICATIONS
# ========================================

def customer_notifications(customer):

    print("\n========================================")
    print("          NOTIFICATIONS")
    print("========================================")

    # ========================================
    # GET NOTIFICATIONS
    # ========================================

    notifications = customer.get(
        "notifications",
        []
    )

    # ========================================
    # CHECK NOTIFICATION DATA
    # ========================================

    if not isinstance(notifications, list):

        print("\nNotification data is invalid.")
        print("========================================")

        input("\nPress Enter to return...")

        return

    # ========================================
    # NO NOTIFICATIONS
    # ========================================

    if len(notifications) == 0:

        print("\nNo notifications found.")
        print("========================================")

        input("\nPress Enter to return...")

        return

    # ========================================
    # DISPLAY NOTIFICATIONS
    # ========================================

    while True:

        print("\n========================================")
        print("          YOUR NOTIFICATIONS")
        print("========================================")

        unread_count = 0

        for index, notification in enumerate(
            notifications,
            start=1
        ):

            if not isinstance(notification, dict):
                continue

            message = notification.get(
                "message",
                "No message"
            )

            date = notification.get(
                "date",
                "Date not available"
            )

            read_status = notification.get(
                "read",
                False
            )

            if read_status:

                status = "READ"

            else:

                status = "UNREAD"

                unread_count += 1

            print("\nNotification", index)
            print("----------------------------------------")

            print(
                "Message :",
                message
            )

            print(
                "Date    :",
                date
            )

            print(
                "Status  :",
                status
            )

        print("\n========================================")
        print(
            "Unread Notifications:",
            unread_count
        )
        print("========================================")

        # ========================================
        # NOTIFICATION MENU
        # ========================================

        print("\n1. Mark Notification as Read")
        print("2. Mark All Notifications as Read")
        print("3. Refresh Notifications")
        print("4. Back")

        choice = input(
            "\nEnter your choice (1-4): "
        ).strip()

        # ========================================
        # MARK ONE AS READ
        # ========================================

        if choice == "1":

            try:

                notification_number = int(
                    input(
                        "Enter notification number: "
                    ).strip()
                )

            except ValueError:

                print(
                    "\nPlease enter a valid number."
                )

                continue

            if (
                notification_number < 1
                or
                notification_number > len(notifications)
            ):

                print(
                    "\nInvalid notification number."
                )

                continue

            notification = notifications[
                notification_number - 1
            ]

            if not isinstance(
                notification,
                dict
            ):

                print(
                    "\nInvalid notification data."
                )

                continue

            notification["read"] = True

            if save_customers():

                print(
                    "\nNotification marked as read."
                )

            else:

                print(
                    "\nNotification could not be saved."
                )

        # ========================================
        # MARK ALL AS READ
        # ========================================

        elif choice == "2":

            for notification in notifications:

                if isinstance(
                    notification,
                    dict
                ):

                    notification["read"] = True

            if save_customers():

                print(
                    "\nAll notifications marked as read."
                )

            else:

                print(
                    "\nNotifications could not be saved."
                )

        # ========================================
        # REFRESH
        # ========================================

        elif choice == "3":

            print(
                "\nRefreshing notifications..."
            )

            continue

        # ========================================
        # BACK
        # ========================================

        elif choice == "4":

            print(
                "\nReturning to customer dashboard..."
            )

            break

        else:

            print(
                "\nInvalid choice!"
            )

            print(
                "Please select 1-4."
            )


# ========================================
# GENERATE TRANSACTION ID
# ========================================
def generate_transaction_id():

    today = datetime.now().strftime("%Y%m%d")

    prefix = f"TXN-{today}-"

    connection = get_db_connection()

    if connection is None:
        return None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT transaction_id
            FROM transactions
            WHERE transaction_id LIKE %s
            ORDER BY transaction_id DESC
            LIMIT 1
            """,
            (prefix + "%",)
        )

        result = cursor.fetchone()

        if result is None:
            highest_number = 0

        else:
            last_transaction_id = result[0]

            try:
                number_part = last_transaction_id[len(prefix):]
                highest_number = int(number_part)

            except (ValueError, TypeError):
                highest_number = 0

        next_number = highest_number + 1

        transaction_id = (
            f"{prefix}{next_number:04d}"
        )

        return transaction_id

    except psycopg2.Error as error:

        print("\nUnable to generate transaction ID.")
        print("Database Error:", error)

        return None

    finally:
        cursor.close()
        connection.close()


# ========================================
# DEPOSIT MONEY
# ========================================
def deposit_money(customer):

    print("\n========================================")
    print("          DEPOSIT MONEY")
    print("========================================")

    # ========================================
    # CHECK ACCOUNT STATUS
    # ========================================

    if not check_account_active(customer):
        return

    # ========================================
    # DEPOSIT AMOUNT
    # ========================================

    while True:

        try:

            amount = Decimal(
                input(
                    "Enter Deposit Amount: ₹"
                ).strip()
            ).quantize(
                Decimal("0.01")
            )

        except (
            InvalidOperation,
            ValueError
        ):

            print("\nInvalid amount.")
            print("Please enter a valid number.")
            continue

        if amount <= Decimal("0.00"):

            print(
                "\nDeposit amount must be greater than zero."
            )

            continue

        break

    # ========================================
    # CONNECT TO POSTGRESQL
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print("\nDeposit could not be saved.")
        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ====================================
        # GET CURRENT BALANCE FROM DATABASE
        # ====================================

        cursor.execute(
            """
            SELECT balance
            FROM customers
            WHERE account_no = %s
            """,
            (
                customer.get("account_no"),
            )
        )

        result = cursor.fetchone()

        if result is None:

            print("\nCustomer account not found.")
            return

        current_balance = to_decimal(
            result[0]
        )

        # ====================================
        # CALCULATE NEW BALANCE
        # ====================================

        new_balance = (
            current_balance + amount
        )

        # ====================================
        # GENERATE TRANSACTION ID
        # ====================================

        transaction_id = generate_transaction_id()

        if transaction_id is None:

            print(
                "\nUnable to generate transaction ID."
            )

            return

        # ====================================
        # UPDATE CUSTOMER BALANCE
        # ====================================

        cursor.execute(
            """
            UPDATE customers
            SET balance = %s
            WHERE account_no = %s
            """,
            (
                new_balance,
                customer.get("account_no")
            )
        )

        # ====================================
        # INSERT DEPOSIT TRANSACTION
        # ====================================

        cursor.execute(
            """
            INSERT INTO transactions
            (
                transaction_id,
                customer_id,
                transaction_type,
                amount,
                date,
                status
            )
            SELECT
                %s,
                customer_id,
                %s,
                %s,
                %s,
                %s
            FROM customers
            WHERE account_no = %s
            """,
            (
                transaction_id,
                "Deposit",
                amount,
                datetime.now(),
                "SUCCESS",
                customer.get("account_no")
            )
        )

        # ====================================
        # COMMIT BOTH CHANGES
        # ====================================

        connection.commit()

        # ====================================
        # UPDATE IN-MEMORY CUSTOMER
        # ====================================

        customer["balance"] = new_balance

        if "transactions" not in customer:

            customer["transactions"] = []

        transaction = {

            "transaction_id":
                transaction_id,

            "type":
                "Deposit",

            "amount":
                amount,

            "date":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "balance_after":
                new_balance
        }

        customer["transactions"].append(
            transaction
        )

        # ====================================
        # NOTIFICATION
        # ====================================

        add_notification(
            customer,
            f"₹{amount:.2f} deposited successfully. "
            f"Transaction ID: {transaction_id}"
        )

        # ====================================
        # SUCCESS MESSAGE
        # ====================================

        print("\n========================================")
        print("        DEPOSIT SUCCESSFUL")
        print("========================================")

        print(
            "Transaction ID :",
            transaction_id
        )

        print(
            "Deposited Amount: ₹",
            format(
                amount,
                ".2f"
            )
        )

        print(
            "Current Balance : ₹",
            format(
                new_balance,
                ".2f"
            )
        )

        print(
            "Date            :",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        print("========================================")

    except psycopg2.Error as error:

        connection.rollback()

        print("\n========================================")
        print("        DEPOSIT NOT SAVED")
        print("========================================")

        print(
            "The deposit could not be saved."
        )

        print(
            "Database Error:",
            error
        )

        print("========================================")

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()

# ========================================
# WITHDRAW MONEY
# ========================================
def withdraw_money(customer):

    print("\n========================================")
    print("          WITHDRAW MONEY")
    print("========================================")

    # ========================================
    # CHECK ACCOUNT STATUS
    # ========================================

    if not check_account_active(customer):
        return

    # ========================================
    # WITHDRAWAL AMOUNT
    # ========================================

    while True:

        try:

            amount = Decimal(
                input(
                    "Enter Withdrawal Amount: ₹"
                ).strip()
            ).quantize(
                Decimal("0.01")
            )

        except (
            InvalidOperation,
            ValueError
        ):

            print("\nInvalid amount.")
            print("Please enter a valid number.")
            continue

        if amount <= Decimal("0.00"):

            print(
                "\nWithdrawal amount must be "
                "greater than zero."
            )

            continue

        break

    # ========================================
    # CONNECT TO POSTGRESQL
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print("\nWithdrawal could not be saved.")
        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ====================================
        # GET CURRENT BALANCE FROM DATABASE
        # ====================================

        cursor.execute(
            """
            SELECT
                customer_id,
                balance
            FROM customers
            WHERE account_no = %s
            """,
            (
                customer.get("account_no"),
            )
        )

        result = cursor.fetchone()

        if result is None:

            print("\nCustomer account not found.")
            return

        customer_id = result[0]

        current_balance = to_decimal(
            result[1]
        )

        # ====================================
        # INSUFFICIENT BALANCE CHECK
        # ====================================

        if amount > current_balance:

            print("\n========================================")
            print("       INSUFFICIENT BALANCE")
            print("========================================")

            print(
                "Current Balance : ₹",
                format(
                    current_balance,
                    ".2f"
                )
            )

            print(
                "Withdrawal Amount: ₹",
                format(
                    amount,
                    ".2f"
                )
            )

            print(
                "You cannot withdraw more than "
                "your available balance."
            )

            print("========================================")

            return

        # ====================================
        # CALCULATE NEW BALANCE
        # ====================================

        new_balance = (
            current_balance - amount
        )

        # ====================================
        # TRANSACTION DATE
        # ====================================

        transaction_date = datetime.now()

        # ====================================
        # GENERATE TRANSACTION ID
        # ====================================

        transaction_id = generate_transaction_id()

        if transaction_id is None:

            print(
                "\nUnable to generate transaction ID."
            )

            return

        # ====================================
        # UPDATE CUSTOMER BALANCE
        # ====================================

        cursor.execute(
            """
            UPDATE customers
            SET balance = %s
            WHERE account_no = %s
            """,
            (
                new_balance,
                customer.get("account_no")
            )
        )

        # ====================================
        # INSERT WITHDRAWAL TRANSACTION
        # ====================================

        cursor.execute(
            """
            INSERT INTO transactions
            (
                transaction_id,
                customer_id,
                transaction_type,
                amount,
                date,
                status
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s
            )
            """,
            (
                transaction_id,
                customer_id,
                "Withdrawal",
                amount,
                transaction_date,
                "SUCCESS"
            )
        )

        # ====================================
        # COMMIT
        # ====================================

        connection.commit()

        # ====================================
        # UPDATE IN-MEMORY CUSTOMER
        # ====================================

        customer["balance"] = new_balance

        if "transactions" not in customer:

            customer["transactions"] = []

        transaction = {

            "transaction_id":
                transaction_id,

            "type":
                "Withdrawal",

            "amount":
                amount,

            "date":
                transaction_date.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "balance_after":
                new_balance
        }

        customer["transactions"].append(
            transaction
        )

        # ====================================
        # NOTIFICATION
        # ====================================
        notification_saved = add_notification(
            customer,
            f"₹{amount:.2f} withdrawn successfully. "
            f"Transaction ID: {transaction_id}",transaction_id
            )

        # ====================================
        # SUCCESS MESSAGE
        # ====================================

        print("\n========================================")
        print("       WITHDRAWAL SUCCESSFUL")
        print("========================================")

        print(
            "Transaction ID  :",
            transaction_id
        )

        print(
            "Withdrawn Amount: ₹",
            format(
                amount,
                ".2f"
            )
        )

        print(
            "Remaining Balance: ₹",
            format(
                new_balance,
                ".2f"
            )
        )

        print(
            "Date             :",
            transaction_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        print("========================================")

    except psycopg2.Error as error:

        connection.rollback()

        print("\n========================================")
        print("       WITHDRAWAL NOT SAVED")
        print("========================================")

        print(
            "The withdrawal could not be saved."
        )

        print(
            "Database Error:",
            error
        )

        print("========================================")

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()


# ========================================
# TRANSACTION HISTORY
# ========================================
def transaction_history(customer):

    print("\n========================================")
    print("          TRANSACTION HISTORY")
    print("========================================")

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to load transaction history.")
        print("========================================")

        input("\nPress Enter to return...")
        return

    cursor = None

    try:

        cursor = connection.cursor()

        account_no = customer.get("account_no")

        # ========================================
        # GET TRANSACTIONS FROM POSTGRESQL
        # ========================================

        cursor.execute(
            """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                date,
                status
            FROM transactions
            WHERE
                customer_id = (
                    SELECT customer_id
                    FROM customers
                    WHERE account_no = %s
                )
                OR sender_account = %s
                OR receiver_account = %s
            ORDER BY date ASC
            """,
            (
                account_no,
                account_no,
                account_no
            )
        )

        transactions = cursor.fetchall()

        # ========================================
        # NO TRANSACTIONS
        # ========================================

        if len(transactions) == 0:

            print("\nNo transactions found.")
            print("========================================")

            input("\nPress Enter to return...")
            return

        # ========================================
        # DISPLAY TRANSACTIONS
        # ========================================

        for index, transaction in enumerate(
            transactions,
            start=1
        ):

            (
                transaction_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                transaction_date,
                status
            ) = transaction

            print(
                f"\nTransaction {index}"
            )

            print(
                "----------------------------------------"
            )

            # ====================================
            # TRANSACTION ID
            # ====================================

            print(
                "Transaction ID :",
                transaction_id
            )

            # ====================================
            # TRANSACTION TYPE
            # ====================================

            if transaction_type == "Transfer":

                if sender_account == account_no:

                    print(
                        "Type           :",
                        "Transfer Sent"
                    )

                elif receiver_account == account_no:

                    print(
                        "Type           :",
                        "Transfer Received"
                    )

                else:

                    print(
                        "Type           :",
                        transaction_type
                    )

            else:

                print(
                    "Type           :",
                    transaction_type
                )

            # ====================================
            # AMOUNT
            # ====================================

            try:

                amount_decimal = to_decimal(
                    amount
                )

                print(
                    "Amount         : ₹",
                    format(
                        amount_decimal,
                        ".2f"
                    )
                )

            except (
                ValueError,
                TypeError,
                InvalidOperation
            ):

                print(
                    "Amount         :",
                    amount
                )

            # ====================================
            # DATE & TIME
            # ====================================

            if transaction_date is not None:

                print(
                    "Date & Time    :",
                    transaction_date.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

            else:

                print(
                    "Date & Time    :",
                    "Date not available"
                )

            # ====================================
            # TRANSFER DETAILS
            # ====================================

            if transaction_type == "Transfer":

                # --------------------------------
                # TRANSFER SENT
                # --------------------------------

                if sender_account == account_no:

                    print(
                        "Receiver Name  :",
                        receiver_name
                    )

                    print(
                        "Receiver Account:",
                        receiver_account
                    )

                # --------------------------------
                # TRANSFER RECEIVED
                # --------------------------------

                elif receiver_account == account_no:

                    print(
                        "Sender Name    :",
                        sender_name
                    )

                    print(
                        "Sender Account :",
                        sender_account
                    )

            # ====================================
            # STATUS
            # ====================================

            print(
                "Status         :",
                status
            )

        # ========================================
        # END
        # ========================================

        print(
            "\n========================================"
        )

        input("\nPress Enter to return...")

    except psycopg2.Error as error:

        print(
            "\nUnable to load transaction history."
        )

        print(
            "Database Error:",
            error
        )

        print(
            "========================================"
        )

        input("\nPress Enter to return...")

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
# ========================================
# TRANSFER MONEY
# ========================================
def transfer_money(customer):

    print("\n========================================")
    print("          TRANSFER MONEY")
    print("========================================")

    # ========================================
    # CHECK SENDER ACCOUNT STATUS
    # ========================================

    if not check_account_active(customer):
        return

    sender_account = customer.get("account_no")

    # ========================================
    # RECEIVER ACCOUNT NUMBER
    # ========================================

    try:

        receiver_account = int(
            input(
                "Enter Receiver Account Number: "
            ).strip()
        )

    except ValueError:

        print(
            "\nAccount number must be a number."
        )

        return

    # ========================================
    # SAME ACCOUNT CHECK
    # ========================================

    if receiver_account == sender_account:

        print(
            "\nYou cannot transfer money "
            "to your own account."
        )

        return

    # ========================================
    # CONNECT TO POSTGRESQL
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print("\nTransfer could not be saved.")
        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ====================================
        # GET SENDER DETAILS
        # ====================================

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                balance,
                status
            FROM customers
            WHERE account_no = %s
            """,
            (
                sender_account,
            )
        )

        sender_result = cursor.fetchone()

        if sender_result is None:

            print(
                "\nSender account not found."
            )

            return

        sender_customer_id = sender_result[0]
        sender_name = sender_result[1]
        sender_balance = to_decimal(
            sender_result[2]
        )
        sender_status = sender_result[3]

        # ====================================
        # CHECK SENDER STATUS
        # ====================================

        if sender_status == "Closed":

            print(
                "\nYour account is closed."
            )

            return

        if sender_status == "Inactive":

            print(
                "\nYour account is inactive."
            )

            return

        # ====================================
        # GET RECEIVER DETAILS
        # ====================================

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                balance,
                status
            FROM customers
            WHERE account_no = %s
            """,
            (
                receiver_account,
            )
        )

        receiver_result = cursor.fetchone()

        # ====================================
        # RECEIVER NOT FOUND
        # ====================================

        if receiver_result is None:

            print(
                "\nReceiver account not found."
            )

            return

        receiver_customer_id = receiver_result[0]
        receiver_name = receiver_result[1]
        receiver_balance = to_decimal(
            receiver_result[2]
        )
        receiver_status = receiver_result[3]

        # ====================================
        # CHECK RECEIVER STATUS
        # ====================================

        if receiver_status == "Closed":

            print(
                "\nReceiver account is closed."
            )

            return

        if receiver_status == "Inactive":

            print(
                "\nReceiver account is inactive."
            )

            return

        # ====================================
        # TRANSFER AMOUNT
        # ========================================

        while True:

            try:

                amount = Decimal(
                    input(
                        "Enter Transfer Amount: ₹"
                    ).strip()
                ).quantize(
                    Decimal("0.01")
                )

            except (
                InvalidOperation,
                ValueError
            ):

                print(
                    "\nInvalid amount."
                )

                print(
                    "Please enter a valid number."
                )

                continue

            if amount <= Decimal("0.00"):

                print(
                    "\nTransfer amount must be "
                    "greater than zero."
                )

                continue

            break

        # ====================================
        # CHECK SENDER BALANCE
        # ====================================

        if amount > sender_balance:

            print("\n========================================")
            print("       INSUFFICIENT BALANCE")
            print("========================================")

            print(
                "Current Balance : ₹",
                format(
                    sender_balance,
                    ".2f"
                )
            )

            print(
                "Transfer Amount  : ₹",
                format(
                    amount,
                    ".2f"
                )
            )

            print(
                "Transfer cannot be completed."
            )

            print("========================================")

            return

        # ====================================
        # CALCULATE NEW BALANCES
        # ====================================

        new_sender_balance = (
            sender_balance - amount
        )

        new_receiver_balance = (
            receiver_balance + amount
        )

        # ====================================
        # TRANSACTION DATE
        # ====================================

        transaction_date = datetime.now()

        # ====================================
        # GENERATE TRANSACTION ID
        # ====================================

        transaction_id = generate_transaction_id()

        if transaction_id is None:

            print(
                "\nUnable to generate transaction ID."
            )

            return

        # ====================================
        # UPDATE SENDER BALANCE
        # ====================================

        cursor.execute(
            """
            UPDATE customers
            SET balance = %s
            WHERE account_no = %s
            """,
            (
                new_sender_balance,
                sender_account
            )
        )

        # ====================================
        # UPDATE RECEIVER BALANCE
        # ====================================

        cursor.execute(
            """
            UPDATE customers
            SET balance = %s
            WHERE account_no = %s
            """,
            (
                new_receiver_balance,
                receiver_account
            )
        )

        # ====================================
        # INSERT ONE TRANSFER RECORD
        # ====================================
        #
        # IMPORTANT:
        # We insert only ONE database transaction
        # because transaction_id is the PRIMARY KEY.
        #
        # sender_account and receiver_account tell
        # us both sides of the transfer.
        #
        # ====================================

        cursor.execute(
            """
            INSERT INTO transactions
            (
                transaction_id,
                customer_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                date,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                transaction_id,
                sender_customer_id,
                "Transfer",
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                transaction_date,
                "SUCCESS"
            )
        )

        # ====================================
        # COMMIT ALL DATABASE CHANGES
        # ====================================

        connection.commit()

        # ====================================
        # UPDATE SENDER IN-MEMORY DATA
        # ====================================

        customer["balance"] = new_sender_balance

        if "transactions" not in customer:
            customer["transactions"] = []

        sender_transaction = {

            "transaction_id":
                transaction_id,

            "type":
                "Transfer Sent",

            "amount":
                amount,

            "date":
                transaction_date.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "sender_name":
                sender_name,

            "sender_account":
                sender_account,

            "receiver_name":
                receiver_name,

            "receiver_account":
                receiver_account,

            "balance_after":
                new_sender_balance,

            "status":
                "SUCCESS"
        }

        customer["transactions"].append(
            sender_transaction
        )

        # ====================================
        # UPDATE RECEIVER IN-MEMORY DATA
        # ====================================

        receiver = {
            "customer_id":
                receiver_customer_id,

            "account_no":
                receiver_account,

            "name":
                receiver_name,

            "balance":
                new_receiver_balance,

            "status":
                receiver_status,

            "transactions":
                []
        }

        receiver_transaction = {

            "transaction_id":
                transaction_id,

            "type":
                "Transfer Received",

            "amount":
                amount,

            "date":
                transaction_date.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "sender_name":
                sender_name,

            "sender_account":
                sender_account,

            "receiver_name":
                receiver_name,

            "receiver_account":
                receiver_account,

            "balance_after":
                new_receiver_balance,

            "status":
                "SUCCESS"
        }

        receiver["transactions"].append(
            receiver_transaction
        )

        # ====================================
        # SENDER NOTIFICATION
        # ====================================

        sender_notification_saved = add_notification(
            customer,
            f"₹{amount:.2f} sent successfully to "
            f"{receiver_name} "
            f"(Account XXXX{str(receiver_account)[-4:]}). "
            f"Transaction ID: {transaction_id}",
            transaction_id
        )

        # ====================================
        # RECEIVER NOTIFICATION
        # ====================================

        receiver_notification_saved = add_notification(
            receiver,
            f"₹{amount:.2f} received from "
            f"{sender_name} "
            f"(Account XXXX{str(sender_account)[-4:]}). "
            f"Transaction ID: {transaction_id}",
            transaction_id
        )

        # ====================================
        # SUCCESS MESSAGE
        # ====================================

        print("\n========================================")
        print("        TRANSFER SUCCESSFUL")
        print("========================================")

        print(
            "Transaction ID :",
            transaction_id
        )

        print(
            "Receiver Name  :",
            receiver_name
        )

        print(
            "Receiver Account:",
            receiver_account
        )

        print(
            "Transfer Amount: ₹",
            format(
                amount,
                ".2f"
            )
        )

        print(
            "Remaining Balance: ₹",
            format(
                new_sender_balance,
                ".2f"
            )
        )

        print(
            "Date            :",
            transaction_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        print("========================================")

    except psycopg2.Error as error:

        connection.rollback()

        print("\n========================================")
        print("        TRANSFER NOT SAVED")
        print("========================================")

        print(
            "The transfer could not be completed."
        )

        print(
            "Both account balances have been "
            "restored automatically."
        )

        print(
            "Database Error:",
            error
        )

        print("========================================")

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
#=========================================
# ADMIN LOGIN
# ========================================
def admin_login():

    print("\n----------ADMIN LOGIN----------")
    print("")

    username = input(
        "Enter Admin Username: "
    ).strip()

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        password = getpass(
            "Enter Admin Password: "
        )

        # Password hash
        entered_password_hash = hash_password(
            password
        )

        # Check username and password
        if (
            username == ADMIN_USERNAME
            and entered_password_hash == ADMIN_PASSWORD_HASH
        ):

            print("\n===========================")
            print("       LOGIN SUCCESSFUL")
            print("===========================")
            print("Welcome, Administrator.")
            print("===========================")

            return True

        # Wrong username or password
        remaining_attempts = (
            max_attempts - attempt
        )

        if remaining_attempts > 0:

            print(
                "\n================================="
            )

            print(
                "      ADMIN LOGIN FAILED"
            )

            print(
                "Invalid Admin Username or Password."
            )

            print(
                "Remaining attempts:",
                remaining_attempts
            )

            print(
                "================================="
            )

        else:

            print(
                "\n================================="
            )

            print(
                "   ADMIN LOGIN ATTEMPTS EXCEEDED"
            )

            print(
                "================================="
            )

            print(
                "You have entered invalid "
                "credentials 3 times."
            )

            print(
                "Please try again later."
            )

            print(
                "================================="
            )

    return False

#==========================================
# admin see all the customers
#==========================================
def view_all_customers():

    print("\n========================================")
    print("          ALL CUSTOMER DETAILS")
    print("========================================")

    connection = get_db_connection()

    if connection is None:
        print("\nUnable to connect to database.")
        input("\nPress Enter to return to Admin Dashboard...")
        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # GET ALL CUSTOMERS FROM POSTGRESQL
        # ========================================

        cursor.execute(
            """
            SELECT
                customer_id,
                account_no,
                name,
                mobile,
                mobile_verified,
                email,
                email_type,
                aadhaar_masked,
                status,
                balance
            FROM customers
            ORDER BY account_no ASC
            """
        )

        customer_rows = cursor.fetchall()

        if not customer_rows:

            print("\nNo customers registered.")

            input(
                "\nPress Enter to return to Admin Dashboard..."
            )

            return

        # ========================================
        # DISPLAY ALL CUSTOMERS
        # ========================================

        for customer_row in customer_rows:

            customer_id = customer_row[0]
            account_no = customer_row[1]
            name = customer_row[2]
            mobile = customer_row[3]
            mobile_verified = customer_row[4]
            email = customer_row[5]
            email_type = customer_row[6]
            aadhaar_masked = customer_row[7]
            status = customer_row[8]
            balance = customer_row[9]

            print("\n----------------------------------------")

            # ========================================
            # CUSTOMER DETAILS
            # ========================================

            print(
                "Account Number   :",
                account_no
            )

            print(
                "Customer Name    :",
                name
            )

            print(
                "Mobile Number    :",
                mobile if mobile else "Not available"
            )

            if mobile_verified:

                print("Mobile Verified  : YES")

            else:

                print("Mobile Verified  : NO")

            print(
                "Email            :",
                email if email else "Not available"
            )

            print(
                "Email Type       :",
                email_type if email_type else "Not available"
            )

            print(
                "Aadhaar          :",
                aadhaar_masked
                if aadhaar_masked
                else "Not available"
            )

            print(
                "Account Status   :",
                status
            )

            print(
                "Balance          : ₹",
                format(
                    balance or Decimal("0.00"),
                    ".2f"
                )
            )

            # ========================================
            # GET CUSTOMER TRANSACTIONS
            # ========================================

            cursor.execute(
                """
                SELECT
                    transaction_id,
                    date,
                    transaction_type,
                    amount,
                    sender_account,
                    receiver_account,
                    sender_name,
                    receiver_name,
                    status
                FROM transactions
                WHERE
                    customer_id = %s
                    OR sender_account = %s
                    OR receiver_account = %s
                ORDER BY date ASC
                """,
                (
                    customer_id,
                    account_no,
                    account_no
                )
            )

            transaction_rows = cursor.fetchall()

            print(
                "Total Transactions:",
                len(transaction_rows)
            )

            if not transaction_rows:

                print("No transactions found.")

                continue

            # ========================================
            # TRANSACTION HISTORY
            # ========================================

            print("\nTransaction History:")

            for transaction_row in transaction_rows:

                transaction_id = transaction_row[0]
                transaction_date = transaction_row[1]
                transaction_type = transaction_row[2]
                amount = transaction_row[3]
                sender_account = transaction_row[4]
                receiver_account = transaction_row[5]
                sender_name = transaction_row[6]
                receiver_name = transaction_row[7]
                transaction_status = transaction_row[8]

                display_type = transaction_type

                # ========================================
                # TRANSFER TYPE
                # ========================================

                if transaction_type == "Transfer":

                    if sender_account == account_no:

                        display_type = "Transfer Sent"

                    elif receiver_account == account_no:

                        display_type = "Transfer Received"

                print(
                    "\n  Transaction ID :",
                    transaction_id
                )

                print(
                    "  Date           :",
                    transaction_date
                )

                print(
                    "  Type           :",
                    display_type
                )

                print(
                    "  Amount         : ₹",
                    format(
                        amount or Decimal("0.00"),
                        ".2f"
                    )
                )

                print(
                    "  Status         :",
                    transaction_status
                )

                # ========================================
                # TRANSFER DETAILS
                # ========================================

                if transaction_type == "Transfer":

                    if sender_account == account_no:

                        print(
                            "  Receiver       :",
                            receiver_name
                            if receiver_name
                            else "Not available"
                        )

                        print(
                            "  Receiver Acct  : XXXX",
                            str(receiver_account)[-4:]
                            if receiver_account
                            else "N/A"
                        )

                    elif receiver_account == account_no:

                        print(
                            "  Sender         :",
                            sender_name
                            if sender_name
                            else "Not available"
                        )

                        print(
                            "  Sender Acct    : XXXX",
                            str(sender_account)[-4:]
                            if sender_account
                            else "N/A"
                        )

                print(
                    "  --------------------------"
                )

        print("\n========================================")

        input(
            "\nPress Enter to return to Admin Dashboard..."
        )

    except psycopg2.Error as error:

        print(
            "\nDatabase error while loading customers."
        )

        print(
            "Database Error:",
            error
        )

        input(
            "\nPress Enter to return to Admin Dashboard..."
        )

    finally:

        if cursor is not None:

            cursor.close()

        connection.close()
#==========================================
#BANKING STATISTICS
#==========================================
def banking_statistics():

    print("\n========================================")
    print("          BANKING STATISTICS")
    print("========================================")

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to connect to database.")

        input(
            "\nPress Enter to return to Admin Dashboard..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # GET BANKING STATISTICS FROM POSTGRESQL
        # ========================================

        cursor.execute(
            """
            SELECT
                COUNT(*),
                COALESCE(SUM(balance), 0),
                COALESCE(MAX(balance), 0),
                COALESCE(MIN(balance), 0),
                COALESCE(AVG(balance), 0)
            FROM customers
            """
        )

        result = cursor.fetchone()

        total_customers = result[0]
        total_balance = result[1]
        highest_balance = result[2]
        lowest_balance = result[3]
        average_balance = result[4]

        # ========================================
        # CHECK CUSTOMER COUNT
        # ========================================

        if total_customers == 0:

            print("\nNo customers registered.")

            input(
                "\nPress Enter to return to Admin Dashboard..."
            )

            return

        # ========================================
        # DISPLAY STATISTICS
        # ========================================

        print(
            "Total Customers    :",
            total_customers
        )

        print(
            "Total Bank Balance : ₹",
            format(
                total_balance,
                ".2f"
            )
        )

        print(
            "Highest Balance    : ₹",
            format(
                highest_balance,
                ".2f"
            )
        )

        print(
            "Lowest Balance     : ₹",
            format(
                lowest_balance,
                ".2f"
            )
        )

        print(
            "Average Balance    : ₹",
            format(
                average_balance,
                ".2f"
            )
        )

        print(
            "========================================"
        )

        input(
            "\nPress Enter to return to Admin Dashboard..."
        )

    except psycopg2.Error as error:

        print(
            "\nDatabase error while loading "
            "banking statistics."
        )

        print(
            "Database Error:",
            error
        )

        input(
            "\nPress Enter to return to Admin Dashboard..."
        )

    finally:

        if cursor is not None:

            cursor.close()

        connection.close()

# ========================================
# SEARCH CUSTOMER
# ========================================
def search_customer():

    print("\n========================================")
    print("          SEARCH CUSTOMER")
    print("========================================")

    # ========================================
    # ACCOUNT NUMBER
    # ========================================

    try:

        account_number = int(
            input("Enter Account Number: ").strip()
        )

    except ValueError:

        print(
            "\nAccount Number must be a number."
        )

        return

    # ========================================
    # DATABASE CONNECTION
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to database."
        )

        input(
            "\nPress Enter to return to Admin Dashboard..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # FIND CUSTOMER FROM POSTGRESQL
        # ========================================

        cursor.execute(
            """
            SELECT
                customer_id,
                account_no,
                name,
                mobile,
                mobile_verified,
                email,
                email_type,
                aadhaar_masked,
                status,
                balance
            FROM customers
            WHERE account_no = %s
            """,
            (account_number,)
        )

        customer_row = cursor.fetchone()

        # ========================================
        # CUSTOMER NOT FOUND
        # ========================================

        if customer_row is None:

            print(
                "\nCustomer not found."
            )

            # ====================================
            # LOG UNSUCCESSFUL SEARCH
            # ====================================

            log_admin_activity(
                "Search Customer",
                (
                    f"Admin searched for account "
                    f"{account_number}, but the customer "
                    f"was not found."
                )
            )

            input(
                "\nPress Enter to return to Admin Dashboard..."
            )

            return

        # ========================================
        # CUSTOMER DETAILS
        # ========================================

        customer_id = customer_row[0]
        account_no = customer_row[1]
        name = customer_row[2]
        mobile = customer_row[3]
        mobile_verified = customer_row[4]
        email = customer_row[5]
        email_type = customer_row[6]
        aadhaar_masked = customer_row[7]
        status = customer_row[8]
        balance = customer_row[9]

        # ========================================
        # DISPLAY CUSTOMER DETAILS
        # ========================================

        print(
            "\n========================================"
        )

        print(
            "         CUSTOMER DETAILS"
        )

        print(
            "========================================"
        )

        print(
            "Account Number   :",
            account_no
        )

        print(
            "Customer Name    :",
            name
        )

        print(
            "Mobile Number    :",
            mobile
            if mobile
            else "Not available"
        )

        # ========================================
        # MOBILE VERIFICATION
        # ========================================

        if mobile_verified:

            print(
                "Mobile Verified  : YES"
            )

        else:

            print(
                "Mobile Verified  : NO"
            )

        # ========================================
        # EMAIL
        # ========================================

        print(
            "Email            :",
            email
            if email
            else "Not available"
        )

        print(
            "Email Type       :",
            email_type
            if email_type
            else "Not available"
        )

        # ========================================
        # AADHAAR
        # ========================================

        print(
            "Aadhaar          :",
            aadhaar_masked
            if aadhaar_masked
            else "Not available"
        )

        # ========================================
        # ACCOUNT STATUS
        # ========================================

        print(
            "Account Status   :",
            status
        )

        # ========================================
        # BALANCE
        # ========================================

        print(
            "Balance          : ₹",
            format(
                balance or Decimal("0.00"),
                ".2f"
            )
        )

        # ========================================
        # GET TRANSACTIONS
        # ========================================

        cursor.execute(
            """
            SELECT
                transaction_id,
                date,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                status
            FROM transactions
            WHERE
                customer_id = %s
                OR sender_account = %s
                OR receiver_account = %s
            ORDER BY date ASC
            """,
            (
                customer_id,
                account_no,
                account_no
            )
        )

        transaction_rows = cursor.fetchall()

        # ========================================
        # TRANSACTION COUNT
        # ========================================

        print(
            "Total Transactions:",
            len(transaction_rows)
        )

        # ========================================
        # TRANSACTION HISTORY
        # ========================================

        print(
            "\n========================================"
        )

        print(
            "         TRANSACTION HISTORY"
        )

        print(
            "========================================"
        )

        if not transaction_rows:

            print(
                "No transactions found."
            )

        else:

            for index, transaction_row in enumerate(
                transaction_rows,
                start=1
            ):

                # ====================================
                # TRANSACTION DATA
                # ====================================

                transaction_id = transaction_row[0]
                transaction_date = transaction_row[1]
                transaction_type = transaction_row[2]
                amount = transaction_row[3]
                sender_account = transaction_row[4]
                receiver_account = transaction_row[5]
                sender_name = transaction_row[6]
                receiver_name = transaction_row[7]
                transaction_status = transaction_row[8]

                # ====================================
                # DISPLAY TRANSACTION TYPE
                # ====================================

                display_type = transaction_type

                if transaction_type == "Transfer":

                    if sender_account == account_no:

                        display_type = "Transfer Sent"

                    elif receiver_account == account_no:

                        display_type = "Transfer Received"

                # ====================================
                # DISPLAY TRANSACTION
                # ====================================

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
                    transaction_date
                )

                print(
                    "Type           :",
                    display_type
                )

                print(
                    "Amount         : ₹",
                    format(
                        amount or Decimal("0.00"),
                        ".2f"
                    )
                )

                print(
                    "Status         :",
                    transaction_status
                )

                # ====================================
                # TRANSFER DETAILS
                # ====================================

                if transaction_type == "Transfer":

                    if sender_account == account_no:

                        print(
                            "Receiver       :",
                            receiver_name
                            if receiver_name
                            else "Not available"
                        )

                        print(
                            "Receiver Acct  : XXXX",
                            (
                                str(receiver_account)[-4:]
                                if receiver_account
                                else "N/A"
                            )
                        )

                    elif receiver_account == account_no:

                        print(
                            "Sender         :",
                            sender_name
                            if sender_name
                            else "Not available"
                        )

                        print(
                            "Sender Acct    : XXXX",
                            (
                                str(sender_account)[-4:]
                                if sender_account
                                else "N/A"
                            )
                        )

                print(
                    "----------------------------------------"
                )

        print(
            "========================================"
        )

        # ========================================
        # LOG SUCCESSFUL SEARCH
        # ========================================

        log_admin_activity(
            "Search Customer",
            (
                f"Admin searched customer account "
                f"{account_number} belonging to "
                f"{name}."
            )
        )

        # ========================================
        # RETURN
        # ========================================

        input(
            "\nPress Enter to return to Admin Dashboard..."
        )

    except psycopg2.Error as error:

        print(
            "\nDatabase error while searching customer."
        )

        print(
            "Database Error:",
            error
        )

        input(
            "\nPress Enter to return to Admin Dashboard..."
        )

    finally:

        if cursor is not None:

            cursor.close()

        connection.close()
# ========================================
# SEARCH TRANSACTIONS
# ========================================
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

        # ========================================
        # SELECT SEARCH TYPE
        # ========================================

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
        print(
            "Searching:",
            search_type
        )
        print("========================================")

        connection = get_db_connection()

        if connection is None:

            print("\nUnable to connect to database.")

            input(
                "\nPress Enter to continue..."
            )

            continue

        cursor = None

        found = False

        try:

            cursor = connection.cursor()

            # ========================================
            # SEARCH DEPOSITS / WITHDRAWALS
            # ========================================

            if search_type in ["Deposit", "Withdrawal"]:

                cursor.execute(
                    """
                    SELECT
                        c.name,
                        c.account_no,
                        t.transaction_id,
                        t.date,
                        t.transaction_type,
                        t.amount
                    FROM transactions t
                    JOIN customers c
                        ON t.customer_id = c.customer_id
                    WHERE t.transaction_type = %s
                    ORDER BY t.date DESC
                    """,
                    (search_type,)
                )

            # ========================================
            # SEARCH TRANSFERS
            # ========================================

            else:

                cursor.execute(
                    """
                    SELECT
                        c.name,
                        c.account_no,
                        t.transaction_id,
                        t.date,
                        t.transaction_type,
                        t.amount,
                        t.sender_name,
                        t.sender_account,
                        t.receiver_name,
                        t.receiver_account
                    FROM transactions t
                    JOIN customers c
                        ON t.customer_id = c.customer_id
                    WHERE t.transaction_type = 'Transfer'
                    ORDER BY t.date DESC
                    """
                )

            transactions = cursor.fetchall()

            # ========================================
            # DISPLAY RESULTS
            # ========================================

            for transaction in transactions:

                found = True

                if search_type in ["Deposit", "Withdrawal"]:

                    customer_name = transaction[0]
                    account_no = transaction[1]
                    transaction_id = transaction[2]
                    date_time = transaction[3]
                    transaction_type = transaction[4]
                    amount = transaction[5]

                    print(
                        "\nCustomer       :",
                        customer_name
                    )

                    print(
                        "Account        :",
                        account_no
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

                    try:

                        print(
                            "Amount         : ₹",
                            format(
                                float(amount),
                                ".2f"
                            )
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        print(
                            "Amount         :",
                            amount
                        )

                else:

                    customer_name = transaction[0]
                    account_no = transaction[1]
                    transaction_id = transaction[2]
                    date_time = transaction[3]
                    transaction_type = transaction[4]
                    amount = transaction[5]
                    sender_name = transaction[6]
                    sender_account = transaction[7]
                    receiver_name = transaction[8]
                    receiver_account = transaction[9]

                    print(
                        "\nCustomer       :",
                        customer_name
                    )

                    print(
                        "Account        :",
                        account_no
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

                    try:

                        print(
                            "Amount         : ₹",
                            format(
                                float(amount),
                                ".2f"
                            )
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        print(
                            "Amount         :",
                            amount
                        )

                    print(
                        "Sender         :",
                        sender_name
                        if sender_name
                        else "Not available"
                    )

                    print(
                        "Sender Account :",
                        sender_account
                        if sender_account
                        else "Not available"
                    )

                    print(
                        "Receiver       :",
                        receiver_name
                        if receiver_name
                        else "Not available"
                    )

                    print(
                        "Receiver Account:",
                        receiver_account
                        if receiver_account
                        else "Not available"
                    )

                print(
                    "----------------------------------------"
                )

            # ========================================
            # NO TRANSACTIONS FOUND
            # ========================================

            if not found:

                print(
                    "\nNo",
                    search_type,
                    "transactions found."
                )

            # ========================================
            # ACTIVITY LOG
            # ========================================

            if found:

                log_admin_activity(
                    "Search Transactions",
                    (
                        f"Admin searched for "
                        f"{search_type} transactions. "
                        f"Matching transactions were found."
                    )
                )

            else:

                log_admin_activity(
                    "Search Transactions",
                    (
                        f"Admin searched for "
                        f"{search_type} transactions, "
                        f"but no matching transactions were found."
                    )
                )

            print(
                "========================================"
            )

        except psycopg2.Error as error:

            print(
                "\nDatabase error while searching transactions."
            )

            print(
                "Database Error:",
                error
            )

        finally:

            if cursor is not None:
                cursor.close()

            connection.close()

        input(
            "\nPress Enter to continue..."
        )


# ========================================
# CHANGE ACCOUNT STATUS
# ========================================
def change_account_status():

    print("\n========================================")
    print("       CHANGE ACCOUNT STATUS")
    print("========================================")

    try:

        account_number = int(
            input("Enter Account Number: ").strip()
        )

    except ValueError:

        print(
            "\nAccount Number must be a number."
        )

        return

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to database."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # FIND CUSTOMER
        # ========================================

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                status
            FROM customers
            WHERE account_no = %s
            """,
            (account_number,)
        )

        customer = cursor.fetchone()

        # ========================================
        # CUSTOMER NOT FOUND
        # ========================================

        if customer is None:

            print(
                "\nCustomer not found."
            )

            return

        customer_id = customer[0]
        customer_name = customer[1]
        current_status = customer[2]

        if not current_status:

            current_status = "Active"

        # ========================================
        # DISPLAY CURRENT DETAILS
        # ========================================

        print(
            "\nCustomer Name :",
            customer_name
        )

        print(
            "Account Number:",
            account_number
        )

        print(
            "Current Status:",
            current_status
        )

        # ========================================
        # CLOSED ACCOUNT
        # ========================================

        if current_status == "Closed":

            print(
                "\n========================================"
            )

            print(
                "       ACCOUNT PERMANENTLY CLOSED"
            )

            print(
                "========================================"
            )

            print(
                "A closed account cannot be activated"
            )

            print(
                "or deactivated."
            )

            print(
                "Please create a new account if required."
            )

            print(
                "========================================"
            )

            log_admin_activity(
                "Change Account Status",
                (
                    f"Admin attempted to change status "
                    f"of closed account {account_number}."
                )
            )

            return

        # ========================================
        # STATUS OPTIONS
        # ========================================

        print(
            "\n1. Activate Account"
        )

        print(
            "2. Deactivate Account"
        )

        print(
            "3. Cancel"
        )

        choice = input(
            "\nEnter your choice (1-3): "
        ).strip()

        # ========================================
        # ACTIVATE
        # ========================================

        if choice == "1":

            if current_status == "Active":

                print(
                    "\nAccount is already active."
                )

                return

            cursor.execute(
                """
                UPDATE customers
                SET status = 'Active'
                WHERE customer_id = %s
                """,
                (customer_id,)
            )

            connection.commit()

            print(
                "\n========================================"
            )

            print(
                "      ACCOUNT ACTIVATED SUCCESSFULLY"
            )

            print(
                "========================================"
            )

            print(
                "Account Number:",
                account_number
            )

            print(
                "Customer Name :",
                customer_name
            )

            print(
                "New Status    : Active"
            )

            print(
                "========================================"
            )

            log_admin_activity(
                "Activate Account",
                (
                    f"Admin activated account "
                    f"{account_number} "
                    f"({customer_name})."
                )
            )

        # ========================================
        # DEACTIVATE
        # ========================================

        elif choice == "2":

            if current_status == "Inactive":

                print(
                    "\nAccount is already inactive."
                )

                return

            confirmation = input(
                "\nAre you sure you want to deactivate "
                "this account? (yes/no): "
            ).strip().lower()

            if confirmation != "yes":

                print(
                    "\nOperation cancelled."
                )

                return

            cursor.execute(
                """
                UPDATE customers
                SET status = 'Inactive'
                WHERE customer_id = %s
                """,
                (customer_id,)
            )

            connection.commit()

            print(
                "\n========================================"
            )

            print(
                "    ACCOUNT DEACTIVATED SUCCESSFULLY"
            )

            print(
                "========================================"
            )

            print(
                "Account Number:",
                account_number
            )

            print(
                "Customer Name :",
                customer_name
            )

            print(
                "New Status    : Inactive"
            )

            print(
                "========================================"
            )

            log_admin_activity(
                "Deactivate Account",
                (
                    f"Admin deactivated account "
                    f"{account_number} "
                    f"({customer_name})."
                )
            )

        # ========================================
        # CANCEL
        # ========================================

        elif choice == "3":

            print(
                "\nOperation cancelled."
            )

        # ========================================
        # INVALID CHOICE
        # ========================================

        else:

            print(
                "\nInvalid Choice."
            )

            print(
                "Please enter 1, 2 or 3."
            )

    except psycopg2.Error as error:

        connection.rollback()

        print(
            "\nDatabase error while changing "
            "account status."
        )

        print(
            "Database Error:",
            error
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
# ========================================
# CLOSE CUSTOMER ACCOUNT
# ========================================
def close_customer_account():

    print("\n========================================")
    print("        CLOSE CUSTOMER ACCOUNT")
    print("========================================")

    # ========================================
    # ACCOUNT NUMBER
    # ========================================

    try:

        account_number = int(
            input("Enter Account Number: ").strip()
        )

    except ValueError:

        print(
            "\nAccount Number must be a number."
        )

        return

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to database."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # FIND CUSTOMER
        # ========================================

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                balance,
                status
            FROM customers
            WHERE account_no = %s
            """,
            (account_number,)
        )

        customer = cursor.fetchone()

        # ========================================
        # CUSTOMER NOT FOUND
        # ========================================

        if customer is None:

            print(
                "\nCustomer not found."
            )

            return

        customer_id = customer[0]
        customer_name = customer[1]
        balance = customer[2]
        current_status = customer[3]

        if not current_status:

            current_status = "Active"

        # ========================================
        # ALREADY CLOSED
        # ========================================

        if current_status == "Closed":

            print(
                "\n========================================"
            )

            print(
                "       ACCOUNT ALREADY CLOSED"
            )

            print(
                "========================================"
            )

            print(
                "This customer account is already closed."
            )

            return

        # ========================================
        # CUSTOMER DETAILS
        # ========================================

        print(
            "\nCustomer Name :",
            customer_name
        )

        print(
            "Account Number:",
            account_number
        )

        print(
            "Current Status:",
            current_status
        )

        try:

            print(
                "Balance       : ₹",
                format(
                    float(balance),
                    ".2f"
                )
            )

        except (
            ValueError,
            TypeError
        ):

            print(
                "Balance       :",
                balance
            )

        # ========================================
        # CONFIRMATION
        # ========================================

        confirmation = input(
            "\nAre you sure you want to close "
            "this account? (yes/no): "
        ).strip().lower()

        # ========================================
        # CLOSE ACCOUNT
        # ========================================

        if confirmation == "yes":

            cursor.execute(
                """
                UPDATE customers
                SET status = 'Closed'
                WHERE customer_id = %s
                """,
                (customer_id,)
            )

            connection.commit()

            # ====================================
            # ADMIN ACTIVITY LOG
            # ====================================

            log_admin_activity(
                "Close Customer Account",
                (
                    f"Admin closed account "
                    f"{account_number} belonging to "
                    f"{customer_name}."
                )
            )

            # ====================================
            # SUCCESS MESSAGE
            # ====================================

            print(
                "\n========================================"
            )

            print(
                "       ACCOUNT CLOSED SUCCESSFULLY"
            )

            print(
                "========================================"
            )

            print(
                "Account Number:",
                account_number
            )

            print(
                "Customer Name :",
                customer_name
            )

            print(
                "Account Status: Closed"
            )

            print(
                "========================================"
            )

        # ========================================
        # CANCEL
        # ========================================

        elif confirmation == "no":

            print(
                "\nAccount closing cancelled."
            )

        # ========================================
        # INVALID INPUT
        # ========================================

        else:

            print(
                "\nInvalid choice."
            )

            print(
                "Please enter yes or no."
            )

    except psycopg2.Error as error:

        connection.rollback()

        print(
            "\nDatabase error while closing "
            "customer account."
        )

        print(
            "Database Error:",
            error
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()

#====================================
#admin banking summary
#====================================
def banking_summary():

    print("\n========================================")
    print("           BANKING SUMMARY")
    print("========================================")

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to connect to database.")

        input(
            "\nPress Enter to return to Admin Dashboard..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ====================================
        # ACCOUNT STATISTICS
        # ====================================

        cursor.execute(
            """
            SELECT
                COUNT(*),
                COUNT(*) FILTER (
                    WHERE status = 'Active'
                ),
                COUNT(*) FILTER (
                    WHERE status = 'Inactive'
                ),
                COUNT(*) FILTER (
                    WHERE status = 'Closed'
                ),
                COALESCE(
                    SUM(balance),
                    0
                )
            FROM customers
            """
        )

        customer_data = cursor.fetchone()

        total_customers = customer_data[0]
        active_accounts = customer_data[1]
        inactive_accounts = customer_data[2]
        closed_accounts = customer_data[3]
        total_balance = customer_data[4]

        # ====================================
        # TRANSACTION STATISTICS
        # ====================================

        cursor.execute(
            """
            SELECT
                COUNT(*),

                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type
                            IN ('Deposit', 'Initial Deposit')
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ),

                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Withdrawal'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ),

                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Transfer'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                )

            FROM transactions
            """
        )

        transaction_data = cursor.fetchone()

        total_transactions = transaction_data[0]
        total_deposits = transaction_data[1]
        total_withdrawals = transaction_data[2]
        total_transfers = transaction_data[3]

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
                float(total_balance),
                ".2f"
            )
        )

        print(
            "Total Deposits        : ₹",
            format(
                float(total_deposits),
                ".2f"
            )
        )

        print(
            "Total Withdrawals     : ₹",
            format(
                float(total_withdrawals),
                ".2f"
            )
        )

        print(
            "Total Transfers       : ₹",
            format(
                float(total_transfers),
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

    except psycopg2.Error as error:

        print(
            "\nDatabase error while loading "
            "banking summary."
        )

        print(
            "Database Error:",
            error
        )

        input(
            "\nPress Enter to return to Admin Dashboard..."
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
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

# ========================================
# FILTER TRANSACTIONS
# ========================================

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

    # ========================================
    # BACK
    # ========================================

    if choice == "6":

        print(
            "\nReturning to Admin Dashboard..."
        )

        return

    # ========================================
    # ALL TRANSACTIONS
    # ========================================

    if choice == "5":

        selected_type = None

        log_description = (
            "Admin filtered all transactions."
        )

    # ========================================
    # SELECTED TRANSACTION TYPE
    # ========================================

    elif choice in transaction_types:

        selected_type = transaction_types[
            choice
        ]

        log_description = (
            f"Admin filtered transactions "
            f"by type: {selected_type}."
        )

    # ========================================
    # INVALID CHOICE
    # ========================================

    else:

        print(
            "\nInvalid Choice."
        )

        return

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to database."
        )

        input(
            "\nPress Enter to return to Admin Dashboard..."
        )

        return

    cursor = None

    found = False

    transaction_count = 0

    try:

        cursor = connection.cursor()

        # ========================================
        # DEPOSIT FILTER
        # Includes Initial Deposit
        # ========================================

        if selected_type == "Deposit":

            cursor.execute(
                """
                SELECT
                    c.name,
                    c.account_no,
                    t.transaction_id,
                    t.transaction_type,
                    t.amount,
                    t.date
                FROM transactions t
                JOIN customers c
                    ON t.customer_id = c.customer_id
                WHERE t.transaction_type IN (
                    'Deposit',
                    'Initial Deposit'
                )
                ORDER BY t.date DESC
                """
            )

        # ========================================
        # WITHDRAWAL FILTER
        # ========================================

        elif selected_type == "Withdrawal":

            cursor.execute(
                """
                SELECT
                    c.name,
                    c.account_no,
                    t.transaction_id,
                    t.transaction_type,
                    t.amount,
                    t.date
                FROM transactions t
                JOIN customers c
                    ON t.customer_id = c.customer_id
                WHERE t.transaction_type = 'Withdrawal'
                ORDER BY t.date DESC
                """
            )

        # ========================================
        # TRANSFER SENT
        # ========================================

        elif selected_type == "Transfer Sent":

            cursor.execute(
                """
                SELECT
                    c.name,
                    c.account_no,
                    t.transaction_id,
                    t.transaction_type,
                    t.amount,
                    t.date
                FROM transactions t
                JOIN customers c
                    ON t.sender_account = c.account_no
                WHERE t.transaction_type = 'Transfer'
                ORDER BY t.date DESC
                """
            )

        # ========================================
        # TRANSFER RECEIVED
        # ========================================

        elif selected_type == "Transfer Received":

            cursor.execute(
                """
                SELECT
                    c.name,
                    c.account_no,
                    t.transaction_id,
                    t.transaction_type,
                    t.amount,
                    t.date
                FROM transactions t
                JOIN customers c
                    ON t.receiver_account = c.account_no
                WHERE t.transaction_type = 'Transfer'
                ORDER BY t.date DESC
                """
            )

        # ========================================
        # ALL TRANSACTIONS
        # ========================================

        else:

            cursor.execute(
                """
                SELECT
                    c.name,
                    c.account_no,
                    t.transaction_id,
                    t.transaction_type,
                    t.amount,
                    t.date
                FROM transactions t
                JOIN customers c
                    ON t.customer_id = c.customer_id
                ORDER BY t.date DESC
                """
            )

        transactions = cursor.fetchall()

        print("\n========================================")
        print("          TRANSACTION RESULTS")
        print("========================================")

        # ========================================
        # DISPLAY RESULTS
        # ========================================

        for transaction in transactions:

            found = True

            transaction_count += 1

            customer_name = transaction[0]
            account_no = transaction[1]
            transaction_id = transaction[2]
            transaction_type = transaction[3]
            amount = transaction[4]
            date_time = transaction[5]

            # ====================================
            # DISPLAY TRANSFER TYPE
            # ====================================

            display_type = transaction_type

            if transaction_type == "Transfer":

                if selected_type == "Transfer Sent":

                    display_type = "Transfer Sent"

                elif selected_type == "Transfer Received":

                    display_type = "Transfer Received"

                else:

                    display_type = "Transfer"

            print(
                "\nCustomer       :",
                customer_name
            )

            print(
                "Account Number :",
                account_no
            )

            print(
                "Transaction ID :",
                transaction_id
            )

            print(
                "Transaction    :",
                display_type
            )

            try:

                print(
                    "Amount         : ₹",
                    format(
                        float(amount),
                        ".2f"
                    )
                )

            except (
                ValueError,
                TypeError
            ):

                print(
                    "Amount         :",
                    amount
                )

            print(
                "Date & Time    :",
                date_time
            )

            print(
                "----------------------------------------"
            )

        # ========================================
        # NO TRANSACTIONS
        # ========================================

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

        # ========================================
        # RESULTS COUNT
        # ========================================

        else:

            print(
                "\nTotal Matching Transactions:",
                transaction_count
            )

        print(
            "========================================"
        )

        # ========================================
        # ADMIN ACTIVITY LOG
        # ========================================

        if found:

            log_admin_activity(
                "Filter Transactions",
                (
                    f"{log_description} "
                    f"{transaction_count} matching "
                    f"transaction(s) found."
                )
            )

        else:

            log_admin_activity(
                "Filter Transactions",
                (
                    f"{log_description} "
                    "No matching transactions found."
                )
            )

    except psycopg2.Error as error:

        print(
            "\nDatabase error while filtering transactions."
        )

        print(
            "Database Error:",
            error
        )

    finally:

        if cursor is not None:

            cursor.close()

        connection.close()

    input(
        "\nPress Enter to return to Admin Dashboard..."
    )

# ========================================
# SEARCH TRANSACTION BY ID
# ========================================
def search_transaction_by_id():

    print("\n========================================")
    print("       SEARCH TRANSACTION BY ID")
    print("========================================")

    # ========================================
    # GET TRANSACTION ID
    # ========================================

    transaction_id = input(
        "\nEnter Transaction ID: "
    ).strip()

    # ========================================
    # EMPTY ID CHECK
    # ========================================

    if not transaction_id:

        print(
            "\nTransaction ID cannot be empty."
        )

        return

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to database."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # SEARCH TRANSACTION IN POSTGRESQL
        # ========================================

        cursor.execute(
            """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                status,
                date,
                sender_name,
                sender_account,
                receiver_name,
                receiver_account
            FROM transactions
            WHERE transaction_id = %s
            """,
            (transaction_id,)
        )

        transaction = cursor.fetchone()

        # ========================================
        # TRANSACTION NOT FOUND
        # ========================================

        if transaction is None:

            print(
                "\nTransaction not found."
            )

            log_admin_activity(
                "Search Transaction by ID",
                (
                    f"Admin searched for transaction "
                    f"ID {transaction_id}, but the "
                    f"transaction was not found."
                )
            )

            return

        # ========================================
        # DISPLAY TRANSACTION
        # ========================================

        print("\n========================================")
        print("       TRANSACTION DETAILS")
        print("========================================")

        transaction_id = transaction[0]
        transaction_type = transaction[1]
        amount = transaction[2]
        status = transaction[3]
        date_time = transaction[4]
        sender_name = transaction[5]
        sender_account = transaction[6]
        receiver_name = transaction[7]
        receiver_account = transaction[8]

        # ========================================
        # BASIC TRANSACTION DETAILS
        # ========================================

        print(
            "Transaction ID   :",
            transaction_id
        )

        print(
            "Transaction Type :",
            transaction_type
        )

        # ========================================
        # AMOUNT
        # ========================================

        try:

            print(
                "Amount           : ₹",
                format(
                    float(amount),
                    ".2f"
                )
            )

        except (
            ValueError,
            TypeError
        ):

            print(
                "Amount           :",
                amount
            )

        # ========================================
        # STATUS
        # ========================================

        print(
            "Status           :",
            status
            if status
            else "SUCCESS"
        )

        # ========================================
        # DATE & TIME
        # ========================================

        print(
            "Date & Time      :",
            date_time
            if date_time
            else "Date not available"
        )

        # ========================================
        # SENDER DETAILS
        # ========================================

        print(
            "Sender Name      :",
            sender_name
            if sender_name
            else "Not available"
        )

        print(
            "Sender Account   :",
            sender_account
            if sender_account
            else "Not available"
        )

        # ========================================
        # RECEIVER DETAILS
        # ========================================

        print(
            "Receiver Name    :",
            receiver_name
            if receiver_name
            else "Not available"
        )

        print(
            "Receiver Account :",
            receiver_account
            if receiver_account
            else "Not available"
        )

        print(
            "========================================"
        )

        # ========================================
        # ADMIN ACTIVITY LOG
        # ========================================

        log_admin_activity(
            "Search Transaction by ID",
            (
                f"Admin searched for transaction "
                f"ID {transaction_id}. "
                f"Transaction was found."
            )
        )

    except psycopg2.Error as error:

        print(
            "\nDatabase error while searching "
            "transaction by ID."
        )

        print(
            "Database Error:",
            error
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
#==========================
#validate transaction data
#============================
def validate_transaction_data(transaction):

    if not isinstance(transaction, dict):

        return False

    transaction_id = transaction.get(
        "transaction_id"
    )

    transaction_type = transaction.get(
        "type"
    )

    amount = transaction.get(
        "amount"
    )

    transaction_date = transaction.get(
        "date"
    )

    if not transaction_id:

        return False

    if not transaction_type:

        return False

    if amount is None:

        return False

    if not transaction_date:

        return False

    try:

        amount = float(amount)

    except (ValueError, TypeError):

        return False

    if amount <= 0:

        return False

    return True

# export all transactions
def export_all_transactions():

    print("\n========================================")
    print("       EXPORT ALL TRANSACTIONS")
    print("========================================")

    filename = "all_transactions.csv"

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to connect to database.")

        input("\nPress Enter to return...")

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ====================================
        # GET ALL TRANSACTIONS
        # ====================================

        cursor.execute(
            """
            SELECT
                t.transaction_id,
                c.name,
                c.account_no,
                t.transaction_type,
                t.amount,
                t.status,
                t.date,
                t.sender_name,
                t.sender_account,
                t.receiver_name,
                t.receiver_account
            FROM transactions t
            LEFT JOIN customers c
                ON t.customer_id = c.customer_id
            ORDER BY t.date ASC
            """
        )

        transactions = cursor.fetchall()

        total_transactions = 0

        # ====================================
        # CREATE CSV FILE
        # ====================================

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
            # WRITE TRANSACTIONS
            # ====================================

            for transaction in transactions:

                writer.writerow([

                    transaction[0]
                    if transaction[0] is not None
                    else "Not available",

                    transaction[1]
                    if transaction[1] is not None
                    else "Not available",

                    transaction[2]
                    if transaction[2] is not None
                    else "Not available",

                    transaction[3]
                    if transaction[3] is not None
                    else "Unknown",

                    transaction[4]
                    if transaction[4] is not None
                    else 0,

                    transaction[5]
                    if transaction[5] is not None
                    else "SUCCESS",

                    transaction[6]
                    if transaction[6] is not None
                    else "Not available",

                    transaction[7]
                    if transaction[7] is not None
                    else "Not available",

                    transaction[8]
                    if transaction[8] is not None
                    else "Not available",

                    transaction[9]
                    if transaction[9] is not None
                    else "Not available",

                    transaction[10]
                    if transaction[10] is not None
                    else "Not available"
                ])

                total_transactions += 1

        # ====================================
        # SUCCESS
        # ====================================

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

    except psycopg2.Error as error:

        print("\n========================================")
        print("          EXPORT FAILED")
        print("========================================")

        print(
            "Database Error:",
            error
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

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()

    input(
        "\nPress Enter to return..."
    )
#==============================
#admin transaction statistics
#============================
def admin_transaction_statistics():

    print("\n========================================")
    print("       TRANSACTION STATISTICS")
    print("========================================")

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to connect to database.")

        input(
            "\nPress Enter to return..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # GET TRANSACTION STATISTICS
        # ========================================

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_transactions,

                COUNT(*) FILTER (
                    WHERE transaction_type = 'Deposit'
                ) AS deposit_count,

                COUNT(*) FILTER (
                    WHERE transaction_type = 'Withdrawal'
                ) AS withdrawal_count,

                COUNT(*) FILTER (
                    WHERE transaction_type = 'Transfer'
                ) AS transfer_count,

                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Deposit'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ) AS total_deposits,

                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Withdrawal'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ) AS total_withdrawals,

                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Transfer'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ) AS total_transfers

            FROM transactions
            """
        )

        result = cursor.fetchone()

        total_transactions = result[0]
        deposit_count = result[1]
        withdrawal_count = result[2]
        transfer_count = result[3]

        total_deposits = result[4]
        total_withdrawals = result[5]
        total_transfers = result[6]

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
            "Transfer Count          :",
            transfer_count
        )

        print("\n----------------------------------------")
        print("          TRANSACTION AMOUNTS")
        print("----------------------------------------")

        print(
            "Total Deposits          : ₹",
            format(
                float(total_deposits),
                ".2f"
            )
        )

        print(
            "Total Withdrawals       : ₹",
            format(
                float(total_withdrawals),
                ".2f"
            )
        )

        print(
            "Total Transfers         : ₹",
            format(
                float(total_transfers),
                ".2f"
            )
        )

        print("\n========================================")

        input(
            "\nPress Enter to return..."
        )

    except psycopg2.Error as error:

        print("\n========================================")
        print("       DATABASE ERROR")
        print("========================================")

        print(
            "Database Error:",
            error
        )

        print("========================================")

        input(
            "\nPress Enter to return..."
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
#==========================
# admin customer statistics
#=========================
def admin_customer_statistics():

    print("\n========================================")
    print("       CUSTOMER STATISTICS")
    print("========================================")

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to connect to database.")

        input(
            "\nPress Enter to return..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # CUSTOMER STATISTICS
        # ========================================

        cursor.execute(
            """
            SELECT
                COUNT(*),

                COUNT(*) FILTER (
                    WHERE status = 'Active'
                ),

                COUNT(*) FILTER (
                    WHERE status = 'Inactive'
                ),

                COUNT(*) FILTER (
                    WHERE status = 'Closed'
                ),

                COALESCE(
                    SUM(balance),
                    0
                ),

                COALESCE(
                    AVG(balance),
                    0
                )

            FROM customers
            """
        )

        result = cursor.fetchone()

        total_customers = result[0]
        active_accounts = result[1]
        inactive_accounts = result[2]
        closed_accounts = result[3]
        total_balance = result[4]
        average_balance = result[5]

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
                float(total_balance),
                ".2f"
            )
        )

        print(
            "Average Balance      : ₹",
            format(
                float(average_balance),
                ".2f"
            )
        )

        print("\n========================================")

        input(
            "\nPress Enter to return..."
        )

    except psycopg2.Error as error:

        print("\n========================================")
        print("       DATABASE ERROR")
        print("========================================")

        print(
            "Database Error:",
            error
        )

        print("========================================")

        input(
            "\nPress Enter to return..."
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
#============================
#admin dashboard summary
#=========================

def admin_dashboard_summary():

    print("\n========================================")
    print("        BANKING SYSTEM SUMMARY")
    print("========================================")

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to connect to database.")

        input(
            "\nPress Enter to return..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # CUSTOMER + BALANCE SUMMARY
        # ========================================

        cursor.execute(
            """
            SELECT
                COUNT(*),

                COUNT(*) FILTER (
                    WHERE status = 'Active'
                ),

                COUNT(*) FILTER (
                    WHERE status = 'Inactive'
                ),

                COUNT(*) FILTER (
                    WHERE status = 'Closed'
                ),

                COALESCE(
                    SUM(balance),
                    0
                ),

                COALESCE(
                    AVG(balance),
                    0
                )

            FROM customers
            """
        )

        customer_data = cursor.fetchone()

        total_customers = customer_data[0]
        active_accounts = customer_data[1]
        inactive_accounts = customer_data[2]
        closed_accounts = customer_data[3]
        total_balance = customer_data[4]
        average_balance = customer_data[5]

        # ========================================
        # TRANSACTION SUMMARY
        # ========================================

        cursor.execute(
            """
            SELECT
                COUNT(*),

                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Deposit'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ),

                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Withdrawal'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ),

                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Transfer'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                )

            FROM transactions
            """
        )

        transaction_data = cursor.fetchone()

        total_transactions = transaction_data[0]
        total_deposits = transaction_data[1]
        total_withdrawals = transaction_data[2]
        total_transfers = transaction_data[3]

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
                float(total_balance),
                ".2f"
            )
        )

        print(
            "Average Customer Balance: ₹",
            format(
                float(average_balance),
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
                float(total_deposits),
                ".2f"
            )
        )

        print(
            "Total Withdrawals     : ₹",
            format(
                float(total_withdrawals),
                ".2f"
            )
        )

        print(
            "Total Transfers       : ₹",
            format(
                float(total_transfers),
                ".2f"
            )
        )

        print("\n========================================")

        input(
            "\nPress Enter to return..."
        )

    except psycopg2.Error as error:

        print("\n========================================")
        print("       DATABASE ERROR")
        print("========================================")

        print(
            "Database Error:",
            error
        )

        print("========================================")

        input(
            "\nPress Enter to return..."
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
# ========================================
# ADVANCED CUSTOMER SEARCH
# ========================================
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
    # VALIDATE CHOICE
    # ========================================

    if choice not in ["1", "2", "3", "4"]:

        print("\nInvalid choice.")

        return

    # ========================================
    # SEARCH VALUE
    # ========================================

    search_value = input(
        "\nEnter search value: "
    ).strip()

    if not search_value:

        print(
            "\nSearch value cannot be empty."
        )

        return

    # ========================================
    # ACCOUNT NUMBER VALIDATION
    # ========================================

    account_no = None

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

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to database."
        )

        input(
            "\nPress Enter to return..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # SEARCH BY ACCOUNT NUMBER
        # ========================================

        if choice == "1":

            cursor.execute(
                """
                SELECT
                    customer_id,
                    name,
                    account_no,
                    mobile,
                    email,
                    status,
                    balance
                FROM customers
                WHERE account_no = %s
                """,
                (account_no,)
            )

        # ========================================
        # SEARCH BY NAME
        # ========================================

        elif choice == "2":

            cursor.execute(
                """
                SELECT
                    customer_id,
                    name,
                    account_no,
                    mobile,
                    email,
                    status,
                    balance
                FROM customers
                WHERE name ILIKE %s
                ORDER BY name
                """,
                (
                    "%" + search_value + "%",
                )
            )

        # ========================================
        # SEARCH BY MOBILE NUMBER
        # ========================================

        elif choice == "3":

            cursor.execute(
                """
                SELECT
                    customer_id,
                    name,
                    account_no,
                    mobile,
                    email,
                    status,
                    balance
                FROM customers
                WHERE mobile = %s
                """,
                (search_value,)
            )

        # ========================================
        # SEARCH BY EMAIL
        # ========================================

        elif choice == "4":

            cursor.execute(
                """
                SELECT
                    customer_id,
                    name,
                    account_no,
                    mobile,
                    email,
                    status,
                    balance
                FROM customers
                WHERE LOWER(email) = LOWER(%s)
                """,
                (search_value,)
            )

        found_customers = cursor.fetchall()

        # ========================================
        # SEARCH TYPE FOR LOGGING
        # ========================================

        search_types = {
            "1": "Account Number",
            "2": "Name",
            "3": "Mobile Number",
            "4": "Email"
        }

        search_type = search_types.get(
            choice,
            "Unknown"
        )

        # ========================================
        # NO RESULTS
        # ========================================

        if not found_customers:

            print(
                "\nNo customers found."
            )

            log_admin_activity(
                "Advanced Customer Search",
                (
                    f"Admin searched customers by "
                    f"{search_type}: {search_value}, "
                    f"but no customers were found."
                )
            )

            input(
                "\nPress Enter to return..."
            )

            return

        # ========================================
        # DISPLAY RESULTS
        # ========================================

        print(
            "\n========================================"
        )

        print(
            "        SEARCH RESULTS"
        )

        print(
            "========================================"
        )

        for customer in found_customers:

            customer_id = customer[0]
            customer_name = customer[1]
            customer_account = customer[2]
            mobile = customer[3]
            email = customer[4]
            status = customer[5]
            balance = customer[6]

            print(
                "\n----------------------------------------"
            )

            print(
                "Name          :",
                customer_name
                if customer_name
                else "Not available"
            )

            print(
                "Account Number:",
                customer_account
                if customer_account
                else "Not available"
            )

            print(
                "Mobile        :",
                mobile
                if mobile
                else "Not available"
            )

            print(
                "Email         :",
                email
                if email
                else "Not available"
            )

            print(
                "Status        :",
                status
                if status
                else "Active"
            )

            # ====================================
            # BALANCE
            # ====================================

            try:

                print(
                    "Balance       : ₹",
                    format(
                        float(balance),
                        ".2f"
                    )
                )

            except (
                ValueError,
                TypeError
            ):

                print(
                    "Balance       :",
                    balance
                )

        print(
            "\n========================================"
        )

        print(
            "Customers Found:",
            len(found_customers)
        )

        print(
            "========================================"
        )

        # ========================================
        # ADMIN ACTIVITY LOG
        # ========================================

        log_admin_activity(
            "Advanced Customer Search",
            (
                f"Admin searched customers by "
                f"{search_type}: {search_value}. "
                f"{len(found_customers)} customer(s) found."
            )
        )

        # ========================================
        # RETURN
        # ========================================

        input(
            "\nPress Enter to return..."
        )

    except psycopg2.Error as error:

        print(
            "\n========================================"
        )

        print(
            "       DATABASE ERROR"
        )

        print(
            "========================================"
        )

        print(
            "Database Error:",
            error
        )

        print(
            "========================================"
        )

        input(
            "\nPress Enter to return..."
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
# ========================================
# ADMIN VIEW CUSTOMER DETAILS
# ========================================
def admin_view_customer_details():

    print("\n========================================")
    print("       CUSTOMER DETAILS")
    print("========================================")

    # ========================================
    # ACCOUNT NUMBER
    # ========================================

    try:

        account_no = int(
            input(
                "Enter Customer Account Number: "
            ).strip()
        )

    except ValueError:

        print(
            "\nAccount Number must be a number."
        )

        return

    # ========================================
    # DATABASE CONNECTION
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to database."
        )

        input(
            "\nPress Enter to return..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # FIND CUSTOMER
        # ========================================

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                account_no,
                mobile,
                mobile_verified,
                email,
                email_type,
                aadhaar_masked,
                balance,
                status
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )

        found_customer = cursor.fetchone()

        # ========================================
        # CUSTOMER NOT FOUND
        # ========================================

        if found_customer is None:

            print(
                "\nCustomer account not found."
            )

            log_admin_activity(
                "Admin View Customer Details",
                (
                    f"Admin attempted to view "
                    f"account {account_no}, but the "
                    f"customer account was not found."
                )
            )

            input(
                "\nPress Enter to return..."
            )

            return

        # ========================================
        # CUSTOMER DATA
        # ========================================

        customer_id = found_customer[0]
        customer_name = found_customer[1]
        customer_account = found_customer[2]
        mobile = found_customer[3]
        mobile_verified = found_customer[4]
        email = found_customer[5]
        email_type = found_customer[6]
        aadhaar_masked = found_customer[7]
        balance = found_customer[8]
        status = found_customer[9]

        # ========================================
        # CUSTOMER PROFILE
        # ========================================

        print("\n========================================")
        print("          CUSTOMER PROFILE")
        print("========================================")

        print(
            "Name             :",
            customer_name
            if customer_name
            else "Not available"
        )

        print(
            "Account Number   :",
            customer_account
            if customer_account
            else "Not available"
        )

        # ========================================
        # MASK MOBILE NUMBER
        # ========================================

        if mobile:

            mobile_string = str(mobile)

            if len(mobile_string) >= 4:

                masked_mobile = (
                    "XXXXXX"
                    + mobile_string[-4:]
                )

            else:

                masked_mobile = "XXXXXX"

        else:

            masked_mobile = "Not available"

        print(
            "Mobile Number    :",
            masked_mobile
        )

        # ========================================
        # MOBILE VERIFICATION
        # ========================================

        if mobile_verified:

            print(
                "Mobile Verified  : YES"
            )

        else:

            print(
                "Mobile Verified  : NO"
            )

        # ========================================
        # EMAIL
        # ========================================

        print(
            "Email            :",
            email
            if email
            else "Not available"
        )

        print(
            "Email Type       :",
            email_type
            if email_type
            else "Not available"
        )

        # ========================================
        # AADHAAR
        # ========================================

        if aadhaar_masked:

            masked_aadhaar = str(
                aadhaar_masked
            )

        else:

            masked_aadhaar = "Not available"

        print(
            "Aadhaar          :",
            masked_aadhaar
        )

        # ========================================
        # ACCOUNT STATUS
        # ========================================

        print(
            "Account Status   :",
            status
            if status
            else "Active"
        )

        # ========================================
        # BALANCE
        # ========================================

        try:

            print(
                "Balance          : ₹",
                format(
                    float(balance),
                    ".2f"
                )
            )

        except (
            ValueError,
            TypeError
        ):

            print(
                "Balance          :",
                balance
            )

        print(
            "========================================"
        )

        # ========================================
        # TRANSACTION HISTORY
        # ========================================

        cursor.execute(
            """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                status,
                date,
                sender_name,
                sender_account,
                receiver_name,
                receiver_account
            FROM transactions
            WHERE
                customer_id = %s
                OR sender_account = %s
                OR receiver_account = %s
            ORDER BY date ASC
            """,
            (
                customer_id,
                customer_account,
                customer_account
            )
        )

        transactions = cursor.fetchall()

        print("\n========================================")
        print("        TRANSACTION HISTORY")
        print("========================================")

        if not transactions:

            print(
                "\nNo transactions found."
            )

        else:

            for index, transaction in enumerate(
                transactions,
                start=1
            ):

                print(
                    "\nTransaction",
                    index
                )

                print(
                    "----------------------------------------"
                )

                # --------------------------------
                # TRANSACTION ID
                # --------------------------------

                print(
                    "Transaction ID :",
                    transaction[0]
                    if transaction[0]
                    else "Not available"
                )

                # --------------------------------
                # TYPE
                # --------------------------------

                transaction_type = transaction[1]

                # Display sent/received based on
                # the customer's account
                if transaction_type == "Transfer":

                    if transaction[7] == customer_account:

                        display_type = "Transfer Received"

                    elif transaction[6] == customer_account:

                        display_type = "Transfer Sent"

                    else:

                        display_type = "Transfer"

                else:

                    display_type = (
                        transaction_type
                        if transaction_type
                        else "Unknown"
                    )

                print(
                    "Type           :",
                    display_type
                )

                # --------------------------------
                # AMOUNT
                # --------------------------------

                amount = transaction[2]

                try:

                    print(
                        "Amount         : ₹",
                        format(
                            float(amount),
                            ".2f"
                        )
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    print(
                        "Amount         :",
                        amount
                    )

                # --------------------------------
                # STATUS
                # --------------------------------

                print(
                    "Status         :",
                    transaction[3]
                    if transaction[3]
                    else "SUCCESS"
                )

                # --------------------------------
                # DATE
                # --------------------------------

                print(
                    "Date & Time    :",
                    transaction[4]
                    if transaction[4]
                    else "Not available"
                )

                # --------------------------------
                # TRANSFER DETAILS
                # --------------------------------

                if transaction_type == "Transfer":

                    print(
                        "Sender Name    :",
                        transaction[5]
                        if transaction[5]
                        else "Not available"
                    )

                    print(
                        "Sender Account :",
                        transaction[6]
                        if transaction[6]
                        else "Not available"
                    )

                    print(
                        "Receiver Name  :",
                        transaction[7]
                        if transaction[7]
                        else "Not available"
                    )

                    print(
                        "Receiver Account:",
                        transaction[8]
                        if transaction[8]
                        else "Not available"
                    )

        # ========================================
        # SUMMARY
        # ========================================

        print(
            "\n========================================"
        )

        print(
            "Total Transactions:",
            len(transactions)
        )

        print(
            "========================================"
        )

        # ========================================
        # ADMIN ACTIVITY LOG
        # ========================================

        log_admin_activity(
            "Admin View Customer Details",
            (
                f"Admin viewed details of customer "
                f"{customer_name}, account "
                f"{account_no}. "
                f"Total transactions: "
                f"{len(transactions)}."
            )
        )

        # ========================================
        # RETURN
        # ========================================

        input(
            "\nPress Enter to return..."
        )

    except psycopg2.Error as error:

        print("\n========================================")
        print("       DATABASE ERROR")
        print("========================================")

        print(
            "Database Error:",
            error
        )

        print("========================================")

        input(
            "\nPress Enter to return...")

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
# ========================================
# VALIDATE TRANSACTION
# ========================================
def validate_transaction_by_id():

    # ========================================
    # VALIDATE TRANSACTION
    # ========================================

    print("\n========================================")
    print("        VALIDATE TRANSACTION")
    print("========================================")

    # ========================================
    # ENTER TRANSACTION ID
    # ========================================

    transaction_id = input(
        "\nEnter Transaction ID: "
    ).strip()

    if not transaction_id:

        print(
            "\nTransaction ID cannot be empty."
        )

        return

    # ========================================
    # DATABASE CONNECTION
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to PostgreSQL."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # SEARCH TRANSACTION IN POSTGRESQL
        # ========================================

        cursor.execute(
            """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                status,
                date,
                sender_name,
                sender_account,
                receiver_name,
                receiver_account
            FROM transactions
            WHERE transaction_id = %s
            """,
            (
                transaction_id,
            )
        )

        row = cursor.fetchone()

        # ========================================
        # TRANSACTION NOT FOUND
        # ========================================

        if row is None:

            print(
                "\nTransaction ID not found."
            )

            return

        # ========================================
        # CONVERT DATABASE ROW
        # INTO TRANSACTION DICTIONARY
        # ========================================

        transaction = {

            "transaction_id": row[0],

            "transaction_type": row[1],

            "amount": row[2],

            "status": row[3],

            "date": row[4],

            "sender_name": row[5],

            "sender_account": row[6],

            "receiver_name": row[7],

            "receiver_account": row[8]

        }

        # ========================================
        # VALIDATE TRANSACTION
        # ========================================

        is_valid = validate_transaction(
            transaction
        )

        # ========================================
        # DISPLAY TRANSACTION DETAILS
        # ========================================

        print(
            "\n========================================"
        )

        print(
            "       TRANSACTION DETAILS"
        )

        print(
            "========================================"
        )

        print(
            "Transaction ID :",
            transaction["transaction_id"]
        )

        print(
            "Transaction Type :",
            transaction["transaction_type"]
        )

        print(
            "Amount :",
            transaction["amount"]
        )

        print(
            "Status :",
            transaction["status"]
        )

        print(
            "Date & Time :",
            transaction["date"]
        )

        # ========================================
        # TRANSFER DETAILS
        # ========================================

        if transaction["transaction_type"] == "Transfer":

            print(
                "\nSender Details"
            )

            print(
                "Sender Name :",
                transaction["sender_name"]
            )

            print(
                "Sender Account :",
                transaction["sender_account"]
            )

            print(
                "\nReceiver Details"
            )

            print(
                "Receiver Name :",
                transaction["receiver_name"]
            )

            print(
                "Receiver Account :",
                transaction["receiver_account"]
            )

        # ========================================
        # VALIDATION RESULT
        # ========================================

        print(
            "\n========================================"
        )

        if is_valid:

            print(
                "TRANSACTION VALIDATION: SUCCESS"
            )

            print(
                "Transaction is valid."
            )

        else:

            print(
                "TRANSACTION VALIDATION: FAILED"
            )

            print(
                "Transaction is invalid."
            )

        print(
            "========================================"
        )

    except psycopg2.Error as error:

        print(
            "\nDatabase error while validating "
            "transaction."
        )

        print(
            "Database Error:",
            error
        )

    except Exception as error:

        print(
            "\nUnexpected error while validating "
            "transaction."
        )

        print(
            "Error:",
            error
        )

    finally:

        if cursor is not None:

            cursor.close()

        connection.close()
#=====================
#transaction id exists
#====================
def transaction_id_exists(transaction_id):

    connection = get_db_connection()

    if connection is None:
        return False

    cursor = None

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM transactions
            WHERE UPPER(TRIM(transaction_id)) =
                  UPPER(TRIM(%s))
            LIMIT 1
            """,
            (transaction_id,)
        )

        result = cursor.fetchone()

        if result is not None:
            return True

        return False

    except psycopg2.Error as error:

        print("\nDatabase error while checking Transaction ID.")
        print("Error:", error)

        return False

    except Exception as error:

        print("\nUnexpected error while checking Transaction ID.")
        print("Error:", error)

        return False

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()

# ========================================
# LOG ADMIN ACTIVITY
# ========================================
def log_admin_activity(
    action,
    details=""
):

    connection = get_db_connection()

    if connection is None:
        return False

    cursor = None

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO admin_activity
            (
                action,
                details,
                date
            )
            VALUES
            (
                %s,
                %s,
                CURRENT_TIMESTAMP
            )
            """,
            (
                action,
                details
            )
        )

        connection.commit()

        return True

    except psycopg2.Error as error:

        if connection is not None:
            connection.rollback()

        print(
            "\nDatabase error while saving admin activity."
        )

        print(
            "Error:",
            error
        )

        return False

    except Exception as error:

        if connection is not None:
            connection.rollback()

        print(
            "\nUnexpected error while saving admin activity."
        )

        print(
            "Error:",
            error
        )

        return False

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
# ========================================
# VIEW ADMIN ACTIVITY LOG
# ========================================
def view_admin_activity_log():

    print("\n========================================")
    print("          ADMIN ACTIVITY LOG")
    print("========================================")

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to connect to PostgreSQL.")
        print("========================================")

        input(
            "\nPress Enter to return..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # LOAD ACTIVITY LOG FROM POSTGRESQL
        # ========================================

        cursor.execute(
            """
            SELECT
                activity_id,
                action,
                details,
                date
            FROM admin_activity
            ORDER BY activity_id
            """
        )

        activities = cursor.fetchall()

        # ========================================
        # CHECK DATA
        # ========================================

        if not activities:

            print(
                "\nNo admin activity found."
            )

            print(
                "========================================"
            )

            input(
                "\nPress Enter to return..."
            )

            return

        # ========================================
        # DISPLAY ACTIVITIES
        # ========================================

        for index, activity in enumerate(
            activities,
            start=1
        ):

            activity_id = activity[0]
            action = activity[1]
            details = activity[2]
            activity_date = activity[3]

            print(
                f"\nActivity {index}"
            )

            print(
                "----------------------------------------"
            )

            print(
                "Activity ID:",
                activity_id
            )

            print(
                "Action     :",
                action
            )

            print(
                "Date       :",
                activity_date
            )

            print(
                "Details    :",
                details
            )

        # ========================================
        # TOTAL ACTIVITIES
        # ========================================

        print(
            "\n========================================"
        )

        print(
            "Total Activities:",
            len(activities)
        )

        print(
            "========================================"
        )

    except psycopg2.Error as error:

        print(
            "\nDatabase error while loading admin activity log."
        )

        print(
            "Error:",
            error
        )

        print(
            "========================================"
        )

    except Exception as error:

        print(
            "\nUnexpected error while loading admin activity log."
        )

        print(
            "Error:",
            error
        )

        print(
            "========================================"
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()

    input(
        "\nPress Enter to return..."
    )
#==============================
#VALIDATE TRANSACTION
#============================
def validate_transaction(transaction):

    valid_types = [
        "Deposit",
        "Initial Deposit",
        "Withdrawal",
        "Transfer"
    ]

    required_fields = [
        "transaction_id",
        "transaction_type",
        "amount",
        "status",
        "date"
    ]

    # Check required fields
    for field in required_fields:

        if field not in transaction:

            return False

    # Check transaction type
    if transaction["transaction_type"] not in valid_types:

        return False

    # Check amount
    try:

        amount = float(transaction["amount"])

        if amount <= 0:

            return False

    except (ValueError, TypeError):

        return False

    # Check status
    if transaction["status"] != "SUCCESS":

        return False

    # Transfer validation
    if transaction["transaction_type"] == "Transfer":

        sender_account = transaction.get("sender_account")
        receiver_account = transaction.get("receiver_account")

        if sender_account is None or receiver_account is None:

            return False

        if sender_account == receiver_account:

            return False

    return True
# ========================================
# ADMIN DASHBOARD
# ========================================

def admin_dashboard():

    global customers

    while True:

        print("\n========================================")
        print("             ADMIN DASHBOARD")
        print("========================================")

        print("1.  View All Customers")
        print("2.  Banking Statistics")
        print("3.  Search Customer")
        print("4.  Search Transactions")
        print("5.  Filter Transactions")
        print("6.  Search Transaction by ID")
        print("7.  Change Account Status")
        print("8.  Close Customer Account")
        print("9.  Banking Summary")
        print("10. Export All Transactions")
        print("11. Admin Transaction Statistics")
        print("12. Customer Statistics")
        print("13. Banking System Summary")
        print("14. Advanced Customer Search")
        print("15. Admin View Customer Details")
        print("16. Validate Transaction")
        print("17. Check Transaction ID")
        print("18. Check Customer Account Status")
        print("19. Backup Data")
        print("20. System Health Check")
        print("21. View Admin Activity Log")
        print("22. Logout")

        choice = input(
            "\nEnter your choice (1-22): "
        ).strip()

        # ========================================
        # 1. VIEW ALL CUSTOMERS
        # ========================================

        if choice == "1":

            view_all_customers()

        # ========================================
        # 2. TOTAL CUSTOMERS
        # ========================================

        elif choice == "2":

            banking_statistics()

        # ========================================
        # 3. SEARCH CUSTOMER
        # ========================================

        elif choice == "3":

            search_customer()

        # ========================================
        # 4. SEARCH TRANSACTIONS
        # ========================================

        elif choice == "4":

            search_transactions()

        # ========================================
        # 5. FILTER TRANSACTIONS
        # ========================================

        elif choice == "5":

            filter_transactions()

        # ========================================
        # 6. SEARCH TRANSACTION BY ID
        # ========================================

        elif choice == "6":

            search_transaction_by_id()

        # ========================================
        # 7. CHANGE ACCOUNT STATUS
        # ========================================

        elif choice == "7":

            change_account_status()

        # ========================================
        # 8. CLOSE CUSTOMER ACCOUNT
        # ========================================

        elif choice == "8":

            close_customer_account()

        # ========================================
        # 9. BANKING SUMMARY
        # ========================================

        elif choice == "9":

            banking_summary()

        # ========================================
        # 10. EXPORT ALL TRANSACTIONS
        # ========================================

        elif choice == "10":

            export_all_transactions()

        # ========================================
        # 11. ADMIN TRANSACTION STATISTICS
        # ========================================

        elif choice == "11":

            admin_transaction_statistics()

        # ========================================
        # 12. CUSTOMER STATISTICS
        # ========================================

        elif choice == "12":

            admin_customer_statistics()

        # ========================================
        # 13. BANKING SYSTEM SUMMARY
        # ========================================

        elif choice == "13":

            admin_dashboard_summary()

        # ========================================
        # 14. ADVANCED CUSTOMER SEARCH
        # ========================================

        elif choice == "14":

            advanced_customer_search()

        # ========================================
        # 15. ADMIN VIEW CUSTOMER DETAILS
        # ========================================

        elif choice == "15":

            admin_view_customer_details()

        # ========================================
        # 16. VALIDATE TRANSACTION
        # ========================================

        elif choice == "16":

            print(
                "\n========================================"
            )

            print(
                "        VALIDATE TRANSACTION"
            )

            print(
                "========================================"
            )

            transaction_id = input(
                "\nEnter Transaction ID: "
            ).strip().upper()

            # ------------------------------------
            # EMPTY ID
            # ------------------------------------

            if not transaction_id:

                print(
                    "\nTransaction ID cannot be empty."
                )

                continue

            connection = get_db_connection()

            if connection is None:

                print(
                    "\nUnable to connect to PostgreSQL."
                )

                continue

            cursor = None

            try:

                cursor = connection.cursor()

                # ------------------------------------
                # SEARCH TRANSACTION IN POSTGRESQL
                # ------------------------------------

                cursor.execute(
                    """
                    SELECT
                        transaction_id,
                        transaction_type,
                        amount,
                        status,
                        date,
                        sender_name,
                        sender_account,
                        receiver_name,
                        receiver_account
                    FROM transactions
                    WHERE UPPER(TRIM(transaction_id)) =
                        UPPER(TRIM(%s))
                    """,
                    (
                        transaction_id,
                    )
                )

                row = cursor.fetchone()

                # ------------------------------------
                # TRANSACTION NOT FOUND
                # ------------------------------------

                if row is None:

                    print(
                        "\nTransaction ID not found."
                    )

                    log_admin_activity(
                        "Validate Transaction",
                        (
                            f"Admin attempted to validate "
                            f"transaction ID {transaction_id}, "
                            f"but it was not found."
                        )
                    )

                    continue

                # ------------------------------------
                # CREATE TRANSACTION DICTIONARY
                # ------------------------------------

                found_transaction = {

                    "transaction_id":
                        row[0],

                    "transaction_type":
                        row[1],

                    "amount":
                        row[2],

                    "status":
                        row[3],

                    "date":
                        row[4],

                    "sender_name":
                        row[5],

                    "sender_account":
                        row[6],

                    "receiver_name":
                        row[7],

                    "receiver_account":
                        row[8]

                }

                # ------------------------------------
                # VALIDATE TRANSACTION
                # ------------------------------------

                is_valid = validate_transaction(
                    found_transaction
                )

                # ------------------------------------
                # VALID TRANSACTION
                # ------------------------------------

                if is_valid:

                    print(
                        "\n========================================"
                    )

                    print(
                        "       TRANSACTION IS VALID"
                    )

                    print(
                        "========================================"
                    )

                    print(
                        "Transaction ID :",
                        found_transaction[
                            "transaction_id"
                        ]
                    )

                    print(
                        "Type           :",
                        found_transaction[
                            "transaction_type"
                        ]
                    )

                    print(
                        "Amount         : ₹",
                        format(
                            float(
                                found_transaction[
                                    "amount"
                                ]
                            ),
                            ".2f"
                        )
                    )

                    print(
                        "Date & Time    :",
                        found_transaction[
                            "date"
                        ]
                    )

                    print(
                        "Database Status:",
                        found_transaction[
                            "status"
                        ]
                    )

                    # --------------------------------
                    # TRANSFER DETAILS
                    # --------------------------------

                    if found_transaction[
                        "transaction_type"
                    ] == "Transfer":

                        print(
                            "\nSender Name    :",
                            found_transaction[
                                "sender_name"
                            ]
                        )

                        print(
                            "Sender Account :",
                            found_transaction[
                                "sender_account"
                            ]
                        )

                        print(
                            "Receiver Name  :",
                            found_transaction[
                                "receiver_name"
                            ]
                        )

                        print(
                            "Receiver Account:",
                            found_transaction[
                                "receiver_account"
                            ]
                        )

                    print(
                        "Validation     : VALID"
                    )

                    print(
                        "========================================"
                    )

                    log_admin_activity(
                        "Validate Transaction",
                        (
                            f"Admin validated transaction "
                            f"ID {transaction_id}. "
                            f"Result: VALID."
                        )
                    )

                # ------------------------------------
                # INVALID TRANSACTION
                # ------------------------------------

                else:

                    print(
                        "\n========================================"
                    )

                    print(
                        "      TRANSACTION IS INVALID"
                    )

                    print(
                        "========================================"
                    )

                    print(
                        "Transaction ID :",
                        transaction_id
                    )

                    print(
                        "Validation     : INVALID"
                    )

                    print(
                        "========================================"
                    )

                    log_admin_activity(
                        "Validate Transaction",
                        (
                            f"Admin validated transaction "
                            f"ID {transaction_id}. "
                            f"Result: INVALID."
                        )
                    )

            except psycopg2.Error as error:

                print(
                    "\nDatabase error while validating "
                    "transaction."
                )

                print(
                    "Database Error:",
                    error
                )

                connection.rollback()

            except Exception as error:

                print(
                    "\nUnexpected error while validating "
                    "transaction."
                )

                print(
                    "Error:",
                    error
                )

            finally:

                if cursor is not None:

                    cursor.close()

                connection.close()

                print(
                    "========================================"
                )

        

        # ========================================
        # 17. CHECK TRANSACTION ID
        # ========================================

        elif choice == "17":

            print(
                "\n========================================"
            )

            print(
                "        CHECK TRANSACTION ID"
            )

            print(
                "========================================"
            )

            transaction_id = input(
                "\nEnter Transaction ID: "
            ).strip()

            # ------------------------------------
            # EMPTY ID
            # ------------------------------------

            if not transaction_id:

                print(
                    "\nTransaction ID cannot be empty."
                )

                continue

            # ------------------------------------
            # CHECK ID
            # ------------------------------------

            if transaction_id_exists(
                transaction_id
            ):

                print(
                    "\n========================================"
                )

                print(
                    "       TRANSACTION ID FOUND"
                )

                print(
                    "========================================"
                )

                print(
                    "Transaction ID:",
                    transaction_id
                )

                print(
                    "Status         : EXISTS"
                )

                print(
                    "========================================"
                )

                log_admin_activity(
                    "Check Transaction ID",
                    (
                        f"Admin checked transaction "
                        f"ID {transaction_id}. "
                        f"Result: Transaction ID exists."
                    )
                )

            else:

                print(
                    "\n========================================"
                )

                print(
                    "       TRANSACTION ID NOT FOUND"
                )

                print(
                    "========================================"
                )

                print(
                    "Transaction ID:",
                    transaction_id
                )

                print(
                    "Status         : DOES NOT EXIST"
                )

                print(
                    "========================================"
                )

                log_admin_activity(
                    "Check Transaction ID",
                    (
                        f"Admin checked transaction "
                        f"ID {transaction_id}. "
                        f"Result: Transaction ID does not exist."
                    )
                )

        # ========================================
        # 18. CHECK CUSTOMER ACCOUNT STATUS
        # ========================================

        elif choice == "18":

            print(
                "\n========================================"
            )

            print(
                "     CHECK CUSTOMER ACCOUNT STATUS"
            )

            print(
                "========================================"
            )

            try:

                account_no = int(
                    input(
                        "\nEnter Account Number: "
                    ).strip()
                )

            except ValueError:

                print(
                    "\nAccount Number must be a number."
                )

                continue

            connection = get_db_connection()

            if connection is None:

                print(
                    "\nUnable to connect to database."
                )

                continue

            cursor = None

            try:

                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT
                        name,
                        account_no,
                        status
                    FROM customers
                    WHERE account_no = %s
                    """,
                    (account_no,)
                )

                customer = cursor.fetchone()

                # ------------------------------------
                # ACCOUNT NOT FOUND
                # ------------------------------------

                if customer is None:

                    print(
                        "\nAccount not found."
                    )

                    log_admin_activity(
                        "Check Customer Account Status",
                        (
                            f"Admin checked account "
                            f"{account_no}, but the account "
                            f"was not found."
                        )
                    )

                    continue

                # ------------------------------------
                # ACCOUNT STATUS
                # ------------------------------------

                customer_name = customer[0]
                customer_account = customer[1]
                account_status = customer[2]

                print(
                    "\nCustomer Name :",
                    customer_name
                )

                print(
                    "Account Number:",
                    customer_account
                )

                print(
                    "Account Status:",
                    account_status
                )

                print(
                    "========================================"
                )

                log_admin_activity(
                    "Check Customer Account Status",
                    (
                        f"Admin checked account "
                        f"{account_no}. "
                        f"Current status: {account_status}."
                    )
                )

            except psycopg2.Error as error:

                print(
                    "\nDatabase error while checking account status."
                )

                print(
                    "Error:",
                    error
                )

            except Exception as error:

                print(
                    "\nUnexpected error while checking account status."
                )

                print(
                    "Error:",
                    error
                )

            finally:

                if cursor is not None:
                    cursor.close()

                connection.close()

        # ========================================
        # 19. BACKUP DATA
        # ========================================

        elif choice == "19":

            backup_data()

        # ========================================
        # 20. SYSTEM HEALTH CHECK
        # ========================================

        elif choice == "20":

            system_health_check()

        # ========================================
        # 21. VIEW ADMIN ACTIVITY LOG
        # ========================================

        elif choice == "21":

            view_admin_activity_log()

        # ========================================
        # 21. LOGOUT
        # ========================================

        elif choice == "22":

            print(
                "\nAdmin logged out successfully."
            )

            break

        # ========================================
        # INVALID CHOICE
        # ========================================

        else:

            print(
                "\nInvalid choice!"
                " Please enter a number from 1 to 21."
            )


#==============================
#CHANGE PASSWORD
#==============================
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

    # ========================================
    # GET CURRENT PASSWORD HASH
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to connect to database.")
        return

    cursor = None

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT password_hash
            FROM customers
            WHERE account_no = %s
            """,
            (
                customer.get("account_no"),
            )
        )

        result = cursor.fetchone()

        if result is None:

            print("\nCustomer account not found.")
            return

        stored_password_hash = result[0]

        # ====================================
        # VERIFY CURRENT PASSWORD
        # ====================================

        current_password_hash = hash_password(
            current_password
        )

        if current_password_hash != stored_password_hash:

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

        # ========================================
        # PASSWORD LENGTH
        # ========================================

        if len(new_password) < 4:

            print(
                "\nPassword must contain at least "
                "4 characters."
            )

            return

        # ========================================
        # HASH NEW PASSWORD
        # ========================================

        new_password_hash = hash_password(
            new_password
        )

        # ========================================
        # CHECK SAME PASSWORD
        # ========================================

        if new_password_hash == stored_password_hash:

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
        # UPDATE PASSWORD IN POSTGRESQL
        # ========================================

        cursor.execute(
            """
            UPDATE customers
            SET password_hash = %s
            WHERE account_no = %s
            """,
            (
                new_password_hash,
                customer.get("account_no")
            )
        )

        # ========================================
        # COMMIT
        # ========================================

        connection.commit()

        # ========================================
        # UPDATE IN-MEMORY CUSTOMER
        # ========================================

        customer["password"] = new_password_hash

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

    except psycopg2.Error as error:

        connection.rollback()

        print("\n========================================")
        print("      PASSWORD CHANGE FAILED")
        print("========================================")

        print(
            "The password could not be changed."
        )

        print(
            "Database Error:",
            error
        )

        print("========================================")

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
# ========================================
# ACCOUNT STATEMENT
# ========================================
def account_statement(customer):

    print("\n========================================")
    print("          ACCOUNT STATEMENT")
    print("========================================")

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to load account statement.")
        print("========================================")

        input("\nPress Enter to return...")

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # GET ACCOUNT DETAILS
        # ========================================

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                account_no,
                balance,
                status
            FROM customers
            WHERE account_no = %s
            """,
            (
                customer.get("account_no"),
            )
        )

        customer_result = cursor.fetchone()

        if customer_result is None:

            print("\nCustomer account not found.")
            print("========================================")

            input("\nPress Enter to return...")

            return

        (
            customer_id,
            customer_name,
            account_no,
            current_balance,
            account_status
        ) = customer_result

        current_balance = to_decimal(
            current_balance
        )

        # ========================================
        # ACCOUNT DETAILS
        # ========================================

        print(
            "Customer Name  :",
            customer_name
        )

        print(
            "Account Number :",
            account_no
        )

        print(
            "Account Status :",
            account_status
        )

        print(
            "Current Balance: ₹",
            format(
                current_balance,
                ".2f"
            )
        )

        # ========================================
        # TRANSACTIONS
        # ========================================

        print("\n========================================")
        print("        TRANSACTION STATEMENT")
        print("========================================")

        cursor.execute(
            """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                date,
                status
            FROM transactions
            WHERE
                customer_id = %s
                OR sender_account = %s
                OR receiver_account = %s
            ORDER BY date ASC
            """,
            (
                customer_id,
                account_no,
                account_no
            )
        )

        transactions = cursor.fetchall()

        # ========================================
        # NO TRANSACTIONS
        # ========================================

        if len(transactions) == 0:

            print(
                "\nNo transactions found."
            )

            print(
                "========================================"
            )

            input(
                "\nPress Enter to return..."
            )

            return

        # ========================================
        # DISPLAY TRANSACTIONS
        # ========================================

        valid_transaction_count = 0

        for index, transaction in enumerate(
            transactions,
            start=1
        ):

            (
                transaction_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                transaction_date,
                status
            ) = transaction

            valid_transaction_count += 1

            print(
                f"\nTransaction {index}"
            )

            print(
                "----------------------------------------"
            )

            # ====================================
            # TRANSACTION ID
            # ====================================

            print(
                "Transaction ID :",
                transaction_id
            )

            # ====================================
            # DATE & TIME
            # ====================================

            if transaction_date is not None:

                print(
                    "Date & Time    :",
                    transaction_date.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

            else:

                print(
                    "Date & Time    :",
                    "Date not available"
                )

            # ====================================
            # TYPE
            # ====================================

            display_type = transaction_type

            if transaction_type == "Transfer":

                if sender_account == account_no:

                    display_type = "Transfer Sent"

                elif receiver_account == account_no:

                    display_type = "Transfer Received"

            print(
                "Type           :",
                display_type
            )

            # ====================================
            # AMOUNT
            # ====================================

            try:

                amount_decimal = to_decimal(
                    amount
                )

                print(
                    "Amount         : ₹",
                    format(
                        amount_decimal,
                        ".2f"
                    )
                )

            except (
                ValueError,
                TypeError,
                InvalidOperation
            ):

                print(
                    "Amount         :",
                    amount
                )

            # ====================================
            # TRANSFER DETAILS
            # ====================================

            if transaction_type == "Transfer":

                # --------------------------------
                # TRANSFER SENT
                # --------------------------------

                if sender_account == account_no:

                    print(
                        "Receiver Name  :",
                        receiver_name
                    )

                    print(
                        "Receiver Account:",
                        receiver_account
                    )

                # --------------------------------
                # TRANSFER RECEIVED
                # --------------------------------

                elif receiver_account == account_no:

                    print(
                        "Sender Name    :",
                        sender_name
                    )

                    print(
                        "Sender Account :",
                        sender_account
                    )

            # ====================================
            # STATUS
            # ====================================

            print(
                "Status         :",
                status
            )

            print(
                "----------------------------------------"
            )

        # ========================================
        # SUMMARY
        # ========================================

        print(
            "\nTotal Transactions:",
            valid_transaction_count
        )

        print(
            "Current Balance   : ₹",
            format(
                current_balance,
                ".2f"
            )
        )

        print(
            "========================================"
        )

        input(
            "\nPress Enter to return..."
        )

    except psycopg2.Error as error:

        print(
            "\nUnable to load account statement."
        )

        print(
            "Database Error:",
            error
        )

        print(
            "========================================"
        )

        input(
            "\nPress Enter to return..."
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
# ========================================
# CUSTOMER TRANSACTION SEARCH
# ========================================

def customer_transaction_search(customer):

    print("\n========================================")
    print("       TRANSACTION SEARCH")
    print("========================================")

    transactions = customer.get(
        "transactions",
        []
    )

    if not isinstance(transactions, list) or not transactions:

        print("\nNo transactions found.")
        print("========================================")

        input("\nPress Enter to return...")

        return

    while True:

        print("\n========================================")
        print("       SEARCH TRANSACTIONS")
        print("========================================")

        print("1. Search by Transaction ID")
        print("2. Search by Transaction Type")
        print("3. Search by Date")
        print("4. View All Transactions")
        print("5. Back")

        choice = input(
            "\nEnter your choice (1-5): "
        ).strip()

        # ========================================
        # SEARCH BY TRANSACTION ID
        # ========================================

        if choice == "1":

            search_id = input(
                "\nEnter Transaction ID: "
            ).strip().upper()

            found = False

            for transaction in transactions:

                if not isinstance(transaction, dict):
                    continue

                transaction_id = str(
                    transaction.get(
                        "transaction_id",
                        ""
                    )
                ).upper()

                if transaction_id == search_id:

                    print("\n========================================")
                    print("       TRANSACTION FOUND")
                    print("========================================")

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
                            float(
                                transaction.get(
                                    "amount",
                                    0
                                )
                            ),
                            ".2f"
                        )
                    )

                    print(
                        "Date & Time    :",
                        transaction.get(
                            "date",
                            "Not available"
                        )
                    )

                    print(
                        "Status         :",
                        transaction.get(
                            "status",
                            "SUCCESS"
                        )
                    )

                    found = True

                    break

            if not found:

                print(
                    "\nTransaction ID not found."
                )

            print("========================================")

        # ========================================
        # SEARCH BY TRANSACTION TYPE
        # ========================================

        elif choice == "2":

            print("\nTransaction Types:")
            print("1. Initial Deposit")
            print("2. Deposit")
            print("3. Withdrawal")
            print("4. Transfer Sent")
            print("5. Transfer Received")

            type_choice = input(
                "\nEnter your choice (1-5): "
            ).strip()

            transaction_types = {

                "1": "Initial Deposit",
                "2": "Deposit",
                "3": "Withdrawal",
                "4": "Transfer Sent",
                "5": "Transfer Received"

            }

            if type_choice not in transaction_types:

                print(
                    "\nInvalid transaction type."
                )

                continue

            selected_type = transaction_types[
                type_choice
            ]

            found = False

            print("\n========================================")
            print(
                "TRANSACTIONS:",
                selected_type
            )
            print("========================================")

            for transaction in transactions:

                if not isinstance(transaction, dict):
                    continue

                if transaction.get(
                    "type"
                ) == selected_type:

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
                            float(
                                transaction.get(
                                    "amount",
                                    0
                                )
                            ),
                            ".2f"
                        )
                    )

                    print(
                        "Date & Time    :",
                        transaction.get(
                            "date",
                            "Not available"
                        )
                    )

                    print(
                        "Status         :",
                        transaction.get(
                            "status",
                            "SUCCESS"
                        )
                    )

                    found = True

            if not found:

                print(
                    "\nNo transactions found "
                    "for this type."
                )

            print("----------------------------------------")

        # ========================================
        # SEARCH BY DATE
        # ========================================

        elif choice == "3":

            search_date = input(
                "\nEnter date (YYYY-MM-DD): "
            ).strip()

            try:

                datetime.strptime(
                    search_date,
                    "%Y-%m-%d"
                )

            except ValueError:

                print(
                    "\nInvalid date format."
                )

                print(
                    "Please use YYYY-MM-DD."
                )

                continue

            found = False

            print("\n========================================")
            print(
                "TRANSACTIONS ON:",
                search_date
            )
            print("========================================")

            for transaction in transactions:

                if not isinstance(transaction, dict):
                    continue

                transaction_date = str(
                    transaction.get(
                        "date",
                        ""
                    )
                )

                if transaction_date.startswith(
                    search_date
                ):

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
                            float(
                                transaction.get(
                                    "amount",
                                    0
                                )
                            ),
                            ".2f"
                        )
                    )

                    print(
                        "Date & Time    :",
                        transaction.get(
                            "date",
                            "Not available"
                        )
                    )

                    print(
                        "Status         :",
                        transaction.get(
                            "status",
                            "SUCCESS"
                        )
                    )

                    found = True

            if not found:

                print(
                    "\nNo transactions found "
                    "on this date."
                )

            print("----------------------------------------")

        # ========================================
        # VIEW ALL
        # ========================================

        elif choice == "4":

            transaction_history(
                customer
            )

        # ========================================
        # BACK
        # ========================================

        elif choice == "5":

            print(
                "\nReturning to customer dashboard..."
            )

            break

        else:

            print(
                "\nInvalid choice! "
                "Please select 1-5."
            )


#============================
#verify mobile otp
#===========================

def verify_mobile_otp(customer, save_changes=True):

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

            if save_changes:
                save_customers()

            print("\n========================================")
            print("       MOBILE VERIFIED SUCCESSFULLY")
            print("========================================")

            masked_mobile = "XXXXXX" + mobile[-4:]

            print(
                "Mobile Number  :",
                masked_mobile
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



# ========================================
# FILTER TRANSACTION BY DATE
# ========================================

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

    # ========================================
    # VALIDATE DATE FORMAT
    # ========================================

    try:

        datetime.strptime(
            date_input,
            "%Y-%m-%d"
        )

    except ValueError:

        print("\nInvalid date format.")
        print("Please use YYYY-MM-DD.")
        return

    # ========================================
    # CONNECT TO POSTGRESQL
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to connect to PostgreSQL.")
        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # GET CUSTOMER ID
        # ========================================

        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE account_no = %s
            """,
            (
                customer.get("account_no"),
            )
        )

        customer_result = cursor.fetchone()

        if customer_result is None:

            print("\nCustomer account not found.")
            return

        customer_id = customer_result[0]

        account_no = customer.get(
            "account_no"
        )
        print("\nDEBUG ACCOUNT NUMBER:", account_no)
        print("DEBUG CUSTOMER ID:", customer_id)

        # ========================================
        # GET TRANSACTIONS FOR SELECTED DATE
        # ========================================

        cursor.execute(
            """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                date,
                status
            FROM transactions
            WHERE DATE(date) = %s
              AND (
                    customer_id = %s
                    OR sender_account = %s
                    OR receiver_account = %s
              )
            ORDER BY date ASC
            """,
            (
                date_input,
                customer_id,
                account_no,
                account_no
            )
        )

        # IMPORTANT:
        # Fetch the transactions returned by PostgreSQL.

        transactions = cursor.fetchall()

        # ========================================
        # NO TRANSACTIONS
        # ========================================

        if not transactions:

            print(
                "\nNo transactions found "
                "for this date."
            )

            print(
                "\n========================================"
            )

            input(
                "\nPress Enter to return..."
            )

            return

        # ========================================
        # DISPLAY TRANSACTIONS
        # ========================================

        for index, transaction in enumerate(
            transactions,
            start=1
        ):

            (
                transaction_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                transaction_date,
                status
            ) = transaction

            # ====================================
            # DETERMINE DISPLAY TYPE
            # ====================================

            display_type = transaction_type

            if transaction_type == "Transfer":

                if sender_account == account_no:

                    display_type = "Transfer Sent"

                elif receiver_account == account_no:

                    display_type = "Transfer Received"

            # ====================================
            # DISPLAY TRANSACTION
            # ====================================

            print(
                f"\nTransaction {index}"
            )

            print(
                "----------------------------------------"
            )

            print(
                "Transaction ID :",
                transaction_id
            )

            print(
                "Type           :",
                display_type
            )

            print(
                "Amount         : ₹",
                format(
                    to_decimal(amount),
                    ".2f"
                )
            )

            print(
                "Status         :",
                status
            )

            if transaction_date is not None:

                print(
                    "Date & Time    :",
                    transaction_date.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

            else:

                print(
                    "Date & Time    :",
                    "Date not available"
                )

            # ====================================
            # TRANSFER DETAILS
            # ====================================

            if transaction_type == "Transfer":

                if sender_account == account_no:

                    print(
                        "Receiver Name  :",
                        receiver_name
                    )

                    print(
                        "Receiver Account:",
                        receiver_account
                    )

                elif receiver_account == account_no:

                    print(
                        "Sender Name    :",
                        sender_name
                    )

                    print(
                        "Sender Account :",
                        sender_account
                    )

        # ========================================
        # END
        # ========================================

        print(
            "\n========================================"
        )

        input(
            "\nPress Enter to return..."
        )

    except psycopg2.Error as error:

        print(
            "\nUnable to filter transactions."
        )

        print(
            "Database Error:",
            error
        )

        print(
            "========================================"
        )

        input(
            "\nPress Enter to return..."
        )

    except Exception as error:

        print(
            "\nUnexpected error while filtering transactions."
        )

        print(
            "Error:",
            error
        )

        print(
            "========================================"
        )

        input(
            "\nPress Enter to return..."
        )

    finally:

        if cursor is not None:

            cursor.close()

        connection.close()
#========================
#filter transactions by date range
#==========================
def filter_transactions_by_date_range(customer):

    print("\n========================================")
    print("       TRANSACTION DATE RANGE FILTER")
    print("========================================")

    from_date_input = input(
        "\nEnter From Date (YYYY-MM-DD): "
    ).strip()

    if not from_date_input:

        print("\nFrom date cannot be empty.")

        input(
            "\nPress Enter to return..."
        )

        return

    to_date_input = input(
        "Enter To Date (YYYY-MM-DD): "
    ).strip()

    if not to_date_input:

        print("\nTo date cannot be empty.")

        input(
            "\nPress Enter to return..."
        )

        return

    # ========================================
    # VALIDATE FROM DATE
    # ========================================

    try:

        from_date = datetime.strptime(
            from_date_input,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        print("\nInvalid From Date format.")
        print("Please use YYYY-MM-DD.")

        input(
            "\nPress Enter to return..."
        )

        return

    # ========================================
    # VALIDATE TO DATE
    # ========================================

    try:

        to_date = datetime.strptime(
            to_date_input,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        print("\nInvalid To Date format.")
        print("Please use YYYY-MM-DD.")

        input(
            "\nPress Enter to return..."
        )

        return

    # ========================================
    # CHECK DATE RANGE
    # ========================================

    if from_date > to_date:

        print(
            "\nFrom date cannot be later than "
            "To date."
        )

        input(
            "\nPress Enter to return..."
        )

        return

    # ========================================
    # CONNECT TO POSTGRESQL
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to PostgreSQL."
        )

        input(
            "\nPress Enter to return..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # GET CUSTOMER ID
        # ========================================

        cursor.execute(
            """
            SELECT
                customer_id
            FROM customers
            WHERE account_no = %s
            """,
            (
                customer.get("account_no"),
            )
        )

        customer_result = cursor.fetchone()

        if customer_result is None:

            print(
                "\nCustomer account not found."
            )

            input(
                "\nPress Enter to return..."
            )

            return

        customer_id = customer_result[0]

        account_no = customer.get(
            "account_no"
        )

        # ========================================
        # GET TRANSACTIONS
        # ========================================

        cursor.execute(
            """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                date,
                status
            FROM transactions
            WHERE
                DATE(date) BETWEEN %s AND %s
                AND (
                    customer_id = %s
                    OR sender_account = %s
                    OR receiver_account = %s
                )
            ORDER BY date ASC
            """,
            (
                from_date,
                to_date,
                customer_id,
                account_no,
                account_no
            )
        )

        transactions = cursor.fetchall()

        # ========================================
        # NO TRANSACTIONS
        # ========================================

        if not transactions:

            print(
                "\nNo transactions found "
                "between "
                f"{from_date_input} "
                "and "
                f"{to_date_input}."
            )

            print(
                "\n========================================"
            )

            input(
                "\nPress Enter to return..."
            )

            return

        # ========================================
        # DISPLAY SUMMARY
        # ========================================

        print(
            "\n========================================"
        )

        print(
            "Transactions from",
            from_date_input,
            "to",
            to_date_input
        )

        print(
            "========================================"
        )

        # ========================================
        # DISPLAY TRANSACTIONS
        # ========================================

        for index, transaction in enumerate(
            transactions,
            start=1
        ):

            (
                transaction_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                transaction_date,
                status
            ) = transaction

            # ====================================
            # DETERMINE DISPLAY TYPE
            # ====================================

            display_type = transaction_type

            if transaction_type == "Transfer":

                if sender_account == account_no:

                    display_type = "Transfer Sent"

                elif receiver_account == account_no:

                    display_type = "Transfer Received"

            # ====================================
            # DISPLAY TRANSACTION
            # ====================================

            print(
                f"\nTransaction {index}"
            )

            print(
                "----------------------------------------"
            )

            print(
                "Transaction ID :",
                transaction_id
            )

            print(
                "Type           :",
                display_type
            )

            print(
                "Amount         : ₹",
                format(
                    to_decimal(amount),
                    ".2f"
                )
            )

            print(
                "Status         :",
                status
            )

            if transaction_date is not None:

                print(
                    "Date & Time    :",
                    transaction_date.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

            else:

                print(
                    "Date & Time    :",
                    "Date not available"
                )

            # ====================================
            # TRANSFER DETAILS
            # ====================================

            if transaction_type == "Transfer":

                if sender_account == account_no:

                    print(
                        "Receiver Name  :",
                        receiver_name
                    )

                    print(
                        "Receiver Account:",
                        receiver_account
                    )

                elif receiver_account == account_no:

                    print(
                        "Sender Name    :",
                        sender_name
                    )

                    print(
                        "Sender Account :",
                        sender_account
                    )

        # ========================================
        # END
        # ========================================

        print(
            "\n========================================"
        )

        print(
            "Total Transactions:",
            len(transactions)
        )

        print(
            "========================================"
        )

        input(
            "\nPress Enter to return..."
        )

    except psycopg2.Error as error:

        print(
            "\nUnable to filter transactions."
        )

        print(
            "Database Error:",
            error
        )

        print(
            "========================================"
        )

        input(
            "\nPress Enter to return..."
        )

    except Exception as error:

        print(
            "\nUnexpected error while filtering "
            "transactions."
        )

        print(
            "Error:",
            error
        )

        print(
            "========================================"
        )

        input(
            "\nPress Enter to return..."
        )

    finally:

        if cursor is not None:

            cursor.close()

        connection.close()
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

    # ========================================
    # VALIDATE CHOICE
    # ========================================

    if choice not in ("1", "2"):

        print("\nInvalid choice.")

        return

    # ========================================
    # DATABASE CONNECTION
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to PostgreSQL."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ====================================
        # GET CUSTOMER ID
        # ====================================

        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE account_no = %s
            """,
            (
                customer.get("account_no"),
            )
        )

        customer_result = cursor.fetchone()

        if customer_result is None:

            print("\nCustomer account not found.")

            return

        customer_id = customer_result[0]

        account_no = customer.get(
            "account_no"
        )

        # ====================================
        # SORT NEWEST TO OLDEST
        # ====================================

        if choice == "1":

            cursor.execute(
                """
                SELECT
                    transaction_id,
                    transaction_type,
                    amount,
                    sender_account,
                    receiver_account,
                    sender_name,
                    receiver_name,
                    date,
                    status
                FROM transactions
                WHERE
                    customer_id = %s
                    OR sender_account = %s
                    OR receiver_account = %s
                ORDER BY date DESC
                """,
                (
                    customer_id,
                    account_no,
                    account_no
                )
            )

            title = "NEWEST TO OLDEST"

        # ====================================
        # SORT OLDEST TO NEWEST
        # ====================================

        else:

            cursor.execute(
                """
                SELECT
                    transaction_id,
                    transaction_type,
                    amount,
                    sender_account,
                    receiver_account,
                    sender_name,
                    receiver_name,
                    date,
                    status
                FROM transactions
                WHERE
                    customer_id = %s
                    OR sender_account = %s
                    OR receiver_account = %s
                ORDER BY date ASC
                """,
                (
                    customer_id,
                    account_no,
                    account_no
                )
            )

            title = "OLDEST TO NEWEST"

        transactions = cursor.fetchall()

        # ====================================
        # CHECK TRANSACTIONS
        # ====================================

        if not transactions:

            print("\nNo transactions found.")

            return

        # ====================================
        # DISPLAY
        # ====================================

        print("\n========================================")
        print(
            "       TRANSACTIONS -",
            title
        )
        print("========================================")

        for transaction in transactions:

            print(
                "\n----------------------------------------"
            )

            (
                transaction_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                transaction_date,
                status
            ) = transaction

            # =================================
            # DETERMINE TRANSFER TYPE
            # =================================

            display_type = transaction_type

            if transaction_type == "Transfer":

                if sender_account == account_no:

                    display_type = "Transfer Sent"

                elif receiver_account == account_no:

                    display_type = "Transfer Received"

            # =================================
            # DISPLAY TRANSACTION
            # =================================

            print(
                "Transaction ID :",
                transaction_id
            )

            print(
                "Type           :",
                display_type
            )

            print(
                "Amount         : ₹",
                format(
                    amount,
                    ".2f"
                )
            )

            # =================================
            # TRANSFER DETAILS
            # =================================

            if transaction_type == "Transfer":

                if sender_account == account_no:

                    print(
                        "Receiver       :",
                        receiver_name
                    )

                    print(
                        "Receiver Acct  : XXXX",
                        str(receiver_account)[-4:]
                    )

                elif receiver_account == account_no:

                    print(
                        "Sender         :",
                        sender_name
                    )

                    print(
                        "Sender Acct    : XXXX",
                        str(sender_account)[-4:]
                    )

            print(
                "Status         :",
                status
            )

            print(
                "Date & Time    :",
                transaction_date
            )

        print(
            "\n========================================"
        )

    except psycopg2.Error as error:

        print(
            "\nDatabase error while "
            "sorting transactions."
        )

        print(
            "Database Error:",
            error
        )

    finally:

        if cursor:

            cursor.close()

        connection.close()

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

    if not start_date_input:

        print("\nStart date cannot be empty.")

        return

    # ========================================
    # GET END DATE
    # ========================================

    end_date_input = input(
        "Enter End Date (YYYY-MM-DD): "
    ).strip()

    if not end_date_input:

        print("\nEnd date cannot be empty.")

        return

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

    # ========================================
    # DATABASE CONNECTION
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to PostgreSQL."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ====================================
        # GET CUSTOMER ID
        # ====================================

        cursor.execute(
            """
            SELECT
                customer_id
            FROM customers
            WHERE account_no = %s
            """,
            (
                customer.get("account_no"),
            )
        )

        customer_result = cursor.fetchone()

        if customer_result is None:

            print(
                "\nCustomer account not found."
            )

            return

        customer_id = customer_result[0]

        account_no = customer.get(
            "account_no"
        )

        # ====================================
        # GET TRANSACTIONS
        # ====================================

        cursor.execute(
            """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                date,
                status
            FROM transactions
            WHERE
                (
                    customer_id = %s
                    OR sender_account = %s
                    OR receiver_account = %s
                )
                AND DATE(date) BETWEEN %s AND %s
            ORDER BY date ASC
            """,
            (
                customer_id,
                account_no,
                account_no,
                start_date,
                end_date
            )
        )

        transactions = cursor.fetchall()

        # ====================================
        # DISPLAY HEADER
        # ====================================

        print(
            "\n========================================"
        )

        print(
            "       FILTERED TRANSACTIONS"
        )

        print(
            "========================================"
        )

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

        print(
            "========================================"
        )

        # ====================================
        # DISPLAY MATCHING TRANSACTIONS
        # ====================================

        found = False

        for transaction in transactions:

            (
                transaction_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                transaction_date,
                status
            ) = transaction

            # =================================
            # DETERMINE DISPLAY TYPE
            # =================================

            display_type = transaction_type

            if transaction_type == "Transfer":

                if sender_account == account_no:

                    display_type = "Transfer Sent"

                elif receiver_account == account_no:

                    display_type = "Transfer Received"

            # =================================
            # TYPE CHECK
            # =================================

            if (
                selected_type is not None
                and display_type != selected_type
            ):

                continue

            found = True

            # =================================
            # DISPLAY TRANSACTION
            # =================================

            print(
                "\n----------------------------------------"
            )

            print(
                "Transaction ID :",
                transaction_id
            )

            print(
                "Type           :",
                display_type
            )

            print(
                "Amount         : ₹",
                format(
                    to_decimal(amount),
                    ".2f"
                )
            )

            print(
                "Status         :",
                status
            )

            if transaction_date is not None:

                print(
                    "Date & Time    :",
                    transaction_date.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

            else:

                print(
                    "Date & Time    :",
                    "Date not available"
                )

            # =================================
            # TRANSFER DETAILS
            # =================================

            if transaction_type == "Transfer":

                if sender_account == account_no:

                    print(
                        "Receiver Name  :",
                        receiver_name
                    )

                    print(
                        "Receiver Account:",
                        "XXXX"
                        + str(receiver_account)[-4:]
                        if receiver_account
                        else "Not available"
                    )

                elif receiver_account == account_no:

                    print(
                        "Sender Name    :",
                        sender_name
                    )

                    print(
                        "Sender Account :",
                        "XXXX"
                        + str(sender_account)[-4:]
                        if sender_account
                        else "Not available"
                    )

        # ====================================
        # NO RESULTS
        # ====================================

        if not found:

            print(
                "\nNo transactions found "
                "for the selected filter."
            )

        # ====================================
        # END
        # ====================================

        print(
            "\n========================================"
        )

    except psycopg2.Error as error:

        print(
            "\nDatabase error while "
            "filtering transactions."
        )

        print(
            "Database Error:",
            error
        )

    except Exception as error:

        print(
            "\nUnexpected error while "
            "filtering transactions."
        )

        print(
            "Error:",
            error
        )

    finally:

        if cursor is not None:

            cursor.close()

        connection.close()

    input(
        "\nPress Enter to return..."
    )
#====================================
# transaction summary
#===================================
def customer_transaction_summary(customer):

    print("\n========================================")
    print("       TRANSACTION SUMMARY")
    print("========================================")

    # ========================================
    # DATABASE CONNECTION
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to PostgreSQL."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        account_no = customer.get(
            "account_no"
        )

        # ====================================
        # GET CUSTOMER DETAILS
        # ====================================

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                account_no,
                status,
                balance
            FROM customers
            WHERE account_no = %s
            """,
            (
                account_no,
            )
        )

        customer_result = cursor.fetchone()

        if customer_result is None:

            print(
                "\nCustomer account not found."
            )

            return

        (
            customer_id,
            customer_name,
            customer_account_no,
            account_status,
            current_balance
        ) = customer_result

        # ====================================
        # GET CUSTOMER TRANSACTIONS
        # ====================================

        cursor.execute(
            """
            SELECT
                transaction_type,
                amount,
                sender_account,
                receiver_account
            FROM transactions
            WHERE
                customer_id = %s
                OR sender_account = %s
                OR receiver_account = %s
            """,
            (
                customer_id,
                customer_account_no,
                customer_account_no
            )
        )

        transactions = cursor.fetchall()

        # ========================================
        # INITIALIZE SUMMARY
        # ========================================

        total_deposits = to_decimal(0)
        total_withdrawals = to_decimal(0)
        total_sent = to_decimal(0)
        total_received = to_decimal(0)

        deposit_count = 0
        withdrawal_count = 0
        sent_count = 0
        received_count = 0

        # ========================================
        # PROCESS TRANSACTIONS
        # ========================================

        for transaction in transactions:

            (
                transaction_type,
                amount,
                sender_account,
                receiver_account
            ) = transaction

            amount = to_decimal(amount)

            # ------------------------------------
            # DEPOSIT
            # ------------------------------------

            if transaction_type in (
                "Deposit",
                "Initial Deposit"
            ):

                total_deposits += amount

                deposit_count += 1

            # ------------------------------------
            # WITHDRAWAL
            # ------------------------------------

            elif transaction_type == "Withdrawal":

                total_withdrawals += amount

                withdrawal_count += 1

            # ------------------------------------
            # TRANSFER
            # ------------------------------------

            elif transaction_type == "Transfer":

                # Transfer sent by customer

                if sender_account == customer_account_no:

                    total_sent += amount

                    sent_count += 1

                # Transfer received by customer

                elif receiver_account == customer_account_no:

                    total_received += amount

                    received_count += 1

        # ========================================
        # DISPLAY CUSTOMER
        # ========================================

        print(
            "Customer Name       :",
            customer_name
        )

        print(
            "Account Number      :",
            customer_account_no
        )

        print(
            "Account Status      :",
            account_status
        )

        print(
            "\n----------------------------------------"
        )

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

        print(
            "\n----------------------------------------"
        )

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

        print(
            "\n----------------------------------------"
        )

        # ========================================
        # CURRENT BALANCE
        # ========================================

        print(
            "Current Balance     : ₹",
            format(
                to_decimal(current_balance),
                ".2f"
            )
        )

        print(
            "========================================"
        )

    except psycopg2.Error as error:

        print(
            "\nDatabase error while "
            "generating transaction summary."
        )

        print(
            "Database Error:",
            error
        )

    except Exception as error:

        print(
            "\nUnexpected error while "
            "generating transaction summary."
        )

        print(
            "Error:",
            error
        )

    finally:

        if cursor is not None:

            cursor.close()

        connection.close()

    input(
        "\nPress Enter to return..."
    )

#=================================
#EXPORT ACCOUNT STATEMENT
#================================
def export_account_statement(customer):

    print("\n========================================")
    print("       EXPORT ACCOUNT STATEMENT")
    print("========================================")

    account_no = customer.get(
        "account_no"
    )

    # ========================================
    # DATABASE CONNECTION
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print(
            "\nUnable to connect to PostgreSQL."
        )

        input(
            "\nPress Enter to return..."
        )

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ====================================
        # GET CUSTOMER ID
        # ====================================

        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE account_no = %s
            """,
            (
                account_no,
            )
        )

        customer_result = cursor.fetchone()

        if customer_result is None:

            print(
                "\nCustomer account not found."
            )

            return

        customer_id = customer_result[0]

        # ====================================
        # GET TRANSACTIONS
        # ====================================

        cursor.execute(
            """
            SELECT
                transaction_id,
                date,
                transaction_type,
                amount,
                status,
                sender_name,
                sender_account,
                receiver_name,
                receiver_account
            FROM transactions
            WHERE
                customer_id = %s
                OR sender_account = %s
                OR receiver_account = %s
            ORDER BY date ASC
            """,
            (
                customer_id,
                account_no,
                account_no
            )
        )

        transactions = cursor.fetchall()

        # ====================================
        # CHECK TRANSACTIONS
        # ====================================

        if not transactions:

            print(
                "\nNo transactions available to export."
            )

            return

        # ====================================
        # FILE NAME
        # ====================================

        filename = (
            f"account_statement_{account_no}.csv"
        )

        # ====================================
        # CREATE CSV FILE
        # ====================================

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            # =================================
            # CSV HEADER
            # =================================

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

            # =================================
            # WRITE TRANSACTIONS
            # =================================

            for transaction in transactions:

                (
                    transaction_id,
                    transaction_date,
                    transaction_type,
                    amount,
                    status,
                    sender_name,
                    sender_account,
                    receiver_name,
                    receiver_account
                ) = transaction

                # =============================
                # DETERMINE DISPLAY TYPE
                # =============================

                display_type = transaction_type

                if transaction_type == "Transfer":

                    if sender_account == account_no:

                        display_type = "Transfer Sent"

                    elif receiver_account == account_no:

                        display_type = "Transfer Received"

                # =============================
                # MASK ACCOUNTS
                # =============================

                if sender_account:

                    sender_account_display = (
                        "XXXX"
                        + str(sender_account)[-4:]
                    )

                else:

                    sender_account_display = (
                        "Not available"
                    )

                if receiver_account:

                    receiver_account_display = (
                        "XXXX"
                        + str(receiver_account)[-4:]
                    )

                else:

                    receiver_account_display = (
                        "Not available"
                    )

                # =============================
                # WRITE CSV ROW
                # =============================

                writer.writerow([

                    transaction_id,

                    transaction_date,

                    display_type,

                    amount,

                    status,

                    sender_name
                    if sender_name
                    else "Not available",

                    sender_account_display,

                    receiver_name
                    if receiver_name
                    else "Not available",

                    receiver_account_display
                ])

        # ====================================
        # EXPORT SUCCESS
        # ====================================

        print(
            "\n========================================"
        )

        print(
            "       EXPORT SUCCESSFUL"
        )

        print(
            "========================================"
        )

        print(
            "File Name:",
            filename
        )

        print(
            "Transactions Exported:",
            len(transactions)
        )

        print(
            "========================================"
        )

    except psycopg2.Error as error:

        print(
            "\n========================================"
        )

        print(
            "          EXPORT FAILED"
        )

        print(
            "========================================"
        )

        print(
            "Database Error:",
            error
        )

        print(
            "========================================"
        )

    except Exception as error:

        print(
            "\n========================================"
        )

        print(
            "          EXPORT FAILED"
        )

        print(
            "========================================"
        )

        print(
            "Error:",
            error
        )

        print(
            "========================================"
        )

    finally:

        if cursor:

            cursor.close()

        connection.close()

    input(
        "\nPress Enter to return..."
    )

    
# ========================================
# CUSTOMER PROFILE
# ========================================

def customer_profile(customer):

    print("\n========================================")
    print("          CUSTOMER PROFILE")
    print("========================================")

    connection = get_db_connection()

    if connection is None:
        print("\nUnable to load customer profile.")
        input("\nPress Enter to return...")
        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ========================================
        # GET CUSTOMER DETAILS FROM POSTGRESQL
        # ========================================

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                account_no,
                status,
                mobile,
                mobile_verified,
                email,
                email_type,
                aadhaar_masked,
                balance,
                created_at
            FROM customers
            WHERE account_no = %s
            """,
            (
                customer.get("account_no"),
            )
        )

        result = cursor.fetchone()

        if result is None:

            print("\nCustomer account not found.")

            input(
                "\nPress Enter to return..."
            )

            return

        (
            customer_id,
            name,
            account_no,
            status,
            mobile,
            mobile_verified,
            email,
            email_type,
            aadhaar_masked,
            balance,
            created_at
        ) = result

        # ========================================
        # BASIC DETAILS
        # ========================================

        print("\n----------------------------------------")
        print("             BASIC DETAILS")
        print("----------------------------------------")

        print(
            "Customer Name  :",
            name
        )

        print(
            "Account Number :",
            account_no
        )

        print(
            "Account Status :",
            status
        )

        # ========================================
        # CONTACT DETAILS
        # ========================================

        print("\n----------------------------------------")
        print("            CONTACT DETAILS")
        print("----------------------------------------")

        print(
            "Mobile Number  :",
            mobile if mobile else "Not available"
        )

        print(
            "Mobile Verified:",
            "YES" if mobile_verified else "NO"
        )

        print(
            "Email          :",
            email if email else "Not available"
        )

        print(
            "Email Type     :",
            email_type if email_type else "Not available"
        )

        # ========================================
        # AADHAAR
        # ========================================

        print("\n----------------------------------------")
        print("            IDENTITY DETAILS")
        print("----------------------------------------")

        print(
            "Aadhaar        :",
            aadhaar_masked if aadhaar_masked else "Not available"
        )

        # ========================================
        # ACCOUNT DETAILS
        # ========================================

        print("\n----------------------------------------")
        print("            ACCOUNT DETAILS")
        print("----------------------------------------")

        current_balance = to_decimal(
            balance
        )

        print(
            "Current Balance: ₹",
            format(
                current_balance,
                ".2f"
            )
        )

        # ========================================
        # ACCOUNT CREATED DATE
        # ========================================

        if created_at:

            print(
                "Account Created:",
                created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

        # ========================================
        # TRANSACTION COUNT
        # ========================================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            WHERE
                customer_id = %s
                OR sender_account = %s
                OR receiver_account = %s
            """,
            (
                customer_id,
                account_no,
                account_no
            )
        )

        transaction_count = cursor.fetchone()[0]

        print(
            "Transactions   :",
            transaction_count
        )

        print("\n========================================")

        input(
            "\nPress Enter to return..."
        )

    except psycopg2.Error as error:

        print("\nUnable to load customer profile.")

        print(
            "Database Error:",
            error
        )

        input(
            "\nPress Enter to return..."
        )

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()

# ========================================
# CUSTOMER TRANSACTION SEARCH
# ========================================
def customer_transaction_search(customer):

    print("\n========================================")
    print("       TRANSACTION SEARCH")
    print("========================================")

    account_no = customer.get("account_no")

    # ========================================
    # DATABASE CONNECTION
    # ========================================

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to connect to PostgreSQL.")

        input("\nPress Enter to return...")

        return

    cursor = None

    try:

        cursor = connection.cursor()

        # ====================================
        # GET CUSTOMER ID
        # ====================================

        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )

        customer_result = cursor.fetchone()

        if customer_result is None:

            print("\nCustomer account not found.")

            return

        customer_id = customer_result[0]

        # ====================================
        # CHECK TRANSACTIONS
        # ====================================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            WHERE
                customer_id = %s
                OR sender_account = %s
                OR receiver_account = %s
            """,
            (
                customer_id,
                account_no,
                account_no
            )
        )

        transaction_count = cursor.fetchone()[0]

        if transaction_count == 0:

            print("\nNo transactions found.")
            print("========================================")

            return

        # ====================================
        # SEARCH MENU
        # ====================================

        while True:

            print("\n========================================")
            print("       SEARCH TRANSACTIONS")
            print("========================================")

            print("1. Search by Transaction ID")
            print("2. Search by Transaction Type")
            print("3. Search by Date")
            print("4. View All Transactions")
            print("5. Back")

            choice = input(
                "\nEnter your choice (1-5): "
            ).strip()

            # =================================
            # SEARCH BY TRANSACTION ID
            # =================================

            if choice == "1":

                search_id = input(
                    "\nEnter Transaction ID: "
                ).strip().upper()

                cursor.execute(
                    """
                    SELECT
                        transaction_id,
                        transaction_type,
                        amount,
                        sender_account,
                        receiver_account,
                        sender_name,
                        receiver_name,
                        date,
                        status
                    FROM transactions
                    WHERE
                        transaction_id = %s
                        AND (
                            customer_id = %s
                            OR sender_account = %s
                            OR receiver_account = %s
                        )
                    """,
                    (
                        search_id,
                        customer_id,
                        account_no,
                        account_no
                    )
                )

                transaction = cursor.fetchone()

                if transaction:

                    (
                        transaction_id,
                        transaction_type,
                        amount,
                        sender_account,
                        receiver_account,
                        sender_name,
                        receiver_name,
                        transaction_date,
                        status
                    ) = transaction

                    display_type = transaction_type

                    if transaction_type == "Transfer":

                        if sender_account == account_no:

                            display_type = "Transfer Sent"

                        elif receiver_account == account_no:

                            display_type = "Transfer Received"

                    print(
                        "\n========================================"
                    )

                    print(
                        "       TRANSACTION FOUND"
                    )

                    print(
                        "========================================"
                    )

                    print(
                        "Transaction ID :",
                        transaction_id
                    )

                    print(
                        "Type           :",
                        display_type
                    )

                    print(
                        "Amount         : ₹",
                        format(
                            amount,
                            ".2f"
                        )
                    )

                    print(
                        "Date & Time    :",
                        transaction_date
                    )

                    print(
                        "Status         :",
                        status
                    )

                    if transaction_type == "Transfer":

                        print(
                            "Sender Name    :",
                            sender_name
                        )

                        print(
                            "Sender Account : XXXX",
                            str(sender_account)[-4:]
                        )

                        print(
                            "Receiver Name  :",
                            receiver_name
                        )

                        print(
                            "Receiver Account: XXXX",
                            str(receiver_account)[-4:]
                        )

                else:

                    print(
                        "\nTransaction ID not found."
                    )

                print(
                    "========================================"
                )

            # =================================
            # SEARCH BY TRANSACTION TYPE
            # =================================

            elif choice == "2":

                print("\nTransaction Types:")

                print("1. Initial Deposit")
                print("2. Deposit")
                print("3. Withdrawal")
                print("4. Transfer Sent")
                print("5. Transfer Received")

                type_choice = input(
                    "\nEnter your choice (1-5): "
                ).strip()

                transaction_types = {

                    "1": "Initial Deposit",

                    "2": "Deposit",

                    "3": "Withdrawal",

                    "4": "Transfer Sent",

                    "5": "Transfer Received"

                }

                if type_choice not in transaction_types:

                    print(
                        "\nInvalid transaction type."
                    )

                    continue

                selected_type = transaction_types[
                    type_choice
                ]

                # ---------------------------------
                # DATABASE TYPE CONDITION
                # ---------------------------------

                if selected_type == "Transfer Sent":

                    type_condition = """
                        transaction_type = 'Transfer'
                        AND sender_account = %s
                    """

                    type_parameters = (
                        account_no,
                    )

                elif selected_type == "Transfer Received":

                    type_condition = """
                        transaction_type = 'Transfer'
                        AND receiver_account = %s
                    """

                    type_parameters = (
                        account_no,
                    )

                else:

                    type_condition = """
                        transaction_type = %s
                    """

                    type_parameters = (
                        selected_type,
                    )

                query = f"""
                    SELECT
                        transaction_id,
                        transaction_type,
                        amount,
                        sender_account,
                        receiver_account,
                        sender_name,
                        receiver_name,
                        date,
                        status
                    FROM transactions
                    WHERE
                        (
                            customer_id = %s
                            OR sender_account = %s
                            OR receiver_account = %s
                        )
                        AND {type_condition}
                    ORDER BY date ASC
                """

                cursor.execute(
                    query,
                    (
                        customer_id,
                        account_no,
                        account_no,
                        *type_parameters
                    )
                )

                transactions = cursor.fetchall()

                print(
                    "\n========================================"
                )

                print(
                    "TRANSACTIONS:",
                    selected_type
                )

                print(
                    "========================================"
                )

                if transactions:

                    for transaction in transactions:

                        (
                            transaction_id,
                            transaction_type,
                            amount,
                            sender_account,
                            receiver_account,
                            sender_name,
                            receiver_name,
                            transaction_date,
                            status
                        ) = transaction

                        display_type = transaction_type

                        if transaction_type == "Transfer":

                            if sender_account == account_no:

                                display_type = "Transfer Sent"

                            elif receiver_account == account_no:

                                display_type = "Transfer Received"

                        print(
                            "\n----------------------------------------"
                        )

                        print(
                            "Transaction ID :",
                            transaction_id
                        )

                        print(
                            "Type           :",
                            display_type
                        )

                        print(
                            "Amount         : ₹",
                            format(
                                amount,
                                ".2f"
                            )
                        )

                        print(
                            "Date & Time    :",
                            transaction_date
                        )

                        print(
                            "Status         :",
                            status
                        )

                else:

                    print(
                        "\nNo transactions found "
                        "for this type."
                    )

                print(
                    "----------------------------------------"
                )

            # =================================
            # SEARCH BY DATE
            # =================================

            elif choice == "3":

                search_date = input(
                    "\nEnter date (YYYY-MM-DD): "
                ).strip()

                try:

                    datetime.strptime(
                        search_date,
                        "%Y-%m-%d"
                    )

                except ValueError:

                    print(
                        "\nInvalid date format."
                    )

                    print(
                        "Please use YYYY-MM-DD."
                    )

                    continue

                cursor.execute(
                    """
                    SELECT
                        transaction_id,
                        transaction_type,
                        amount,
                        sender_account,
                        receiver_account,
                        sender_name,
                        receiver_name,
                        date,
                        status
                    FROM transactions
                    WHERE
                        (
                            customer_id = %s
                            OR sender_account = %s
                            OR receiver_account = %s
                        )
                        AND DATE(date) = %s
                    ORDER BY date ASC
                    """,
                    (
                        customer_id,
                        account_no,
                        account_no,
                        search_date
                    )
                )

                transactions = cursor.fetchall()

                print(
                    "\n========================================"
                )

                print(
                    "TRANSACTIONS ON:",
                    search_date
                )

                print(
                    "========================================"
                )

                if transactions:

                    for transaction in transactions:

                        (
                            transaction_id,
                            transaction_type,
                            amount,
                            sender_account,
                            receiver_account,
                            sender_name,
                            receiver_name,
                            transaction_date,
                            status
                        ) = transaction

                        display_type = transaction_type

                        if transaction_type == "Transfer":

                            if sender_account == account_no:

                                display_type = "Transfer Sent"

                            elif receiver_account == account_no:

                                display_type = "Transfer Received"

                        print(
                            "\n----------------------------------------"
                        )

                        print(
                            "Transaction ID :",
                            transaction_id
                        )

                        print(
                            "Type           :",
                            display_type
                        )

                        print(
                            "Amount         : ₹",
                            format(
                                amount,
                                ".2f"
                            )
                        )

                        print(
                            "Date & Time    :",
                            transaction_date
                        )

                        print(
                            "Status         :",
                            status
                        )

                else:

                    print(
                        "\nNo transactions found "
                        "on this date."
                    )

                print(
                    "----------------------------------------"
                )

            # =================================
            # VIEW ALL
            # =================================

            elif choice == "4":

                transaction_history(
                    customer
                )

            # =================================
            # BACK
            # =================================

            elif choice == "5":

                print(
                    "\nReturning to customer dashboard..."
                )

                break

            else:

                print(
                    "\nInvalid choice! "
                    "Please select 1-5."
                )

    except psycopg2.Error as error:

        print(
            "\nDatabase error while "
            "searching transactions."
        )

        print(
            "Database Error:",
            error
        )

    finally:

        if cursor:

            cursor.close()

        connection.close()

# ========================================
# CUSTOMER NOTIFICATIONS
# ========================================
def customer_notifications(customer):

    print("\n========================================")
    print("          NOTIFICATIONS")
    print("========================================")

    connection = get_db_connection()

    if connection is None:

        print("\nUnable to connect to PostgreSQL.")

        input("\nPress Enter to return...")

        return

    try:

        cursor = connection.cursor()

        # ========================================
        # GET CUSTOMER ID
        # ========================================

        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE account_no = %s
            """,
            (customer.get("account_no"),)
        )

        customer_result = cursor.fetchone()

        if customer_result is None:

            print("\nCustomer account not found.")
            print("========================================")

            input("\nPress Enter to return...")

            return

        customer_id = customer_result[0]

        # ========================================
        # GET NOTIFICATIONS
        # ========================================

        while True:

            cursor.execute(
                """
                SELECT
                    notification_id,
                    message,
                    transaction_id,
                    is_read,
                    created_at
                FROM notifications
                WHERE customer_id = %s
                ORDER BY created_at ASC
                """,
                (customer_id,)
            )

            notifications = cursor.fetchall()

            # ========================================
            # NO NOTIFICATIONS
            # ========================================

            if len(notifications) == 0:

                print("\nNo notifications found.")
                print("========================================")

                input("\nPress Enter to return...")

                return

            # ========================================
            # DISPLAY NOTIFICATIONS
            # ========================================

            print("\n========================================")
            print("          YOUR NOTIFICATIONS")
            print("========================================")

            unread_count = 0

            for index, notification in enumerate(
                notifications,
                start=1
            ):

                notification_id = notification[0]
                message = notification[1]
                transaction_id = notification[2]
                is_read = notification[3]
                created_at = notification[4]

                if is_read:

                    status = "READ"

                else:

                    status = "UNREAD"

                    unread_count += 1

                print("\nNotification", index)
                print("----------------------------------------")

                print(
                    "Notification ID :",
                    notification_id
                )

                print(
                    "Message         :",
                    message
                )

                if transaction_id:

                    print(
                        "Transaction ID  :",
                        transaction_id
                    )

                print(
                    "Date            :",
                    created_at
                )

                print(
                    "Status          :",
                    status
                )

            print("\n========================================")
            print(
                "Unread Notifications:",
                unread_count
            )
            print("========================================")

            # ========================================
            # NOTIFICATION MENU
            # ========================================

            print("\n1. Mark Notification as Read")
            print("2. Mark All Notifications as Read")
            print("3. Refresh Notifications")
            print("4. Back")

            choice = input(
                "\nEnter your choice (1-4): "
            ).strip()

            # ========================================
            # MARK ONE AS READ
            # ========================================

            if choice == "1":

                try:

                    notification_number = int(
                        input(
                            "Enter notification number: "
                        ).strip()
                    )

                except ValueError:

                    print(
                        "\nPlease enter a valid number."
                    )

                    continue

                if (
                    notification_number < 1
                    or
                    notification_number > len(notifications)
                ):

                    print(
                        "\nInvalid notification number."
                    )

                    continue

                notification_id = notifications[
                    notification_number - 1
                ][0]

                # ========================================
                # UPDATE DATABASE
                # ========================================

                cursor.execute(
                    """
                    UPDATE notifications
                    SET is_read = TRUE
                    WHERE
                        notification_id = %s
                        AND customer_id = %s
                    """,
                    (
                        notification_id,
                        customer_id
                    )
                )

                connection.commit()

                print(
                    "\nNotification marked as read."
                )

                input(
                    "\nPress Enter to continue..."
                )

            # ========================================
            # MARK ALL AS READ
            # ========================================

            elif choice == "2":

                cursor.execute(
                    """
                    UPDATE notifications
                    SET is_read = TRUE
                    WHERE customer_id = %s
                    """,
                    (customer_id,)
                )

                connection.commit()

                print(
                    "\nAll notifications marked as read."
                )

                input(
                    "\nPress Enter to continue..."
                )

            # ========================================
            # REFRESH
            # ========================================

            elif choice == "3":

                print(
                    "\nRefreshing notifications..."
                )

                continue

            # ========================================
            # BACK
            # ========================================

            elif choice == "4":

                print(
                    "\nReturning to customer dashboard..."
                )

                break

            else:

                print(
                    "\nInvalid choice!"
                )

                print(
                    "Please select 1-4."
                )

    except psycopg2.Error as error:

        connection.rollback()

        print(
            "\nDatabase error while loading notifications."
        )

        print(
            "Database Error:",
            error
        )

        input("\nPress Enter to return...")

    finally:

        cursor.close()
        connection.close()

# ========================================
# GET UNREAD NOTIFICATION COUNT
# ========================================

def get_unread_notification_count(customer):

    notifications = customer.get(
        "notifications",
        []
    )

    if not isinstance(notifications, list):
        return 0

    unread_count = 0

    for notification in notifications:

        if not isinstance(notification, dict):
            continue

        if notification.get("read", False) is False:

            unread_count += 1

    return unread_count
# ========================================
# CUSTOMER DASHBOARD
# ========================================

def customer_dashboard(customer):

    while True:
        print("\n========================================")
        print("          CUSTOMER DASHBOARD")
        print("========================================")

        print(
            "Welcome,",
            customer.get("name", "Customer")
        )

        print("\n1.  Check Balance")
        print("2.  Deposit Money")
        print("3.  Withdraw Money")
        print("4.  Transfer Money")
        print("5.  Transaction History")
        print("6.  Change Password")
        print("7.  Account Statement")
        print("8.  Customer Profile")
        print("9.  Filter Transaction By Date")
        print("10. Filter Transaction By Date Range")
        print("11. Sort Transactions")
        print("12. Filter Transaction By Type And Date")
        print("13. Transaction Summary")
        print("14. Export Account Statement")


        unread_count = get_unread_notification_count(customer)

        if unread_count > 0:

            print(
                f"15. Customer Notifications ({unread_count})"
            )
        else:
            print("15. Customer Notifiactions")
        
        print("16. Transaction Search")

        print("17. Logout")

        print("")

        choice = input(
            "Enter your choice (1-17): "
        ).strip()
        # ========================================
        # 1. CHECK BALANCE
        # ========================================

        if choice == "1":

            print("\n========================================")
            print("          ACCOUNT BALANCE")
            print("========================================")

            connection = get_db_connection()

            if connection is None:

                print("\nUnable to connect to database.")

                continue

            cursor = None

            try:

                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT
                        account_no,
                        name,
                        balance
                    FROM customers
                    WHERE account_no = %s
                    """,
                    (
                        customer.get(
                            "account_no"
                        ),
                    )
                )

                result = cursor.fetchone()

                if result is None:

                    print("\nCustomer account not found.")

                    continue

                account_no = result[0]
                name = result[1]
                balance = result[2]

                print(
                    "Account Number :",
                    account_no
                )

                print(
                    "Account Holder :",
                    name
                )

                print(
                    "Current Balance: ₹",
                    format(
                        balance,
                        ".2f"
                    )
                )

                print("========================================")

            except psycopg2.Error as error:

                print(
                    "\nDatabase Error:",
                    error
                )

            finally:

                if cursor is not None:
                    cursor.close()

                connection.close()

        # ========================================
        # 2. DEPOSIT
        # ========================================

        elif choice == "2":

            deposit_money(
                customer
            )

        # ========================================
        # 3. WITHDRAW
        # ========================================

        elif choice == "3":

            withdraw_money(
                customer
            )

        # ========================================
        # 4. TRANSFER
        # ========================================

        elif choice == "4":

            transfer_money(
                customer
            )

        # ========================================
        # 5. TRANSACTION HISTORY
        # ========================================

        elif choice == "5":

            transaction_history(
                customer
            )

        # ========================================
        # 6. CHANGE PASSWORD
        # ========================================

        elif choice == "6":

            change_password(
                customer
            )

        # ========================================
        # 7. ACCOUNT STATEMENT
        # ========================================

        elif choice == "7":

            account_statement(
                customer
            )

        # ========================================
        # 8. CUSTOMER PROFILE
        # ========================================

        elif choice == "8":

            customer_profile(
                customer
            )

        # ========================================
        # 9. FILTER BY DATE
        # ========================================

        elif choice == "9":

            filter_transactions_by_date(
                customer
            )

        # ========================================
        # 10. FILTER BY DATE RANGE
        # ========================================

        elif choice == "10":

            filter_transactions_by_date_range(
                customer
            )

        # ========================================
        # 11. SORT TRANSACTIONS
        # ========================================

        elif choice == "11":

            sort_transactions(
                customer
            )

        # ========================================
        # 12. FILTER BY TYPE AND DATE
        # ========================================

        elif choice == "12":

            filter_transactions_by_type_and_date(
                customer
            )

        # ========================================
        # 13. TRANSACTION SUMMARY
        # ========================================

        elif choice == "13":

            customer_transaction_summary(
                customer
            )

        # ========================================
        # 14. EXPORT ACCOUNT STATEMENT
        # ========================================

        elif choice == "14":

            export_account_statement(
                customer
            )

        # ========================================
        # 15. CUSTOMER NOTIFICATIONS
        # ========================================

        elif choice == "15":

            customer_notifications(
                customer
            )
        elif choice == "16":

            customer_transaction_search(customer)
        # ========================================
        # 16. LOGOUT
        # ========================================

        elif choice == "17":

            print("\n========================================")
            print("       LOGGED OUT SUCCESSFULLY")
            print("========================================")

            break

        # ========================================
        # INVALID CHOICE
        # ========================================

        else:

            print(
                "\nInvalid choice! Please try again."
            )



connection = get_db_connection()

if connection:

    print("\n========================================")
    print("   POSTGRESQL DATABASE CONNECTED")
    print("========================================")

    connection.close()

else:

    print("\n========================================")
    print("   POSTGRESQL DATABASE CONNECTION FAILED")
    print("========================================")

#=========================
#MAIN MENU
#=========================
if __name__ == "__main__":

    check_transaction_consistency()

    while True:

        print("\n MAIN MENU")

        print("1. Register")
        print("2. Customer Login")
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
        

