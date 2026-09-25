# Smart Banking Management System

A full-stack banking management system built with Python, Flask, PostgreSQL, HTML, CSS, and JavaScript.

## Features

### Customer Features

- Customer registration
- Secure customer login
- Dashboard
- Balance checking
- Deposit
- Withdrawal
- Money transfer
- Transaction history
- Transaction search
- Transaction filtering
- Transaction sorting
- Account statement export
- Notifications
- Profile management
- Account status
- Change password
- Logout

### Admin Features

- Admin login
- Admin dashboard
- Customer search
- Customer details
- Account status management
- Transaction search
- Transaction filtering
- Banking summary
- System health monitoring
- Admin activity log
- Admin logout

## Technologies Used

- Python
- Flask
- PostgreSQL
- HTML5
- CSS3
- JavaScript
- REST APIs
- psycopg2
- bcrypt
- python-dotenv

## Security

- Database credentials are stored using environment variables.
- .env is excluded from Git using .gitignore.
- Passwords are securely hashed.
- Customer and admin pages include access protection.

## Database

#The application uses PostgreSQL with tables for:

- Customers
- Transactions
- Notifications
- Admin Activuty



## Project Structure

```text
Smart Banking Management System/
│
├── backend.py
├── main.py
├── test_api.py
├── test_database.py
├── admin_activity.json
├── .env
├── .gitignore
│
├── data/
│
└── website/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── balance.html
    ├── deposit.html
    ├── withdraw.html
    ├── transactions.html
    ├── transfer.html
    ├── notifications.html
    ├── profile.html
    ├── account-status.html
    ├── change-password.html
    ├── admin-login.html
    ├── admin-dashboard.html
    ├── admin-customer-search.html
    ├── admin-customer-details.html
    ├── admin-transaction-search.html
    ├── admin-transaction-filter.html
    ├── admin-banking-summary.html
    ├── admin-activity-log.html
    ├── admin-system-health.html
    ├── style.css
    ├── script.js
    └── assets/






