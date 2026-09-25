from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import psycopg2
import hashlib
import bcrypt
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder="website", static_url_path="")
CORS(app)

@app.route("/")
def home():
    return app.send_static_file("index.html")

# =========================================
# DATABASE CONNECTION
# =========================================
def get_db_connection():
    try:
        database_url = os.getenv("DATABASE_URL")

        if database_url:
            connection = psycopg2.connect(database_url)
        else:
            connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            )

        return connection

    except psycopg2.Error as error:
        print("\nDatabase connection error:")
        print(error)
        return None

# =========================================
# BACKEND TEST ROUTE
# =========================================



# =========================================
# DATABASE TEST ROUTE
# =========================================

@app.route("/database-test")
def database_test():

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500


    try:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM customers"
        )

        customer_count = cursor.fetchone()[0]

        cursor.close()
        connection.close()


        return jsonify({

            "status": "success",

            "message":
                "PostgreSQL connection successful.",

            "customers":
                customer_count

        })


    except psycopg2.Error as error:

        if connection:
            connection.close()

        return jsonify({

            "status": "error",

            "message":
                "Database query failed.",

            "error":
                str(error)

        }), 500


@app.route("/api/login", methods=["POST"])
def api_login():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No login data received."
        }), 400


    account_number = data.get("account_number")
    password = data.get("password")


    if not account_number or not password:

        return jsonify({
            "status": "error",
            "message": "Account number and password are required."
        }), 400


    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500


    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                customer_id,
                account_no,
                name,
                password_hash,
                status
            FROM customers
            WHERE account_no = %s
            """,
            (account_number,)
        )

        customer = cursor.fetchone()


        if customer is None:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Invalid account number or password."
            }), 401


        customer_id = customer[0]
        account_no = customer[1]
        name = customer[2]
        stored_password = customer[3]
        account_status = customer[4]


        if account_status != "Active":

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Your account is not active."
            }), 403


        password_is_valid = False


        # Existing SHA-256 password

        if stored_password and len(stored_password) == 64:

            password_hash = hashlib.sha256(
                password.encode("utf-8")
            ).hexdigest()

            if password_hash == stored_password:

                password_is_valid = True


# New bcrypt password

        elif stored_password:

            try:

                password_is_valid = bcrypt.checkpw(
                    password.encode("utf-8"),
                    stored_password.encode("utf-8")
                )

            except (ValueError, TypeError):

                password_is_valid = False


        if not password_is_valid:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Invalid account number or password."
        }), 401


        cursor.close()
        connection.close()


        return jsonify({
            "status": "success",
            "message": "Login successful.",
            "customer_id": customer_id,
            "account_no": account_no,
            "name": name
        })


    except psycopg2.Error as error:

        print("\nLogin database error:")
        print(error)

        if connection:
            connection.close()

        return jsonify({
            "status": "error",
            "message": "Login database operation failed."
        }), 500


@app.route("/api/register", methods=["POST"])
def api_register():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No registration data received."
        }), 400


    name = data.get("name", "").strip()
    mobile = data.get("mobile", "").strip()
    email = data.get("email", "").strip()
    aadhaar = data.get("aadhaar", "").strip()
    password = data.get("password", "").strip()


    # =========================================
    # VALIDATION
    # =========================================

    if not name:

        return jsonify({
            "status": "error",
            "message": "Full name is required."
        }), 400


    if len(name) < 3:

        return jsonify({
            "status": "error",
            "message": "Full name must contain at least 3 characters."
        }), 400


    if not mobile:

        return jsonify({
            "status": "error",
            "message": "Mobile number is required."
        }), 400


    if not mobile.isdigit() or len(mobile) != 10:

        return jsonify({
            "status": "error",
            "message": "Mobile number must contain exactly 10 digits."
        }), 400


    if not email:

        return jsonify({
            "status": "error",
            "message": "Email is required."
        }), 400


    if not aadhaar:

        return jsonify({
            "status": "error",
            "message": "Aadhaar number is required."
        }), 400


    if not aadhaar.isdigit() or len(aadhaar) != 12:

        return jsonify({
            "status": "error",
            "message": "Aadhaar number must contain exactly 12 digits."
        }), 400


    if not password:

        return jsonify({
            "status": "error",
            "message": "Password is required."
        }), 400


    if len(password) < 4:

        return jsonify({
            "status": "error",
            "message": "Password must contain at least 4 characters."
        }), 400


    # =========================================
    # DATABASE CONNECTION
    # =========================================

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500


    try:

        cursor = connection.cursor()


        # =====================================
        # CHECK MOBILE
        # =====================================

        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE mobile = %s
            """,
            (mobile,)
        )

        existing_mobile = cursor.fetchone()


        if existing_mobile:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "This mobile number is already registered."
            }), 409


        # =====================================
        # CHECK EMAIL
        # =====================================

        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE email = %s
            """,
            (email,)
        )

        existing_email = cursor.fetchone()


        if existing_email:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "This email is already registered."
            }), 409


        # =====================================
        # HASH AADHAAR
        # =====================================

        aadhaar_hash = hashlib.sha256(
            aadhaar.encode("utf-8")
        ).hexdigest()


        aadhaar_masked = (
            "XXXX-XXXX-" + aadhaar[-4:]
        )


        # =====================================
        # HASH PASSWORD USING BCRYPT
        # =====================================

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")


        # =====================================
        # GENERATE ACCOUNT NUMBER
        # =====================================

        cursor.execute(
            """
            SELECT COALESCE(MAX(account_no), 100000)
            FROM customers
            """
        )

        last_account_no = cursor.fetchone()[0]

        account_no = last_account_no + 1


        # =====================================
        # INSERT CUSTOMER
        # =====================================

        cursor.execute(
            """
            INSERT INTO customers (
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
            VALUES (
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
                False,
                email,
                "Personal",
                aadhaar_hash,
                aadhaar_masked,
                0.00,
                "Active"
            )
        )


        customer_id = cursor.fetchone()[0]


        # =====================================
        # COMMIT
        # =====================================

        connection.commit()


        cursor.close()
        connection.close()


        return jsonify({
            "status": "success",
            "message": "Account created successfully.",
            "customer_id": customer_id,
            "account_no": account_no,
            "name": name
        }), 201


    except psycopg2.Error as error:

        connection.rollback()

        print("\nRegistration database error:")
        print(error)

        if connection:
            connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to create account."
        }), 500


# =========================================
# GET CUSTOMER DASHBOARD DATA
# =========================================

@app.route("/api/customer/<int:account_no>", methods=["GET"])
def get_customer_dashboard(account_no):

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500


    try:

        cursor = connection.cursor()


        cursor.execute(
            """
            SELECT
                name,
                account_no,
                balance,
                status
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )


        customer = cursor.fetchone()


        if customer is None:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404


        name = customer[0]
        account_number = customer[1]
        balance = customer[2]
        status = customer[3]


        cursor.close()
        connection.close()


        return jsonify({
            "status": "success",
            "name": name,
            "account_no": account_number,
            "balance": float(balance),
            "account_status": status
        }), 200


    except psycopg2.Error as error:

        print("\nDashboard database error:")
        print(error)


        if connection:
            connection.close()


        return jsonify({
            "status": "error",
            "message": "Unable to retrieve customer information."
        }), 500


# =========================================
# DEPOSIT MONEY API
# =========================================

@app.route("/api/deposit", methods=["POST"])
def deposit_money_api():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No data received."
        }), 400


    account_no = data.get("account_no")
    amount = data.get("amount")


    # Validate account number

    try:
        account_no = int(account_no)

    except (ValueError, TypeError):

        return jsonify({
            "status": "error",
            "message": "Invalid account number."
        }), 400


    # Validate amount

    try:
        amount = float(amount)

    except (ValueError, TypeError):

        return jsonify({
            "status": "error",
            "message": "Invalid deposit amount."
        }), 400


    if amount <= 0:

        return jsonify({
            "status": "error",
            "message": "Deposit amount must be greater than zero."
        }), 400


    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500


    try:

        cursor = connection.cursor()


        # Get customer

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
            (account_no,)
        )

        customer = cursor.fetchone()


        if customer is None:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404


        customer_id = customer[0]
        customer_name = customer[1]
        current_balance = float(customer[2])
        account_status = customer[3]


        # Check account status

        if account_status != "Active":

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "This account is not active."
            }), 403


        # Generate transaction ID

        today = datetime.now().strftime("%Y%m%d")

        prefix = f"TXN-{today}-"


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


        # Calculate new balance

        new_balance = current_balance + amount


        # Update customer balance

        cursor.execute(
            """
            UPDATE customers
            SET balance = %s
            WHERE customer_id = %s
            """,
            (
                new_balance,
                customer_id
            )
        )


        # Insert transaction

        cursor.execute(
            """
            INSERT INTO transactions (
                transaction_id,
                customer_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                status
            )
            VALUES (
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
                customer_id,
                "Deposit",
                amount,
                None,
                account_no,
                None,
                customer_name,
                "SUCCESS"
            )
        )


        # Insert notification

        notification_message = (
            f"₹{amount:.2f} deposited successfully "
            f"into account {account_no}. "
            f"Transaction ID: {transaction_id}"
        )


        cursor.execute(
            """
            INSERT INTO notifications (
                customer_id,
                message,
                transaction_id,
                is_read
            )
            VALUES (
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                customer_id,
                notification_message,
                transaction_id,
                False
            )
        )


        connection.commit()


        cursor.close()
        connection.close()


        return jsonify({
            "status": "success",
            "message": "Money deposited successfully.",
            "transaction_id": transaction_id,
            "account_no": account_no,
            "amount": amount,
            "new_balance": new_balance
        }), 200


    except psycopg2.Error as error:

        print("\nDeposit database error:")
        print(error)


        if connection:

            connection.rollback()
            connection.close()


        return jsonify({
            "status": "error",
            "message": "Unable to complete the deposit."
        }), 500

# =========================================
# WITHDRAW MONEY API
# =========================================

@app.route("/api/withdraw", methods=["POST"])
def withdraw_money_api():

    data = request.get_json()

    account_no = data.get("account_no")
    amount = data.get("amount")

    # Validate input
    if not account_no or not amount:
        return jsonify({
            "status": "error",
            "message": "Account number and amount are required."
        }), 400

    try:
        account_no = int(account_no)
        amount = float(amount)

    except (ValueError, TypeError):

        return jsonify({
            "status": "error",
            "message": "Invalid account number or amount."
        }), 400

    if amount <= 0:

        return jsonify({
            "status": "error",
            "message": "Withdrawal amount must be greater than zero."
        }), 400

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        # Get customer details
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
            (account_no,)
        )

        customer = cursor.fetchone()

        if customer is None:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404

        customer_id = customer[0]
        customer_name = customer[1]
        current_balance = float(customer[2])
        account_status = customer[3]

        # Check account status
        if account_status != "Active":

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Account is not active."
            }), 403

        # Check sufficient balance
        if amount > current_balance:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Insufficient balance."
            }), 400

        # Generate transaction ID
        today = datetime.now().strftime("%Y%m%d")
        prefix = f"TXN-{today}-"

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

        transaction_id = f"{prefix}{next_number:04d}"

        # Calculate new balance
        new_balance = current_balance - amount

        # Update customer balance
        cursor.execute(
            """
            UPDATE customers
            SET balance = %s
            WHERE customer_id = %s
            """,
            (new_balance, customer_id)
        )

        # Insert withdrawal transaction
        cursor.execute(
            """
            INSERT INTO transactions (
                transaction_id,
                customer_id,
                transaction_type,
                amount,
                sender_account,
                sender_name,
                date,
                status
            )
            VALUES (
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
                customer_id,
                "Withdrawal",
                amount,
                account_no,
                customer_name,
                datetime.now(),
                "SUCCESS"
            )
        )

        # Create notification
        cursor.execute(
            """
            INSERT INTO notifications (
                customer_id,
                message,
                transaction_id,
                is_read
            )
            VALUES (
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                customer_id,
                f"₹{amount:.2f} withdrawn successfully. New balance: ₹{new_balance:.2f}",
                transaction_id,
                False
            )
        )

        # Commit everything
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "status": "success",
            "message": "Withdrawal successful.",
            "transaction_id": transaction_id,
            "account_no": account_no,
            "amount": amount,
            "new_balance": new_balance
        }), 200

    except psycopg2.Error as error:

        print("\nWithdrawal database error:")
        print(error)

        connection.rollback()
        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to process withdrawal."
        }), 500

# =========================================
# GET CUSTOMER TRANSACTIONS API
# =========================================

@app.route("/api/transactions/<int:account_no>", methods=["GET"])
def get_customer_transactions(account_no):

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        # Get customer details
        cursor.execute(
            """
            SELECT
                customer_id,
                balance
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )

        customer = cursor.fetchone()

        if customer is None:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404

        customer_id = customer[0]
        balance = customer[1]

        # Get customer transactions
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

        rows = cursor.fetchall()

        transactions = []

        for row in rows:

            transaction_id = row[0]
            transaction_type = row[1]
            amount = row[2]
            sender_account = row[3]
            receiver_account = row[4]
            sender_name = row[5]
            receiver_name = row[6]
            transaction_date = row[7]
            status = row[8]

            # Convert transfer into customer-specific view
            if transaction_type == "Transfer":

                if sender_account == account_no:

                    display_type = "Transfer Sent"

                elif receiver_account == account_no:

                    display_type = "Transfer Received"

                else:

                    display_type = "Transfer"

            else:

                display_type = transaction_type

            transactions.append({
                "transaction_id": transaction_id,
                "transaction_type": display_type,
                "amount": float(amount),
                "sender_account": sender_account,
                "receiver_account": receiver_account,
                "sender_name": sender_name,
                "receiver_name": receiver_name,
                "date": transaction_date.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "status": status
            })

        cursor.close()
        connection.close()

        return jsonify({
            "status": "success",
            "account_no": account_no,
            "balance": float(balance),
            "transactions": transactions
        }), 200

    except psycopg2.Error as error:

        print("\nTransaction history database error:")
        print(error)

        if connection:
            connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to retrieve transactions."
        }), 500

# =========================================
# GET CUSTOMER NOTIFICATIONS API
# =========================================

@app.route("/api/notifications/<int:account_no>", methods=["GET"])
def get_customer_notifications(account_no):

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        # Find customer
        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )

        customer = cursor.fetchone()

        if customer is None:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404

        customer_id = customer[0]

        # Get notifications
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
            ORDER BY created_at DESC
            """,
            (customer_id,)
        )

        rows = cursor.fetchall()

        notifications = []

        unread_count = 0

        for row in rows:

            notification_id = row[0]
            message = row[1]
            transaction_id = row[2]
            is_read = row[3]
            created_at = row[4]

            if not is_read:
                unread_count += 1

            notifications.append({
                "notification_id": notification_id,
                "message": message,
                "transaction_id": transaction_id,
                "is_read": is_read,
                "created_at": created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            })

        total_count = len(notifications)

        cursor.close()
        connection.close()

        return jsonify({
            "status": "success",
            "account_no": account_no,
            "total_notifications": total_count,
            "unread_notifications": unread_count,
            "notifications": notifications
        }), 200

    except psycopg2.Error as error:

        print("\nNotification database error:")
        print(error)

        if connection:
            connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to retrieve notifications."
        }), 500

# =========================================
# MARK NOTIFICATION AS READ API
# =========================================

@app.route(
    "/api/notifications/<int:notification_id>/read",
    methods=["PUT"]
)
def mark_notification_as_read(notification_id):

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        # Check notification exists
        cursor.execute(
            """
            SELECT
                notification_id,
                customer_id,
                is_read
            FROM notifications
            WHERE notification_id = %s
            """,
            (notification_id,)
        )

        notification = cursor.fetchone()

        if notification is None:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Notification not found."
            }), 404

        # Already read
        if notification[2] is True:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "success",
                "message": "Notification is already read."
            }), 200

        # Mark as read
        cursor.execute(
            """
            UPDATE notifications
            SET is_read = TRUE
            WHERE notification_id = %s
            """,
            (notification_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "status": "success",
            "message": "Notification marked as read."
        }), 200

    except psycopg2.Error as error:

        print("\nMark notification read database error:")
        print(error)

        connection.rollback()
        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to update notification."
        }), 500

# =========================================
# TRANSFER MONEY API
# =========================================

@app.route("/api/transfer", methods=["POST"])
def transfer_money_api():

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        data = request.get_json()

        sender_account = data.get("sender_account")
        receiver_account = data.get("receiver_account")
        amount = data.get("amount")


        # Validate input
        if not sender_account or not receiver_account or not amount:

            return jsonify({
                "status": "error",
                "message": "All transfer details are required."
            }), 400


        try:

            sender_account = int(sender_account)
            receiver_account = int(receiver_account)
            amount = float(amount)

        except (ValueError, TypeError):

            return jsonify({
                "status": "error",
                "message": "Invalid transfer details."
            }), 400


        if sender_account == receiver_account:

            return jsonify({
                "status": "error",
                "message": "You cannot transfer money to your own account."
            }), 400


        if amount <= 0:

            return jsonify({
                "status": "error",
                "message": "Transfer amount must be greater than zero."
            }), 400


        cursor = connection.cursor()


        # Get sender
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
            (sender_account,)
        )

        sender = cursor.fetchone()


        if sender is None:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Sender account not found."
            }), 404


        # Check sender status
        if sender[3] != "Active":

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Sender account is not active."
            }), 400


        # Check sufficient balance
        if float(sender[2]) < amount:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Insufficient balance."
            }), 400


        # Get receiver
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
            (receiver_account,)
        )

        receiver = cursor.fetchone()


        if receiver is None:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Receiver account not found."
            }), 404


        # Check receiver status
        if receiver[3] != "Active":

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Receiver account is not active."
            }), 400


        # Generate transaction ID
        today = datetime.now().strftime("%Y%m%d")

        prefix = f"TXN-{today}-"


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

                number_part = last_transaction_id[
                    len(prefix):
                ]

                highest_number = int(
                    number_part
                )

            except (ValueError, TypeError):

                highest_number = 0


        transaction_id = (
            f"{prefix}{highest_number + 1:04d}"
        )


        # Update sender balance
        cursor.execute(
            """
            UPDATE customers
            SET balance = balance - %s
            WHERE account_no = %s
            """,
            (
                amount,
                sender_account
            )
        )


        # Update receiver balance
        cursor.execute(
            """
            UPDATE customers
            SET balance = balance + %s
            WHERE account_no = %s
            """,
             (
                amount,
                receiver_account
            )
        )


        # Insert transfer transaction
        cursor.execute(
            """
            INSERT INTO transactions (
                transaction_id,
                customer_id,
                transaction_type,
                amount,
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                status
            )
            VALUES (
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
                sender[0],
                "Transfer",
                amount,
                sender_account,
                receiver_account,
                sender[1],
                receiver[1],
                "SUCCESS"
            )
        )


        # Sender notification
        cursor.execute(
            """
            INSERT INTO notifications (
                customer_id,
                message,
                transaction_id,
                is_read
            )
            VALUES (%s, %s, %s, FALSE)
            """,
            (
                sender[0],
                f"₹{amount:.2f} transferred successfully to "
                f"{receiver[1]} ({receiver_account}).",
                transaction_id
            )
        )


        # Receiver notification
        cursor.execute(
            """
            INSERT INTO notifications (
                customer_id,
                message,
                transaction_id,
                is_read
            )
            VALUES (%s, %s, %s, FALSE)
            """,
            (
                receiver[0],
                f"₹{amount:.2f} received successfully from "
                f"{sender[1]} ({sender_account}).",
                transaction_id
            )
        )


        connection.commit()


        # Get updated balances
        cursor.execute(
            """
            SELECT balance
            FROM customers
            WHERE account_no = %s
            """,
            (sender_account,)
        )

        sender_new_balance = cursor.fetchone()[0]


        cursor.execute(
            """
            SELECT balance
            FROM customers
            WHERE account_no = %s
            """,
            (receiver_account,)
        )

        receiver_new_balance = cursor.fetchone()[0]


        cursor.close()
        connection.close()


        return jsonify({
            "status": "success",
            "message": "Money transferred successfully.",
            "transaction_id": transaction_id,
            "sender_account": sender_account,
            "receiver_account": receiver_account,
            "amount": amount,
            "sender_new_balance": float(
                sender_new_balance
            ),
            "receiver_new_balance": float(
                receiver_new_balance
            )
        }), 200


    except psycopg2.Error as error:

        print("\nTransfer database error:")
        print(error)

        connection.rollback()
        connection.close()

        return jsonify({
            "status": "error",
            "message": "Transfer failed. Transaction rolled back."
        }), 500

# =========================================
# RECEIVER ACCOUNT LOOKUP API
# =========================================

@app.route("/api/customer/lookup/<account_no>", methods=["GET"])
def lookup_customer(account_no):

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                account_no,
                name,
                status
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )

        customer = cursor.fetchone()

        cursor.close()
        connection.close()

        if customer is None:
            return jsonify({
                "status": "error",
                "message": "Receiver account not found."
            }), 404

        if customer[2] != "Active":
            return jsonify({
                "status": "error",
                "message": "Receiver account is not active."
            }), 400

        return jsonify({
            "status": "success",
            "account_no": customer[0],
            "name": customer[1]
        }), 200

    except psycopg2.Error as error:

        print("\nReceiver lookup database error:")
        print(error)

        connection.rollback()
        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to find receiver account."
        }), 500

# =========================================
# CUSTOMER PROFILE API
# =========================================

@app.route("/api/profile/<account_no>", methods=["GET"])
def customer_profile_api(account_no):

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                name,
                account_no,
                email,
                mobile,
                status,
                created_at
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )

        customer = cursor.fetchone()

        cursor.close()
        connection.close()

        if customer is None:
            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404

        return jsonify({
            "status": "success",
            "name": customer[0],
            "account_no": customer[1],
            "email": customer[2],
            "mobile": customer[3],
            "account_status": customer[4],
            "created_at": customer[5].strftime("%Y-%m-%d %H:%M:%S")
                if customer[5]
                else None
        }), 200

    except psycopg2.Error as error:

        print("\nCustomer profile database error:")
        print(error)

        connection.rollback()
        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to load customer profile."
        }), 500

# =========================================
# ACCOUNT STATUS API
# =========================================

@app.route("/api/account-status/<account_no>", methods=["GET"])
def account_status_api(account_no):

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                account_no,
                status
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )

        customer = cursor.fetchone()

        cursor.close()
        connection.close()

        if customer is None:
            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404

        return jsonify({
            "status": "success",
            "account_no": customer[0],
            "account_status": customer[1]
        }), 200

    except psycopg2.Error as error:

        print("\nAccount status database error:")
        print(error)

        connection.rollback()
        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to check account status."
        }), 500

@app.route("/api/admin/change-account-status", methods=["POST"])
def change_account_status_api():

    data = request.get_json()

    account_no = data.get("account_no")
    new_status = data.get("new_status")

    if not account_no or not new_status:
        return jsonify({
            "status": "error",
            "message": "Account number and new status are required."
        }), 400

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE customers
            SET status = %s
            WHERE account_no = %s
            """,
            (new_status, account_no)
        )

        if cursor.rowcount == 0:
            cursor.close()
            connection.close()
            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404

        # =========================================
        # LOG ADMIN ACTIVITY
        # =========================================

        cursor.execute(
            """
            INSERT INTO admin_activity
            (action, details, date)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            """,
            (
                "Change Account Status",
                f"Account {account_no} status changed to {new_status}"
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "status": "success",
            "message": f"Account status changed to {new_status}."
        }), 200

    except psycopg2.Error as error:

        print("\nChange account status database error:")
        print(error)

        connection.rollback()
        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to change account status."
        }), 500

# =========================================
# ADMIN LOGIN API
# =========================================

@app.route("/api/admin/login", methods=["POST"])
def admin_login_api():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:

        return jsonify({
            "status": "error",
            "message": "Username and password are required."
        }), 400

    # Temporary admin credentials for development
    admin_username = "admin"
    admin_password = "admin123"

    if (
        username == admin_username
        and password == admin_password
    ):

        return jsonify({
            "status": "success",
            "message": "Admin login successful."
        }), 200

    return jsonify({
        "status": "error",
        "message": "Invalid admin username or password."
    }), 401

# =========================================
# ADMIN CUSTOMER STATUS DETAILS
# =========================================

@app.route("/api/admin/account-status/<account_no>", methods=["GET"])
def admin_account_status_api(account_no):

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT account_no, name, status
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )

        customer = cursor.fetchone()

        cursor.close()
        connection.close()

        if customer is None:

            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404

        return jsonify({
            "status": "success",
            "account_no": customer[0],
            "name": customer[1],
            "account_status": customer[2]
        }), 200

    except psycopg2.Error as error:

        print("\nAdmin account status details error:")
        print(error)

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to retrieve account status."
        }), 500
# =========================================
# ADMIN ACTIVITY LOG API
# =========================================

@app.route("/api/admin/activity-log", methods=["GET"])
def admin_activity_log_api():

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                activity_id,
                action,
                details,
                date
            FROM admin_activity
            ORDER BY activity_id DESC
            LIMIT 20
            """
        )

        activities = cursor.fetchall()

        cursor.close()
        connection.close()

        activity_list = []

        for activity in activities:

            activity_list.append({
                "activity_id": activity[0],
                "action": activity[1],
                "details": activity[2],
                "date": (
                    activity[3].strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if activity[3]
                    else ""
                )
            })

        return jsonify({
            "status": "success",
            "activities": activity_list
        }), 200

    except psycopg2.Error as error:

        print("\nAdmin activity log database error:")
        print(error)

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to retrieve admin activity log."
        }), 500

# =========================================
# ADMIN DASHBOARD STATISTICS API
# =========================================

@app.route("/api/admin/dashboard-statistics", methods=["GET"])
def admin_dashboard_statistics_api():

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*),
                COALESCE(SUM(balance), 0)
            FROM customers
            """
        )

        customer_data = cursor.fetchone()

        total_customers = customer_data[0]
        total_balance = customer_data[1]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            """
        )

        total_transactions = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return jsonify({
            "status": "success",
            "total_customers": total_customers,
            "total_balance": float(total_balance),
            "total_transactions": total_transactions
        }), 200

    except psycopg2.Error as error:

        print("\nAdmin dashboard statistics error:")
        print(error)

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to retrieve dashboard statistics."
        }), 500

# =========================================
# ADMIN SYSTEM HEALTH API
# =========================================

@app.route("/api/admin/system-health", methods=["GET"])
def admin_system_health_api():

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM customers
            """
        )

        total_customers = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            """
        )

        total_transactions = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM notifications
            """
        )

        total_notifications = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM admin_activity
            """
        )

        total_activities = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return jsonify({
            "status": "success",
            "database_status": "Connected",
            "total_customers": total_customers,
            "total_transactions": total_transactions,
            "total_notifications": total_notifications,
            "total_activities": total_activities
        }), 200

    except psycopg2.Error as error:

        print("\nAdmin system health error:")
        print(error)

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to retrieve system health."
        }), 500

# =========================================
# ADMIN CUSTOMER SEARCH API
# =========================================

@app.route("/api/admin/customer-search/<account_no>", methods=["GET"])
def admin_customer_search_api(account_no):

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                account_no,
                name,
                email,
                mobile,
                balance,
                status,
                created_at
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )

        customer = cursor.fetchone()

        cursor.close()
        connection.close()

        if customer is None:

            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404

        return jsonify({
            "status": "success",
            "account_no": customer[0],
            "name": customer[1],
            "email": customer[2],
            "mobile": customer[3],
            "balance": float(customer[4]),
            "account_status": customer[5],
            "created_at": (
                customer[6].strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if customer[6]
                else ""
            )
        }), 200

    except psycopg2.Error as error:

        print("\nAdmin customer search error:")
        print(error)

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to search customer."
        }), 500



#===========================================
#ADMIN CUSTOMER DETAILS API
#==========================================
@app.route("/api/admin/customer-details/<account_no>", methods=["GET"])
def admin_customer_details_api(account_no):

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                account_no,
                name,
                email,
                mobile,
                balance,
                status,
                created_at
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )

        customer = cursor.fetchone()

        cursor.close()
        connection.close()

        if customer is None:

            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404

        return jsonify({
            "status": "success",
            "account_no": customer[0],
            "name": customer[1],
            "email": customer[2],
            "mobile": customer[3],
            "balance": float(customer[4]),
            "account_status": customer[5],
            "created_at": (
                customer[6].strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if customer[6]
                else ""
            )
        }), 200

    except psycopg2.Error as error:

        print("\nAdmin customer details error:")
        print(error)

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to retrieve customer details."
        }), 500

#===========================================
# ADMIN TRANSACTION SEARCH API
#===========================================

@app.route("/api/admin/transaction-search/<transaction_id>", methods=["GET"])
def admin_transaction_search_api(transaction_id):

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                t.transaction_id,
                t.customer_id,
                c.account_no,
                c.name,
                t.transaction_type,
                t.amount,
                t.sender_account,
                t.receiver_account,
                t.sender_name,
                t.receiver_name,
                t.date,
                t.status
            FROM transactions t
            JOIN customers c
                ON t.customer_id = c.customer_id
            WHERE t.transaction_id = %s
            """,
            (transaction_id,)
        )

        transaction = cursor.fetchone()

        cursor.close()
        connection.close()

        if transaction is None:

            return jsonify({
                "status": "error",
                "message": "Transaction not found."
            }), 404

        return jsonify({
            "status": "success",
            "transaction_id": transaction[0],
            "customer_id": transaction[1],
            "account_no": transaction[2],
            "customer_name": transaction[3],
            "transaction_type": transaction[4],
            "amount": float(transaction[5]),
            "sender_account": transaction[6],
            "receiver_account": transaction[7],
            "sender_name": transaction[8],
            "receiver_name": transaction[9],
            "date": (
                transaction[10].strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if transaction[10]
                else ""
            ),
            "transaction_status": transaction[11]
        }), 200

    except psycopg2.Error as error:

        print("\nAdmin transaction search error:")
        print(error)

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to search transaction."
        }), 500

@app.route("/api/admin/transaction-filter", methods=["GET"])
def admin_transaction_filter_api():

    account_no = request.args.get("account_no")
    transaction_type = request.args.get("transaction_type")
    transaction_date = request.args.get("transaction_date")

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        query = """
            SELECT
                t.transaction_id,
                c.account_no,
                c.name,
                t.transaction_type,
                t.amount,
                t.sender_account,
                t.receiver_account,
                t.date,
                t.status
            FROM transactions t
            JOIN customers c
                ON t.customer_id = c.customer_id
            WHERE 1 = 1
        """

        parameters = []

        if account_no:

            query += """
                AND c.account_no = %s
            """

            parameters.append(account_no)

        if transaction_type:

            query += """
                AND t.transaction_type = %s
            """

            parameters.append(transaction_type)

        if transaction_date:

            query += """
                AND DATE(t.date) = %s
            """

            parameters.append(transaction_date)

        query += """
            ORDER BY t.date DESC
        """

        cursor.execute(
            query,
            tuple(parameters)
        )

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()

        transaction_list = []

        for transaction in transactions:

            transaction_list.append({

                "transaction_id":
                    transaction[0],

                "account_no":
                    transaction[1],

                "customer_name":
                    transaction[2],

                "transaction_type":
                    transaction[3],

                "amount":
                    float(transaction[4]),

                "sender_account":
                    transaction[5],

                "receiver_account":
                    transaction[6],

                "date":
                    (
                        transaction[7].strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if transaction[7]
                        else ""
                    ),

                "status":
                    transaction[8]
            })

        return jsonify({

            "status": "success",

            "total_transactions":
                len(transaction_list),

            "transactions":
                transaction_list

        }), 200

    except psycopg2.Error as error:

        print(
            "\nAdmin transaction filter error:"
        )

        print(error)

        connection.close()

        return jsonify({

            "status": "error",

            "message":
                "Unable to filter transactions."

        }), 500

@app.route("/api/admin/banking-summary", methods=["GET"])
def admin_banking_summary_api():

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*),
                COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type IN (
                'Deposit',
                'Initial Deposit'
            )
            AND status = 'SUCCESS'
            """
        )

        deposit_data = cursor.fetchone()

        total_deposit_transactions = deposit_data[0]
        total_deposit_amount = deposit_data[1]


        cursor.execute(
            """
            SELECT
                COUNT(*),
                COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Withdrawal'
            AND status = 'SUCCESS'
            """
        )

        withdrawal_data = cursor.fetchone()

        total_withdrawal_transactions = withdrawal_data[0]
        total_withdrawal_amount = withdrawal_data[1]


        cursor.execute(
            """
            SELECT
                COUNT(*),
                COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Transfer'
            AND status = 'SUCCESS'
            """
        )

        transfer_data = cursor.fetchone()

        total_transfer_transactions = transfer_data[0]
        total_transfer_amount = transfer_data[1]


        cursor.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            WHERE status = 'SUCCESS'
            """
        )

        total_successful_transactions = cursor.fetchone()[0]


        cursor.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            WHERE status != 'SUCCESS'
            """
        )

        total_failed_transactions = cursor.fetchone()[0]


        cursor.execute(
            """
            SELECT
                COALESCE(SUM(balance), 0)
            FROM customers
            WHERE status = 'Active'
            """
        )

        total_active_balance = cursor.fetchone()[0]


        cursor.close()
        connection.close()


        return jsonify({

            "status": "success",

            "total_deposit_transactions":
                total_deposit_transactions,

            "total_deposit_amount":
                float(total_deposit_amount),

            "total_withdrawal_transactions":
                total_withdrawal_transactions,

            "total_withdrawal_amount":
                float(total_withdrawal_amount),

            "total_transfer_transactions":
                total_transfer_transactions,

            "total_transfer_amount":
                float(total_transfer_amount),

            "total_successful_transactions":
                total_successful_transactions,

            "total_failed_transactions":
                total_failed_transactions,

            "total_active_balance":
                float(total_active_balance)

        }), 200


    except psycopg2.Error as error:

        print(
            "\nAdmin banking summary error:"
        )

        print(error)

        connection.close()

        return jsonify({

            "status": "error",

            "message":
                "Unable to retrieve banking summary."

        }), 500

@app.route("/api/change-password", methods=["POST"])
def change_password_api():

    data = request.get_json()

    account_no = data.get("account_no")
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if (
        not account_no
        or not current_password
        or not new_password
    ):

        return jsonify({
            "status": "error",
            "message": "All password fields are required."
        }), 400

    if len(new_password) < 6:

        return jsonify({
            "status": "error",
            "message": "New password must contain at least 6 characters."
        }), 400

    if current_password == new_password:

        return jsonify({
            "status": "error",
            "message": "New password must be different from the current password."
        }), 400

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT password_hash
            FROM customers
            WHERE account_no = %s
            """,
            (account_no,)
        )

        customer = cursor.fetchone()

        if customer is None:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Customer account not found."
            }), 404

        stored_password = customer[0]

        password_is_valid = False

        if stored_password and len(stored_password) == 64:

            current_password_hash = hashlib.sha256(
                current_password.encode("utf-8")
            ).hexdigest()

            if current_password_hash == stored_password:

                password_is_valid = True

        elif stored_password:

            try:

                password_is_valid = bcrypt.checkpw(
                    current_password.encode("utf-8"),
                    stored_password.encode("utf-8")
                )

            except (ValueError, TypeError):

                password_is_valid = False

        if not password_is_valid:

            cursor.close()
            connection.close()

            return jsonify({
                "status": "error",
                "message": "Current password is incorrect."
            }), 401

        new_password_hash = bcrypt.hashpw(
            new_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            """
            UPDATE customers
            SET password_hash = %s
            WHERE account_no = %s
            """,
            (
                new_password_hash,
                account_no
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "status": "success",
            "message": "Password changed successfully."
        }), 200

    except psycopg2.Error as error:

        print("\nChange password database error:")
        print(error)

        connection.rollback()
        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to change password."
        }), 500
@app.route("/api/transactions/<account_no>/date", methods=["GET"])
def customer_transactions_by_date_api(account_no):

    selected_date = request.args.get("date")

    if not selected_date:

        return jsonify({
            "status": "error",
            "message": "Transaction date is required."
        }), 400

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                t.transaction_id,
                t.transaction_type,
                t.amount,
                t.sender_account,
                t.receiver_account,
                t.date,
                t.status
            FROM transactions t
            JOIN customers c
                ON t.customer_id = c.customer_id
            WHERE c.account_no = %s
            AND DATE(t.date) = %s
            ORDER BY t.date DESC
            """,
            (
                account_no,
                selected_date
            )
        )

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()

        transaction_list = []

        for transaction in transactions:

            transaction_list.append({
                "transaction_id": transaction[0],
                "transaction_type": transaction[1],
                "amount": float(transaction[2]),
                "sender_account": transaction[3],
                "receiver_account": transaction[4],
                "date": (
                    transaction[5].strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if transaction[5]
                    else ""
                ),
                "status": transaction[6]
            })

        return jsonify({
            "status": "success",
            "transactions": transaction_list
        }), 200

    except psycopg2.Error as error:

        print("\nDate filter database error:")
        print(error)

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to filter transactions."
        }), 500
@app.route("/api/transactions/<account_no>/date-range", methods=["GET"])
def customer_transactions_by_date_range_api(account_no):

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not start_date or not end_date:

        return jsonify({
            "status": "error",
            "message": "Start date and end date are required."
        }), 400

    if start_date > end_date:

        return jsonify({
            "status": "error",
            "message": "Start date cannot be later than end date."
        }), 400

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                t.transaction_id,
                t.transaction_type,
                t.amount,
                t.sender_account,
                t.receiver_account,
                t.date,
                t.status
            FROM transactions t
            JOIN customers c
                ON t.customer_id = c.customer_id
            WHERE c.account_no = %s
            AND DATE(t.date) BETWEEN %s AND %s
            ORDER BY t.date DESC
            """,
            (
                account_no,
                start_date,
                end_date
            )
        )

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()

        transaction_list = []

        for transaction in transactions:

            transaction_list.append({
                "transaction_id": transaction[0],
                "transaction_type": transaction[1],
                "amount": float(transaction[2]),
                "sender_account": transaction[3],
                "receiver_account": transaction[4],
                "date": (
                    transaction[5].strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if transaction[5]
                    else ""
                ),
                "status": transaction[6]
            })

        return jsonify({
            "status": "success",
            "transactions": transaction_list
        }), 200

    except psycopg2.Error as error:

        print("\nDate range filter database error:")
        print(error)

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to filter transactions."
        }), 500
@app.route("/api/transactions/<account_no>/type", methods=["GET"])
def customer_transactions_by_type_api(account_no):

    transaction_type = request.args.get("type")

    if not transaction_type:

        return jsonify({
            "status": "error",
            "message": "Transaction type is required."
        }), 400

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                t.transaction_id,
                t.transaction_type,
                t.amount,
                t.sender_account,
                t.receiver_account,
                t.date,
                t.status
            FROM transactions t
            JOIN customers c
                ON t.customer_id = c.customer_id
            WHERE c.account_no = %s
            AND t.transaction_type = %s
            ORDER BY t.date DESC
            """,
            (
                account_no,
                transaction_type
            )
        )

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()

        transaction_list = []

        for transaction in transactions:

            transaction_list.append({
                "transaction_id": transaction[0],
                "transaction_type": transaction[1],
                "amount": float(transaction[2]),
                "sender_account": transaction[3],
                "receiver_account": transaction[4],
                "date": (
                    transaction[5].strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if transaction[5]
                    else ""
                ),
                "status": transaction[6]
            })

        return jsonify({
            "status": "success",
            "transactions": transaction_list
        }), 200

    except psycopg2.Error as error:

        print("\nTransaction type filter database error:")
        print(error)

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to filter transactions."
        }), 500
@app.route("/api/transactions/<account_no>/type-date", methods=["GET"])
def customer_transactions_by_type_date_api(account_no):

    transaction_type = request.args.get("type")
    transaction_date = request.args.get("date")

    if not transaction_type or not transaction_date:

        return jsonify({
            "status": "error",
            "message": "Transaction type and date are required."
        }), 400

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                t.transaction_id,
                t.transaction_type,
                t.amount,
                t.sender_account,
                t.receiver_account,
                t.date,
                t.status
            FROM transactions t
            JOIN customers c
                ON t.customer_id = c.customer_id
            WHERE c.account_no = %s
            AND t.transaction_type = %s
            AND DATE(t.date) = %s
            ORDER BY t.date DESC
            """,
            (
                account_no,
                transaction_type,
                transaction_date
            )
        )

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()

        transaction_list = []

        for transaction in transactions:

            transaction_list.append({
                "transaction_id": transaction[0],
                "transaction_type": transaction[1],
                "amount": float(transaction[2]),
                "sender_account": transaction[3],
                "receiver_account": transaction[4],
                "date": (
                    transaction[5].strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if transaction[5]
                    else ""
                ),
                "status": transaction[6]
            })

        return jsonify({
            "status": "success",
            "transactions": transaction_list
        }), 200

    except psycopg2.Error as error:

        print("\nType and date filter database error:")
        print(error)

        connection.close()

        return jsonify({
            "status": "error",
            "message": "Unable to filter transactions."
        }), 500
@app.route("/api/transactions/<account_no>/sort", methods=["GET"])
def customer_transactions_sort_api(account_no):

    sort_option = request.args.get("sort")

    if not sort_option:

        return jsonify({
            "status": "error",
            "message": "Sorting option is required."
        }), 400


    sort_mapping = {

        "newest":
            "t.date DESC",

        "oldest":
            "t.date ASC",

        "amount-high":
            "t.amount DESC",

        "amount-low":
            "t.amount ASC"

    }


    if sort_option not in sort_mapping:

        return jsonify({
            "status": "error",
            "message": "Invalid sorting option."
        }), 400


    order_by = sort_mapping[sort_option]


    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "status": "error",
            "message": "Database connection failed."
        }), 500


    try:

        cursor = connection.cursor()

        query = f"""
            SELECT
                t.transaction_id,
                t.transaction_type,
                t.amount,
                t.sender_account,
                t.receiver_account,
                t.date,
                t.status
            FROM transactions t
            JOIN customers c
                ON t.customer_id = c.customer_id
            WHERE c.account_no = %s
            ORDER BY {order_by}
        """

        cursor.execute(
            query,
            (account_no,)
        )

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()


        transaction_list = []


        for transaction in transactions:

            transaction_list.append({

                "transaction_id":
                    transaction[0],

                "transaction_type":
                    transaction[1],

                "amount":
                    float(transaction[2]),

                "sender_account":
                    transaction[3],

                "receiver_account":
                    transaction[4],

                "date":
                    (
                        transaction[5].strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if transaction[5]
                        else ""
                    ),

                "status":
                    transaction[6]

            })


        return jsonify({

            "status":
                "success",

            "transactions":
                transaction_list

        }), 200


    except psycopg2.Error as error:

        print(
            "\nTransaction sorting database error:"
        )

        print(error)

        connection.close()


        return jsonify({

            "status":
                "error",

            "message":
                "Unable to sort transactions."

        }), 500

@app.route("/api/transactions/<account_no>/summary", methods=["GET"])
def customer_transaction_summary_api(account_no):

    conn = None

    try:
        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) AS total_transactions,
                COALESCE(SUM(CASE
                    WHEN transaction_type IN ('Deposit', 'Initial Deposit', 'Transfer Received')
                    THEN amount
                    ELSE 0
                END), 0) AS total_credits,
                COALESCE(SUM(CASE
                    WHEN transaction_type IN ('Withdrawal', 'Transfer Sent')
                    THEN amount
                    ELSE 0
                END), 0) AS total_debits
            FROM transactions t
            JOIN customers c
                ON t.customer_id = c.customer_id
            WHERE c.account_no = %s
        """, (account_no,))

        result = cursor.fetchone()

        cursor.close()

        return jsonify({
            "status": "success",
            "account_no": int(account_no),
            "total_transactions": result[0],
            "total_credits": float(result[1]),
            "total_debits": float(result[2])
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:

        if conn:
            conn.close()

@app.route("/api/transactions/<account_no>/search", methods=["GET"])
def customer_transaction_search_api(account_no):

    search_text = request.args.get("q", "").strip()

    if not search_text:
        return jsonify({
            "status": "error",
            "message": "Please enter a transaction ID."
        }), 400

    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                t.transaction_id,
                t.transaction_type,
                t.amount,
                t.sender_account,
                t.receiver_account,
                t.date,
                t.status
            FROM transactions t
            JOIN customers c
                ON t.customer_id = c.customer_id
            WHERE c.account_no = %s
              AND t.transaction_id ILIKE %s
            ORDER BY t.date DESC
        """, (account_no, f"%{search_text}%"))

        rows = cursor.fetchall()

        cursor.close()

        transactions = []

        for row in rows:
            transactions.append({
                "transaction_id": row[0],
                "transaction_type": row[1],
                "amount": float(row[2]),
                "sender_account": row[3],
                "receiver_account": row[4],
                "date": row[5].isoformat() if row[5] else None,
                "status": row[6]
            })

        return jsonify({
            "status": "success",
            "transactions": transactions
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:

        if conn:
            conn.close()

from io import StringIO
import csv

@app.route("/api/transactions/<account_no>/export", methods=["GET"])
def export_account_statement_api(account_no):

    conn = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                t.transaction_id,
                t.transaction_type,
                t.amount,
                t.sender_account,
                t.receiver_account,
                t.date,
                t.status
            FROM transactions t
            JOIN customers c
                ON t.customer_id = c.customer_id
            WHERE c.account_no = %s
            ORDER BY t.date DESC
        """, (account_no,))

        rows = cursor.fetchall()

        cursor.close()

        output = StringIO()

        writer = csv.writer(output)

        writer.writerow([
            "Transaction ID",
            "Transaction Type",
            "Amount",
            "Sender Account",
            "Receiver Account",
            "Date",
            "Status"
        ])

        for row in rows:

            writer.writerow([
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6]
            ])

        output.seek(0)

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={
                "Content-Disposition":
                    f"attachment; filename=account_statement_{account_no}.csv"
            }
        )

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:

        if conn:
            conn.close()
# =========================================
# START SERVER
# =========================================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 50001)),
        debug=False
    )