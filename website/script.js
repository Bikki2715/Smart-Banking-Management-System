/* =========================================
   SMARTBANK - JAVASCRIPT
========================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =====================================
       NAVIGATION LINK SMOOTH SCROLL
    ===================================== */

    const navLinks = document.querySelectorAll(
        '.nav-links a[href^="#"]'
    );

    navLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            event.preventDefault();

            const targetId = this.getAttribute("href");

            const targetSection =
                document.querySelector(targetId);

            if (targetSection) {

                targetSection.scrollIntoView({
                    behavior: "smooth"
                });

            }

        });

    });


    /* =====================================
       HERO BUTTON EFFECT
    ===================================== */

    const buttons = document.querySelectorAll(
        ".primary-btn, .secondary-btn"
    );

    buttons.forEach(function (button) {

        button.addEventListener("click", function () {

            this.style.transform = "scale(0.97)";

            setTimeout(() => {

                this.style.transform = "";

            }, 120);

        });

    });


    /* =====================================
       SERVICE CARD ANIMATION
    ===================================== */

    const serviceCards =
        document.querySelectorAll(".service-card");

    serviceCards.forEach(function (card) {

        card.addEventListener("mouseenter", function () {

            this.style.cursor = "pointer";

        });

    });


    /* =====================================
       CURRENT YEAR IN FOOTER
    ===================================== */

    const footerYear =
        document.querySelector(".footer-content span");

    if (footerYear) {

        const currentYear =
            new Date().getFullYear();

        footerYear.textContent =
            `© ${currentYear} SmartBank. All Rights Reserved.`;

    }


    /* =====================================
       PAGE LOAD ANIMATION
    ===================================== */

    document.body.classList.add("page-loaded");

});
/* =========================================
   LOGIN PAGE INTERACTIONS
========================================= */

const loginForm = document.getElementById("loginForm");

const passwordInput =
    document.getElementById("password");

const togglePassword =
    document.getElementById("togglePassword");

const accountNumberInput =
    document.getElementById("accountNumber");


/* =========================================
   SHOW / HIDE PASSWORD
========================================= */

if (togglePassword && passwordInput) {

    togglePassword.addEventListener(
        "click",
        function () {

            if (passwordInput.type === "password") {

                passwordInput.type = "text";

                togglePassword.textContent = "🙈";

            } else {

                passwordInput.type = "password";

                togglePassword.textContent = "👁️";
            }

        }
    );
}


/* =========================================
   ACCOUNT NUMBER VALIDATION
========================================= */

if (accountNumberInput) {

    accountNumberInput.addEventListener(
        "input",
        function () {

            this.value =
                this.value.replace(/\D/g, "");

        }
    );
}



/* =========================================
   REAL LOGIN - FLASK + POSTGRESQL
========================================= */

if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const accountNumber =
                accountNumberInput.value.trim();

            const password =
                passwordInput.value.trim();


            /* ACCOUNT NUMBER */

            if (!accountNumber) {

                alert(
                    "Please enter your account number."
                );

                accountNumberInput.focus();

                return;
            }


            if (!/^\d{6,10}$/.test(accountNumber)) {

                alert(
                    "Please enter a valid account number."
                );

                accountNumberInput.focus();

                return;
            }


            /* PASSWORD */

            if (!password) {

                alert(
                    "Please enter your password."
                );

                passwordInput.focus();

                return;
            }


            if (password.length < 4) {

                alert(
                    "Password must contain at least 4 characters."
                );

                passwordInput.focus();

                return;
            }


            /* CONNECT TO FLASK BACKEND */

            try {

                const response = await fetch(
                    "/api/login",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            account_number: accountNumber,
                            password: password
                        })
                    }
                );


                const data = await response.json();


                if (response.ok) {

                    /* =================================
                    SAVE CUSTOMER LOGIN INFORMATION
                    ================================= */

                    sessionStorage.setItem(
                        "customerName",
                        data.name
                    );

                    sessionStorage.setItem(
                        "accountNumber",
                        data.account_no
                    );


                    /* =================================
                    GO TO CUSTOMER DASHBOARD
                    ================================= */

                    window.location.href =
                        "dashboard.html";

                } 
                else {

                    alert(
                        data.message ||
                        "Login failed."
                    );
                }


            } catch (error) {

                console.error(
                    "Login Error:",
                    error
                );

                alert(
                    "Unable to connect to SmartBank server.\n\n" +
                    "Please make sure backend.py is running."
                );
            }

        }
    );
}


/* =========================================
   FORGOT PASSWORD
========================================= */

const forgotPassword =
    document.getElementById("forgotPassword");

if (forgotPassword) {

    forgotPassword.addEventListener(
        "click",
        function (event) {

            event.preventDefault();

            alert(
                "Forgot Password functionality will be connected to the banking backend later."
            );

        }
    );
}
/* =========================================
   REGISTRATION PAGE INTERACTIONS
========================================= */

const registerForm =
    document.getElementById("registerForm");

const fullNameInput =
    document.getElementById("fullName");

const mobileNumberInput =
    document.getElementById("mobileNumber");

const emailInput =
    document.getElementById("email");

const aadhaarInput =
    document.getElementById("aadhaar");

const registerPasswordInput =
    document.getElementById("registerPassword");

const confirmPasswordInput =
    document.getElementById("confirmPassword");

const toggleRegisterPassword =
    document.getElementById("toggleRegisterPassword");

const toggleConfirmPassword =
    document.getElementById("toggleConfirmPassword");


/* =========================================
   SHOW / HIDE PASSWORD
========================================= */

if (
    toggleRegisterPassword &&
    registerPasswordInput
) {

    toggleRegisterPassword.addEventListener(
        "click",
        function () {

            if (
                registerPasswordInput.type ===
                "password"
            ) {

                registerPasswordInput.type =
                    "text";

                toggleRegisterPassword.textContent =
                    "🙈";

            } else {

                registerPasswordInput.type =
                    "password";

                toggleRegisterPassword.textContent =
                    "👁️";
            }

        }
    );
}


/* =========================================
   SHOW / HIDE CONFIRM PASSWORD
========================================= */

if (
    toggleConfirmPassword &&
    confirmPasswordInput
) {

    toggleConfirmPassword.addEventListener(
        "click",
        function () {

            if (
                confirmPasswordInput.type ===
                "password"
            ) {

                confirmPasswordInput.type =
                    "text";

                toggleConfirmPassword.textContent =
                    "🙈";

            } else {

                confirmPasswordInput.type =
                    "password";

                toggleConfirmPassword.textContent =
                    "👁️";
            }

        }
    );
}


/* =========================================
   MOBILE NUMBER VALIDATION
========================================= */

if (mobileNumberInput) {

    mobileNumberInput.addEventListener(
        "input",
        function () {

            this.value =
                this.value.replace(/\D/g, "");

        }
    );
}


/* =========================================
   AADHAAR VALIDATION
========================================= */

if (aadhaarInput) {

    aadhaarInput.addEventListener(
        "input",
        function () {

            this.value =
                this.value.replace(/\D/g, "");

        }
    );
}



/* =========================================
   REAL REGISTRATION - FLASK + POSTGRESQL
========================================= */

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const name =
                fullNameInput.value.trim();

            const mobile =
                mobileNumberInput.value.trim();

            const email =
                emailInput.value.trim();

            const aadhaar =
                aadhaarInput.value.trim();

            const password =
                registerPasswordInput.value;

            const confirm =
                confirmPasswordInput.value;


            /* =================================
               VALIDATION
            ================================= */

            if (!name) {

                alert(
                    "Please enter your full name."
                );

                fullNameInput.focus();

                return;
            }


            if (name.length < 3) {

                alert(
                    "Full name must contain at least 3 characters."
                );

                fullNameInput.focus();

                return;
            }


            if (!/^\d{10}$/.test(mobile)) {

                alert(
                    "Mobile number must contain exactly 10 digits."
                );

                mobileNumberInput.focus();

                return;
            }


            if (!email) {

                alert(
                    "Please enter your email address."
                );

                emailInput.focus();

                return;
            }


            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {

                alert(
                    "Please enter a valid email address."
                );

                emailInput.focus();

                return;
            }


            if (!/^\d{12}$/.test(aadhaar)) {

                alert(
                    "Aadhaar number must contain exactly 12 digits."
                );

                aadhaarInput.focus();

                return;
            }


            if (password.length < 4) {

                alert(
                    "Password must contain at least 4 characters."
                );

                registerPasswordInput.focus();

                return;
            }


            if (password !== confirm) {

                alert(
                    "Passwords do not match."
                );

                confirmPasswordInput.focus();

                return;
            }


            /* =================================
               SEND DATA TO FLASK BACKEND
            ================================= */

            try {

                const response = await fetch(
                    "/api/register",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({

                            name: name,

                            mobile: mobile,

                            email: email,

                            aadhaar: aadhaar,

                            password: password

                        })
                    }
                );


                const data =
                    await response.json();


                /* =================================
                   REGISTRATION SUCCESS
                ================================= */

                if (response.ok) {

                    alert(
                        "Account created successfully!\n\n" +
                        "Account Number: " +
                        data.account_no +
                        "\n\n" +
                        "Welcome, " +
                        data.name +
                        "!"
                    );


                    window.location.href =
                        "login.html";

                }


                /* =================================
                   REGISTRATION ERROR
                ================================= */

                else {

                    alert(
                        data.message ||
                        "Registration failed."
                    );

                }


            } catch (error) {

                console.error(
                    "Registration Error:",
                    error
                );


                alert(
                    "Unable to connect to SmartBank server.\n\n" +
                    "Please make sure backend.py is running."
                );

            }

        }
    );

}
/* =========================================
   FORGOT PASSWORD PAGE
========================================= */

const forgotPasswordForm =
    document.getElementById("forgotPasswordForm");

const forgotEmailInput =
    document.getElementById("forgotEmail");


/* =========================================
   FORGOT PASSWORD FORM VALIDATION
========================================= */

if (forgotPasswordForm) {

    forgotPasswordForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            const email =
                forgotEmailInput.value.trim();


            /* =================================
               EMAIL VALIDATION
            ================================= */

            if (!email) {

                alert(
                    "Please enter your registered email address."
                );

                forgotEmailInput.focus();

                return;
            }


            if (
                !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
            ) {

                alert(
                    "Please enter a valid email address."
                );

                forgotEmailInput.focus();

                return;
            }


            /* =================================
               TEMPORARY MESSAGE
            ================================= */

            alert(
                "Email address validated successfully.\n\n" +
                "Verification code sending will be connected to the backend in a later step."
            );

        }
    );
}
/* =========================================
   VERIFICATION CODE PAGE
========================================= */

const verificationForm =
    document.getElementById("verificationForm");

const verificationCodeInput =
    document.getElementById("verificationCode");

const resendCode =
    document.getElementById("resendCode");


/* =========================================
   VERIFICATION CODE INPUT
========================================= */

if (verificationCodeInput) {

    verificationCodeInput.addEventListener(
        "input",
        function () {

            // Allow numbers only
            this.value =
                this.value.replace(/\D/g, "");

        }
    );
}


/* =========================================
   VERIFY CODE
========================================= */

if (verificationForm) {

    verificationForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            const code =
                verificationCodeInput.value.trim();


            /* =================================
               EMPTY CODE
            ================================= */

            if (!code) {

                alert(
                    "Please enter the verification code."
                );

                verificationCodeInput.focus();

                return;
            }


            /* =================================
               CODE LENGTH
            ================================= */

            if (!/^\d{6}$/.test(code)) {

                alert(
                    "Verification code must contain exactly 6 digits."
                );

                verificationCodeInput.focus();

                return;
            }


            /* =================================
               TEMPORARY MESSAGE
            ================================= */

            alert(
                "Verification code format is valid.\n\n" +
                "Actual email verification will be connected to the backend later."
            );

        }
    );
}


/* =========================================
   RESEND CODE
========================================= */

if (resendCode) {

    resendCode.addEventListener(
        "click",
        function (event) {

            event.preventDefault();

            alert(
                "A new verification code will be sent to your registered email when the backend is connected."
            );

        }
    );
}
/* =========================================
   NEW PASSWORD PAGE
========================================= */

const newPasswordForm =
    document.getElementById("newPasswordForm");

const newPasswordInput =
    document.getElementById("newPassword");

const confirmNewPasswordInput =
    document.getElementById("confirmNewPassword");

const toggleNewPassword =
    document.getElementById("toggleNewPassword");

const toggleConfirmNewPassword =
    document.getElementById("toggleConfirmNewPassword");


/* =========================================
   SHOW / HIDE NEW PASSWORD
========================================= */

if (toggleNewPassword && newPasswordInput) {

    toggleNewPassword.addEventListener(
        "click",
        function () {

            if (newPasswordInput.type === "password") {

                newPasswordInput.type = "text";

                toggleNewPassword.textContent = "🙈";

            } else {

                newPasswordInput.type = "password";

                toggleNewPassword.textContent = "👁️";

            }

        }
    );
}


/* =========================================
   SHOW / HIDE CONFIRM PASSWORD
========================================= */

if (
    toggleConfirmNewPassword &&
    confirmNewPasswordInput
) {

    toggleConfirmNewPassword.addEventListener(
        "click",
        function () {

            if (
                confirmNewPasswordInput.type ===
                "password"
            ) {

                confirmNewPasswordInput.type =
                    "text";

                toggleConfirmNewPassword.textContent =
                    "🙈";

            } else {

                confirmNewPasswordInput.type =
                    "password";

                toggleConfirmNewPassword.textContent =
                    "👁️";

            }

        }
    );
}


/* =========================================
   NEW PASSWORD VALIDATION
========================================= */

if (newPasswordForm) {

    newPasswordForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            const newPassword =
                newPasswordInput.value;

            const confirmPassword =
                confirmNewPasswordInput.value;


            /* =================================
               EMPTY PASSWORD
            ================================= */

            if (!newPassword) {

                alert(
                    "Please enter your new password."
                );

                newPasswordInput.focus();

                return;
            }


            /* =================================
               PASSWORD LENGTH
            ================================= */

            if (newPassword.length < 4) {

                alert(
                    "Password must contain at least 4 characters."
                );

                newPasswordInput.focus();

                return;
            }


            /* =================================
               CONFIRM PASSWORD
            ================================= */

            if (!confirmPassword) {

                alert(
                    "Please confirm your new password."
                );

                confirmNewPasswordInput.focus();

                return;
            }


            /* =================================
               MATCH PASSWORDS
            ================================= */

            if (newPassword !== confirmPassword) {

                alert(
                    "New passwords do not match."
                );

                confirmNewPasswordInput.focus();

                return;
            }


            /* =================================
               TEMPORARY SUCCESS
            ================================= */

            alert(
                "New password validated successfully.\n\n" +
                "Password update will be connected to PostgreSQL after email verification is connected."
            );

        }
    );
}
/* =========================================
   CUSTOMER DASHBOARD
========================================= */

const customerNameElement =
    document.getElementById("customerName");

const accountNumberElement =
    document.getElementById("accountNumber");

const accountBalanceElement =
    document.getElementById("accountBalance");

const accountStatusElement =
    document.getElementById("accountStatus");


/* =========================================
   LOAD CUSTOMER INFORMATION
========================================= */

if (
    customerNameElement &&
    accountNumberElement
) {

    const customerName =
        sessionStorage.getItem("customerName");

    const accountNumber =
        sessionStorage.getItem("accountNumber");


    /* =====================================
       CHECK LOGIN SESSION
    ===================================== */

    if (!customerName || !accountNumber) {

        alert(
            "Please login to access your dashboard."
        );

        window.location.href =
            "login.html";

    } else {

        customerNameElement.textContent =
            customerName;

        accountNumberElement.textContent =
            accountNumber;

    }

}


/* =========================================
   LOGOUT
========================================= */

const logoutBtn =
    document.getElementById("logoutBtn");


if (logoutBtn) {

    logoutBtn.addEventListener(
        "click",
        function (event) {

            event.preventDefault();


            sessionStorage.removeItem(
                "customerName"
            );

            sessionStorage.removeItem(
                "accountNumber"
            );


            alert(
                "You have been logged out successfully."
            );


            window.location.href =
                "login.html";

        }
    );

}
/* =========================================
   FETCH REAL CUSTOMER DASHBOARD DATA
========================================= */

if (
    customerNameElement &&
    accountNumberElement
) {

    const accountNumber =
        sessionStorage.getItem("accountNumber");


    if (accountNumber) {

        fetch(
            "/api/customer/" +
            accountNumber
        )

        .then(function (response) {

            return response.json();

        })

        .then(function (data) {

            if (data.status === "success") {

                /* CUSTOMER NAME */

                customerNameElement.textContent =
                    data.name;


                /* ACCOUNT NUMBER */

                accountNumberElement.textContent =
                    data.account_no;


                /* BALANCE */

                if (accountBalanceElement) {

                    accountBalanceElement.textContent =
                        "₹" +
                        Number(data.balance).toFixed(2);

                }


                /* ACCOUNT STATUS */

                if (accountStatusElement) {

                    accountStatusElement.textContent =
                        data.account_status;

                }

            } else {

                alert(
                    data.message ||
                    "Unable to load customer information."
                );

            }

        })

        .catch(function (error) {

            console.error(
                "Dashboard Error:",
                error
            );

            alert(
                "Unable to connect to SmartBank server."
            );

        });

    }

}
/* =========================================
   CHECK BALANCE NAVIGATION
========================================= */

const checkBalanceCard =
    document.getElementById("checkBalanceCard");

if (checkBalanceCard) {

    checkBalanceCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "balance.html";

        }
    );

}
/* =========================================
   BALANCE PAGE - REAL CUSTOMER DATA
========================================= */

const balanceAmount =
    document.getElementById("balanceAmount");

const balanceAccountNumber =
    document.getElementById("balanceAccountNumber");

const balanceAccountStatus =
    document.getElementById("balanceAccountStatus");


if (
    balanceAmount &&
    balanceAccountNumber &&
    balanceAccountStatus
) {

    const accountNumber =
        sessionStorage.getItem("accountNumber");


    if (!accountNumber) {

        alert(
            "Please login to access your account."
        );

        window.location.href =
            "login.html";

    } else {

        fetch(
            "/api/customer/" +
            accountNumber
        )

        .then(function (response) {

            return response.json();

        })

        .then(function (data) {

            if (data.status === "success") {

                balanceAccountNumber.textContent =
                    data.account_no;


                balanceAmount.textContent =
                    "₹" +
                    Number(data.balance).toFixed(2);


                balanceAccountStatus.textContent =
                    data.account_status;

            } else {

                alert(
                    data.message ||
                    "Unable to load account information."
                );

            }

        })

        .catch(function (error) {

            console.error(
                "Balance Page Error:",
                error
            );

            alert(
                "Unable to connect to SmartBank server."
            );

        });

    }

}
/* =========================================
   DEPOSIT MONEY NAVIGATION
========================================= */

const depositCard =
    document.getElementById("depositCard");

if (depositCard) {

    depositCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "deposit.html";

        }
    );

}
/* =========================================
   DEPOSIT FORM
========================================= */

const depositForm =
    document.getElementById("depositForm");

const depositAmountInput =
    document.getElementById("depositAmount");

const depositAccountNumber =
    document.getElementById("depositAccountNumber");

const depositMessage =
    document.getElementById("depositMessage");


if (depositForm) {

    const accountNumber =
        sessionStorage.getItem("accountNumber");


    if (!accountNumber) {

        alert(
            "Please login to access your account."
        );

        window.location.href =
            "login.html";

    } else {

        if (depositAccountNumber) {

            depositAccountNumber.textContent =
                accountNumber;

        }


        depositForm.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();


                const amount =
                    depositAmountInput.value.trim();


                /* VALIDATE AMOUNT */

                if (!amount) {

                    alert(
                        "Please enter a deposit amount."
                    );

                    depositAmountInput.focus();

                    return;
                }


                if (Number(amount) <= 0) {

                    alert(
                        "Deposit amount must be greater than zero."
                    );

                    depositAmountInput.focus();

                    return;
                }


                try {

                    const response =
                        await fetch(
                            "/api/deposit",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({
                                    account_no:
                                        accountNumber,

                                    amount:
                                        amount
                                })
                            }
                        );


                    const data =
                        await response.json();


                    if (response.ok) {

                        alert(
                            "Deposit successful!\n\n" +

                            "Amount: ₹" +
                            Number(data.amount).toFixed(2) +

                            "\nTransaction ID: " +
                            data.transaction_id +

                            "\nNew Balance: ₹" +
                            Number(data.new_balance).toFixed(2)
                        );


                        depositAmountInput.value =
                            "";


                        if (depositMessage) {

                            depositMessage.textContent =
                                "Deposit completed successfully.";

                        }

                    } else {

                        alert(
                            data.message ||
                            "Deposit failed."
                        );

                    }

                } catch (error) {

                    console.error(
                        "Deposit Error:",
                        error
                    );

                    alert(
                        "Unable to connect to SmartBank server."
                    );

                }

            }
        );

    }

}
/* =========================================
   WITHDRAW MONEY NAVIGATION
========================================= */

const withdrawCard =
    document.getElementById("withdrawCard");

if (withdrawCard) {

    withdrawCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "withdraw.html";

        }
    );

}
/* =========================================
   WITHDRAW MONEY FORM
========================================= */

const withdrawForm =
    document.getElementById("withdrawForm");

const withdrawAmountInput =
    document.getElementById("withdrawAmount");

const withdrawAccountNumberElement =
    document.getElementById("withdrawAccountNumber");

const withdrawCurrentBalanceElement =
    document.getElementById("withdrawCurrentBalance");

const withdrawMessage =
    document.getElementById("withdrawMessage");


if (withdrawForm) {

    const accountNumber =
        sessionStorage.getItem("accountNumber");

    if (!accountNumber) {

        alert(
            "Please login to withdraw money."
        );

        window.location.href =
            "login.html";

    } else {

        withdrawAccountNumberElement.textContent =
            accountNumber;


        // Get current balance
        fetch(
            `http://127.0.0.1:50001/api/customer/${accountNumber}`
        )
        .then(response => response.json())
        .then(data => {

            if (data.status === "success") {

                withdrawCurrentBalanceElement.textContent =
                    "₹" + Number(data.balance).toFixed(2);

            }

        })
        .catch(error => {

            console.error(
                "Balance Error:",
                error
            );

        });
    }


    withdrawForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const amount =
                withdrawAmountInput.value.trim();


            if (!amount) {

                alert(
                    "Please enter the withdrawal amount."
                );

                withdrawAmountInput.focus();

                return;
            }


            const numericAmount =
                Number(amount);


            if (
                isNaN(numericAmount) ||
                numericAmount <= 0
            ) {

                alert(
                    "Please enter a valid withdrawal amount."
                );

                withdrawAmountInput.focus();

                return;
            }


            try {

                const response =
                    await fetch(
                        "/api/withdraw",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                account_no:
                                    accountNumber,

                                amount:
                                    numericAmount
                            })
                        }
                    );


                const data =
                    await response.json();


                if (response.ok) {

                    alert(
                        "Withdrawal successful!\n\n" +

                        "Amount: ₹" +
                        Number(data.amount).toFixed(2) +

                        "\nTransaction ID: " +
                        data.transaction_id +

                        "\nNew Balance: ₹" +
                        Number(data.new_balance).toFixed(2)
                    );


                    withdrawMessage.textContent =
                        "Withdrawal successful.";


                    withdrawAmountInput.value = "";


                    withdrawCurrentBalanceElement.textContent =
                        "₹" +
                        Number(data.new_balance).toFixed(2);

                } else {

                    alert(
                        data.message ||
                        "Withdrawal failed."
                    );


                    withdrawMessage.textContent =
                        data.message ||
                        "Withdrawal failed.";
                }

            } catch (error) {

                console.error(
                    "Withdrawal Error:",
                    error
                );


                alert(
                    "Unable to connect to SmartBank server.\n\n" +
                    "Please make sure backend.py is running."
                );
            }
        }
    );
}
/* =========================================
   TRANSACTIONS NAVIGATION
========================================= */

const transactionsCard =
    document.getElementById("transactionsCard");

if (transactionsCard) {

    transactionsCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "transactions.html";

        }
    );

}
/* =========================================
   TRANSACTION HISTORY DATA
========================================= */

const transactionList =
    document.getElementById("transactionList");

const transactionAccountNumberElement =
    document.getElementById("transactionAccountNumber");

const transactionBalanceElement =
    document.getElementById("transactionBalance");

const transactionCountElement =
    document.getElementById("transactionCount");


if (transactionList) {

    const accountNumber =
        sessionStorage.getItem("accountNumber");


    if (!accountNumber) {

        alert(
            "Please login to view your transactions."
        );

        window.location.href =
            "login.html";

    } else {

        transactionAccountNumberElement.textContent =
            accountNumber;


        fetch(
            `http://127.0.0.1:50001/api/transactions/${accountNumber}`
        )
        .then(response => response.json())
        .then(data => {

            if (data.status === "success") {

                transactionBalanceElement.textContent =
                    "₹" +
                    Number(data.balance).toFixed(2);


                transactionCountElement.textContent =
                    data.transactions.length;


                if (
                    data.transactions.length === 0
                ) {

                    transactionList.innerHTML =
                        "<p>No transactions found.</p>";

                    return;
                }


                transactionList.innerHTML = "";


                data.transactions.forEach(
                    function (transaction) {

                        const transactionCard =
                            document.createElement("div");

                        transactionCard.className =
                            "transaction-card";


                        transactionCard.innerHTML = `

                            <div class="transaction-icon">
                                💳
                            </div>

                            <div class="transaction-details">

                                <h3>
                                    ${transaction.transaction_type}
                                </h3>

                                <p>
                                    Transaction ID:
                                    ${transaction.transaction_id}
                                </p>

                                <p>
                                    Date:
                                    ${transaction.date}
                                </p>

                            </div>

                            <div class="transaction-amount">

                                <strong>
                                    ₹${Number(transaction.amount).toFixed(2)}
                                </strong>

                                <span>
                                    ${transaction.status}
                                </span>

                            </div>

                        `;


                        transactionList.appendChild(
                            transactionCard
                        );

                    }
                );

            } else {

                transactionList.innerHTML =
                    `<p>${data.message || "Unable to load transactions."}</p>`;

            }

        })
        .catch(error => {

            console.error(
                "Transaction Error:",
                error
            );

            transactionList.innerHTML =
                "<p>Unable to connect to SmartBank server.</p>";

        });

    }

}
/* =========================================
   NOTIFICATIONS NAVIGATION
========================================= */

const notificationsCard =
    document.getElementById("notificationsCard");

if (notificationsCard) {

    notificationsCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "notifications.html";

        }
    );

}
/* =========================================
   CUSTOMER NOTIFICATIONS DATA
========================================= */

const notificationList =
    document.getElementById("notificationList");

const notificationAccountNumberElement =
    document.getElementById("notificationAccountNumber");

const notificationCountElement =
    document.getElementById("notificationCount");

const unreadNotificationCountElement =
    document.getElementById("unreadNotificationCount");


if (notificationList) {

    const accountNumber =
        sessionStorage.getItem("accountNumber");

    if (!accountNumber) {

        alert(
            "Please login to view your notifications."
        );

        window.location.href =
            "login.html";

    } else {

        notificationAccountNumberElement.textContent =
            accountNumber;

        fetch(
            `http://127.0.0.1:50001/api/notifications/${accountNumber}`
        )
        .then(response => response.json())
        .then(data => {

            if (data.status === "success") {

                notificationCountElement.textContent =
                    data.total_notifications;

                unreadNotificationCountElement.textContent =
                    data.unread_notifications;


                if (data.notifications.length === 0) {

                    notificationList.innerHTML =
                        "<p>No notifications found.</p>";

                    return;
                }


                notificationList.innerHTML = "";


                data.notifications.forEach(
                    function (notification) {

                        const notificationCard =
                            document.createElement("div");

                        notificationCard.className =
                            "transaction-card";

                        notificationCard.setAttribute(
                            "data-notification-id",
                            notification.notification_id
                        );

                        notificationCard.addEventListener(
                            "click",
                            async function () {
                                if (notification.is_read) {
                                    return;
                                }
                                const notificationId =  
                                notification.notification_id;

                                try {
                                    const response = await fetch(
                                        `http://127.0.0.1:50001/api/notifications/${notificationId}/read`,
                                        {
                                            method: "PUT"
                                        }
                                    );

                                    const data = await response.json();

                                    console.log("Mark as read response:", data);

                                    if (response.ok) {

                                        notification.is_read = true;

                                        const statusElement =
                                            notificationCard.querySelector(
                                                ".notification-read-status"
                                            );

                                        if (statusElement) {

                                            statusElement.textContent =
                                                "READ";

                                        }

                                        notificationCard.style.opacity =
                                            "0.65";


                                        if (
                                            unreadNotificationCountElement
                                        ) {

                                            const currentCount =
                                                Number(
                                                    unreadNotificationCountElement
                                                        .textContent
                                                );

                                            if (currentCount > 0) {

                                                unreadNotificationCountElement
                                                    .textContent =
                                                    currentCount - 1;

                                            }

                                        }

                                    }

                                } catch (error) {

                                    console.error(
                                        "Mark Notification Error:",
                                        error
                                    );

                                }
                            }
                        );

                        notificationCard.innerHTML = `

                            <div class="transaction-icon">
                                🔔
                            </div>

                            <div class="transaction-details">

                                <h3>
                                    ${notification.message}
                                </h3>

                                <p>
                                    Transaction ID:
                                    ${notification.transaction_id || "N/A"}
                                </p>

                                <p>
                                    Date:
                                    ${notification.created_at}
                                </p>

                            </div>

                            <div class="transaction-amount">

                                <span class="notification-read-status">
                                    ${
                                        notification.is_read
                                            ? "READ"
                                            : "UNREAD"
                                    }
                                </span>

                                ${
                                    !notification.is_read
                                        ? `
                                            <button
                                                type="button"
                                                class="mark-read-btn"
                                                data-notification-id="${notification.notification_id}"
                                            >
                                                Mark as Read
                                            </button>
                                          `
                                        : ""
                                }

                            </div>

                        `;


                        notificationList.appendChild(
                            notificationCard
                        );

                    }
                );

            } else {

                notificationList.innerHTML =
                    `<p>${
                        data.message ||
                        "Unable to load notifications."
                    }</p>`;

            }

        })
        .catch(error => {

            console.error(
                "Notification Error:",
                error
            );

            notificationList.innerHTML =
                "<p>Unable to connect to SmartBank server.</p>";

        });

    }

}


/* =========================================
   MARK NOTIFICATION AS READ
========================================= */

if (notificationList) {

    notificationList.addEventListener(
        "click",
        async function (event) {

            const button =
                event.target.closest(
                    ".mark-read-btn"
                );

            if (!button) {
                return;
            }

            const notificationId =
                button.getAttribute(
                    "data-notification-id"
                );

            if (!notificationId) {

                console.error(
                    "Notification ID not found."
                );

                return;
            }


            try {

                const response =
                    await fetch(
                        `http://127.0.0.1:50001/api/notifications/${notificationId}/read`,
                        {
                            method: "PUT"
                        }
                    );


                const data =
                    await response.json();


                console.log(
                    "Mark as read response:",
                    data
                );


                if (response.ok) {

                    const card =
                        button.closest(
                            ".transaction-card"
                        );


                    if (card) {

                        const status =
                            card.querySelector(
                                ".notification-read-status"
                            );

                        if (status) {

                            status.textContent =
                                "READ";

                        }


                        button.remove();

                        card.style.opacity =
                            "0.65";

                    }


                    const unreadCount =
                        document.getElementById(
                            "unreadNotificationCount"
                        );


                    if (unreadCount) {

                        const currentCount =
                            Number(
                                unreadCount.textContent
                            );

                        if (currentCount > 0) {

                            unreadCount.textContent =
                                currentCount - 1;

                        }

                    }

                } else {

                    console.error(
                        data.message ||
                        "Unable to mark notification as read."
                    );

                }

            } catch (error) {

                console.error(
                    "Mark Notification Error:",
                    error
                );

            }

        }
    );

}
/* =========================================
   TRANSFER MONEY NAVIGATION
========================================= */

const transferCard =
    document.getElementById("transferCard");

if (transferCard) {

    transferCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "transfer.html";

        }
    );

}
// =========================================
// TRANSFER MONEY
// =========================================

const transferForm = document.getElementById("transferForm");

if (transferForm) {

    const senderAccountInput =
        document.getElementById("transferSenderAccount");

    const currentBalance =
        document.getElementById("transferCurrentBalance");

    const receiverAccountInput =
        document.getElementById("receiverAccount");

    const transferAmountInput =
        document.getElementById("transferAmount");

    const transferMessage =
        document.getElementById("transferMessage");


    // Get logged-in account number
    const accountNumber =
        sessionStorage.getItem("accountNumber");


    // Check login
    if (!accountNumber) {

        window.location.href = "login.html";

    } else {

        // Show sender account number
        senderAccountInput.textContent =
            accountNumber;


        // Load current balance
        fetch(
            `http://127.0.0.1:50001/api/customer/${accountNumber}`
        )
        .then(response => response.json())
        .then(data => {

            if (data.status === "success") {

                currentBalance.textContent =
                    `₹${Number(data.balance).toFixed(2)}`;

            }

        })
        .catch(error => {

            console.error(
                "Error loading balance:",
                error
            );

        });
    }


    // Allow only numbers for receiver account
    receiverAccountInput.addEventListener(
    "input",
    function () {

        this.value =
            this.value.replace(/\D/g, "");

        this.dataset.receiverName = "";

        document.getElementById("receiverName").textContent = "";

        transferMessage.textContent = "";

    }
);
    receiverAccountInput.addEventListener(
        "blur",
        function () {
            const receiverAccount = this.value.trim();
            if (!receiverAccount) {
                return;
            }
            fetch(
                `http://127.0.0.1:50001/api/customer/lookup/${receiverAccount}`

            )
            .then(response => response.jsom())
            .then(data => {
                if (data.status === "success") {

                    receiverAccountInput.dataset.receiverName =
                        data.name;

                    document.getElementById("receiverName").textContent =
                        `Receiver: ${data.name}`;

               } else {

                    receiverAccountInput.dataset.receiverName = "";

                    document.getElementById("receiverName").textContent = "";

                    transferMessage.textContent =
                        data.message ||
                        "Receiver account not found.";

                }
        })
        .catch(error => {
            console.error(
                "Receiver lookup error:",
                error
            );
            transferMessage.textContent =
                "Unable to verify receiver account.";
        });
        }
    );
    transferAmountInput.addEventListener(
        "input",
        function () {

            transferMessage.textContent = "";

        }
    );


    // Transfer form submit
    transferForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            const senderAccount =
                accountNumber;

            const receiverAccount =
                receiverAccountInput.value.trim();

            const receiverName =
                receiverAccountInput.dataset.receiverName || "Unknown Receiver";

            const amount =
                parseFloat(transferAmountInput.value);

            const submitButton =
                transferForm.querySelector("button[type='submit']");


            // Clear previous message
            transferMessage.textContent = "";


            // Validate receiver account
            if (!receiverAccount) {

                transferMessage.textContent =
                    "Please enter the receiver account number.";

                return;
            }


            // Prevent self-transfer
            if (
                receiverAccount ===
                String(senderAccount)
            ) {

                transferMessage.textContent =
                    "You cannot transfer money to your own account.";

                return;
            }


            // Validate amount
            if (
                isNaN(amount) ||
                amount <= 0
            ) {

                transferMessage.textContent =
                    "Please enter a valid transfer amount.";

                return;
            }

            if (amount > parseFloat(
                currentBalance.textContent.replace("₹", "")
            )) {

                transferMessage.textContent =
                    "Insufficient balance.";

                return;
            }

            submitButton.disabled = true;
            submitButton.textContent = "Processing...";
            
            const confirmTransfer = confirm(
                `Are you sure you want to transfer ₹${amount.toFixed(2)} to ${receiverName} (${receiverAccount})?`
            );

            if (!confirmTransfer) {
                submitButton.disabled = false;
                submitButton.textContent = "Transfer Money";
                return;
            }
            // Send transfer request
            fetch(
                "/api/transfer",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        sender_account:
                            senderAccount,

                        receiver_account:
                            receiverAccount,

                        amount:
                            amount
                    })
                }
            )
            .then(response => response.json())
            .then(data => {

                submitButton.disabled = false;
                submitButton.textContent = "Transfer Money";

                if (data.status === "success") {

                    transferMessage.innerHTML =
                        `
                        <strong>Transfer Successful!</strong><br>
                        Transaction ID: ${data.transaction_id}<br>
                        Amount Transferred: ₹${Number(data.amount).toFixed(2)}<br>
                        New Balance: ₹${Number(data.sender_new_balance).toFixed(2)}
                        `;

                    // Update balance on page
                    currentBalance.textContent =
                        `₹${Number(data.sender_new_balance).toFixed(2)}`;


                    // Clear form
                    receiverAccountInput.value = "";
                    transferAmountInput.value = "";

                } else {

                    transferMessage.textContent =
                        data.message ||
                        "Transfer failed.";

                }

            })
            .catch(error => {

                console.error(
                    "Transfer error:",
                    error
                );
                submitButton.disabled = false;
                submitButton.textContent = "Transfer Money";

                transferMessage.textContent =
                    "Unable to connect to the banking server.";

            });

        }
    );
}
// =========================================
// CUSTOMER PROFILE
// =========================================

const profileName =
    document.getElementById("profileName");

const profileAccountNumber =
    document.getElementById("profileAccountNumber");

const profileStatus =
    document.getElementById("profileStatus");

const profileEmail =
    document.getElementById("profileEmail");

const profileMobile =
    document.getElementById("profileMobile");

const profileCreatedAt =
    document.getElementById("profileCreatedAt");


if (profileName) {

    const accountNumber =
        sessionStorage.getItem("accountNumber");


    if (!accountNumber) {

        window.location.href = "login.html";

    } else {

        fetch(
            `http://127.0.0.1:50001/api/profile/${accountNumber}`
        )
        .then(response => response.json())
        .then(data => {

            if (data.status === "success") {

                profileName.textContent =
                    data.name;

                profileAccountNumber.textContent =
                    data.account_no;

                profileStatus.textContent =
                    data.account_status;

                profileEmail.textContent =
                    data.email || "Not provided";

                profileMobile.textContent =
                    data.mobile || "Not provided";

                profileCreatedAt.textContent =
                    data.created_at || "Not available";

            } else {

                profileName.textContent =
                    "Unable to load profile.";

            }

        })
        .catch(error => {

            console.error(
                "Profile error:",
                error
            );

            profileName.textContent =
                "Unable to connect to the banking server.";

        });

    }

}
// =========================================
// CUSTOMER PROFILE NAVIGATION
// =========================================

const profileCard =
    document.getElementById("profileCard");

if (profileCard) {

    profileCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "profile.html";

        }
    );
}
// =========================================
// ACCOUNT STATUS
// =========================================

const statusAccountNumber =
    document.getElementById("statusAccountNumber");

const accountStatus =
    document.getElementById("accountStatus");

const statusMessage =
    document.getElementById("statusMessage");


if (statusAccountNumber) {

    const accountNumber =
        sessionStorage.getItem("accountNumber");


    if (!accountNumber) {

        window.location.href = "login.html";

    } else {

        fetch(
            `http://127.0.0.1:50001/api/account-status/${accountNumber}`
        )
        .then(response => response.json())
        .then(data => {

            if (data.status === "success") {

                statusAccountNumber.textContent =
                    data.account_no;

                accountStatus.textContent =
                    data.account_status;

                if (data.account_status === "Active") {

                    statusMessage.textContent =
                        "Your account is active and ready for banking operations.";

                } else if (data.account_status === "Suspended") {

                    statusMessage.textContent =
                        "Your account is currently suspended.";

                } else if (data.account_status === "Closed") {

                    statusMessage.textContent =
                        "Your account is closed.";

                } else {

                    statusMessage.textContent =
                        "Your account status is " +
                        data.account_status + ".";

                }

            } else {

                statusMessage.textContent =
                    data.message ||
                    "Unable to load account status.";

            }

        })
        .catch(error => {

            console.error(
                "Account status error:",
                error
            );

            statusMessage.textContent =
                "Unable to connect to the banking server.";

        });

    }

}
// =========================================
// ACCOUNT STATUS NAVIGATION
// =========================================

const accountStatusCard =
    document.getElementById("accountStatusCard");

if (accountStatusCard) {

    accountStatusCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "account-status.html";

        }
    );

}
const changePasswordCard =
    document.getElementById("changePasswordCard");

if (changePasswordCard) {
    changePasswordCard.addEventListener(
        "click",
        function () {
            window.location.href =
                "change-password.html";
        }
    );
}
// =========================================
// DASHBOARD ACCOUNT STATUS CHECK
// =========================================

const dashboardAccountStatus =
    document.getElementById("accountStatus");

if (dashboardAccountStatus) {

    const accountNumber =
        sessionStorage.getItem("accountNumber");

    if (accountNumber) {

        fetch(
            `http://127.0.0.1:50001/api/account-status/${accountNumber}`
        )
        .then(response => response.json())
        .then(data => {

            if (data.status === "success") {

                dashboardAccountStatus.textContent =
                    data.account_status;

            }

        })
        .catch(error => {

            console.error(
                "Dashboard account status error:",
                error
            );

        });

    }

}

// =========================================
// ADMIN ACCOUNT STATUS MANAGEMENT
// =========================================

const adminStatusForm =
    document.getElementById("adminStatusForm");

if (adminStatusForm) {

    adminStatusForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            const accountNumber =
                document.getElementById(
                    "adminAccountNumber"
                ).value.trim();

            const newStatus =
                document.getElementById(
                    "adminAccountStatus"
                ).value;

            const message =
                document.getElementById(
                    "adminStatusMessage"
                );

            if (!accountNumber || !newStatus) {

                message.textContent =
                    "Please enter account number and select a status.";

                return;
            }

            const confirmation =
                confirm(
                    `Are you sure you want to change account ${accountNumber} status to ${newStatus}?`
                );

            if (!confirmation) {
                return;
            }

            fetch(
                "/api/admin/change-account-status",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        account_no:
                            accountNumber,
                        new_status:
                            newStatus
                    })
                }
            )
            .then(response => response.json())

            .then(data => {

                if (data.status === "success") {

                    message.textContent =
                        data.message;

                    document.getElementById(
                        "adminAccountNumber"
                    ).value = "";

                    document.getElementById(
                        "adminAccountStatus"
                    ).value = "";

                } else {

                    message.textContent =
                        data.message ||
                        "Unable to change account status.";

                }

            })

            .catch(error => {

                console.error(
                    "Admin account status error:",
                    error
                );

                message.textContent =
                    "Unable to connect to the banking server.";

            });

        }
    );

}

// =========================================
// ADMIN CURRENT ACCOUNT STATUS
// =========================================

const adminAccountNumber =
    document.getElementById("adminAccountNumber");

const adminCustomerName =
    document.getElementById("adminCustomerName");

const adminCustomerAccount =
    document.getElementById("adminCustomerAccount");

const adminCurrentStatus =
    document.getElementById("adminCurrentStatus");

const adminStatusMessage =
    document.getElementById("adminStatusMessage");


if (adminAccountNumber) {

    adminAccountNumber.addEventListener(
        "blur",
        function () {

            const accountNumber =
                adminAccountNumber.value.trim();

            if (!accountNumber) {
                return;
            }


            fetch(
                `http://127.0.0.1:50001/api/admin/account-status/${accountNumber}`
            )

            .then(response => response.json())

            .then(data => {

                if (data.status === "success") {

                    adminCustomerName.textContent =
                        data.name;

                    adminCustomerAccount.textContent =
                        data.account_no;

                    adminCurrentStatus.textContent =
                        data.account_status;

                    adminStatusMessage.textContent =
                        "Customer account details loaded successfully.";

                } else {

                    adminCustomerName.textContent =
                        "Not found";

                    adminCustomerAccount.textContent =
                        "Not found";

                    adminCurrentStatus.textContent =
                        "Not found";

                    adminStatusMessage.textContent =
                        data.message ||
                        "Customer account not found.";

                }

            })

            .catch(error => {

                console.error(
                    "Admin current status error:",
                    error
                );

                adminCustomerName.textContent =
                    "Unavailable";

                adminCustomerAccount.textContent =
                    "Unavailable";

                adminCurrentStatus.textContent =
                    "Unavailable";

                adminStatusMessage.textContent =
                    "Unable to connect to the banking server.";

            });

        }
    );

}

// =========================================
// ADMIN LOGIN
// =========================================

const adminLoginForm =
    document.getElementById("adminLoginForm");

if (adminLoginForm) {

    adminLoginForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            const username =
                document.getElementById(
                    "adminUsername"
                ).value.trim();

            const password =
                document.getElementById(
                    "adminPassword"
                ).value;

            const message =
                document.getElementById(
                    "adminLoginMessage"
                );


            fetch(
                "/api/admin/login",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                }
            )

            .then(response => response.json())

            .then(data => {

                if (data.status === "success") {

                    sessionStorage.setItem(
                        "adminLoggedIn",
                        "true"
                    );

                    message.textContent =
                        data.message;

                    window.location.href =
                        "admin-dashboard.html";

                } else {

                    message.textContent =
                        data.message ||
                        "Invalid admin login.";

                }

            })

            .catch(error => {

                console.error(
                    "Admin login error:",
                    error
                );

                message.textContent =
                    "Unable to connect to the banking server.";

            });

        }
    );

}
// =========================================
// ADMIN PAGE ACCESS PROTECTION
// =========================================

const adminPage =
    document.getElementById("adminStatusForm");

if (adminPage) {

    const adminLoggedIn =
        sessionStorage.getItem("adminLoggedIn");

    if (adminLoggedIn !== "true") {

        alert(
            "Admin login required."
        );

        window.location.href =
            "admin-login.html";
    }

}
// =========================================
// ADMIN LOGOUT
// =========================================

const adminLogoutBtn =
    document.getElementById("adminLogoutBtn");

if (adminLogoutBtn) {

    adminLogoutBtn.addEventListener(
        "click",
        function (event) {

            event.preventDefault();

            sessionStorage.removeItem(
                "adminLoggedIn"
            );

            alert(
                "Admin logged out successfully."
            );

            window.location.href =
                "admin-login.html";

        }
    );

}
// =========================================
// ADMIN ACTIVITY LOG
// =========================================

const adminActivityContainer =
    document.getElementById(
        "adminActivityContainer"
    );

const adminActivityMessage =
    document.getElementById(
        "adminActivityMessage"
    );


if (adminActivityContainer) {

    const adminLoggedIn =
        sessionStorage.getItem(
            "adminLoggedIn"
        );

    if (adminLoggedIn !== "true") {

        alert(
            "Admin login required."
        );

        window.location.href =
            "admin-login.html";

    } else {

        fetch(
            "/api/admin/activity-log"
        )

        .then(response =>
            response.json()
        )

        .then(data => {

            if (
                data.status === "success"
                &&
                data.activities.length > 0
            ) {

                adminActivityContainer.innerHTML =
                    "";

                data.activities.forEach(
                    activity => {

                        const activityCard =
                            document.createElement(
                                "div"
                            );

                        activityCard.className =
                            "dashboard-service-card";


                        activityCard.innerHTML = `

                            <div class="service-icon">
                                📋
                            </div>

                            <h3>
                                ${activity.action}
                            </h3>

                            <p>
                                ${activity.details}
                            </p>

                            <p>
                                ${activity.date}
                            </p>

                        `;


                        adminActivityContainer.appendChild(
                            activityCard
                        );

                    }
                );

            } else {

                adminActivityMessage.textContent =
                    "No admin activities found.";

            }

        })

        .catch(error => {

            console.error(
                "Admin activity log error:",
                error
            );

            adminActivityMessage.textContent =
                "Unable to load admin activity log.";

        });

    }

}
// =========================================
// ADMIN DASHBOARD ACCESS PROTECTION
// =========================================

const adminDashboard =
    document.getElementById(
        "adminAccountStatusCard"
    );

if (adminDashboard) {

    const adminLoggedIn =
        sessionStorage.getItem(
            "adminLoggedIn"
        );

    if (adminLoggedIn !== "true") {

        alert(
            "Admin login required."
        );

        window.location.href =
            "admin-login.html";
    }

}
// =========================================
// ADMIN DASHBOARD STATISTICS
// =========================================

const totalCustomers =
    document.getElementById(
        "totalCustomers"
    );

const totalBalance =
    document.getElementById(
        "totalBalance"
    );

const totalTransactions =
    document.getElementById(
        "totalTransactions"
    );


if (
    totalCustomers &&
    totalBalance &&
    totalTransactions
) {

    fetch(
        "/api/admin/dashboard-statistics"
    )

    .then(response =>
        response.json()
    )

    .then(data => {

        if (data.status === "success") {

            totalCustomers.textContent =
                data.total_customers;

            totalBalance.textContent =
                "₹" +
                Number(
                    data.total_balance
                ).toLocaleString(
                    "en-IN",
                    {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    }
                );

            totalTransactions.textContent =
                data.total_transactions;

        } else {

            totalCustomers.textContent =
                "Unavailable";

            totalBalance.textContent =
                "Unavailable";

            totalTransactions.textContent =
                "Unavailable";

        }

    })

    .catch(error => {

        console.error(
            "Admin dashboard statistics error:",
            error
        );

        totalCustomers.textContent =
            "Unavailable";

        totalBalance.textContent =
            "Unavailable";

        totalTransactions.textContent =
            "Unavailable";

    });

}
// =========================================
// ADMIN DASHBOARD CARD NAVIGATION
// =========================================

const adminAccountStatusCard =
    document.getElementById(
        "adminAccountStatusCard"
    );

if (adminAccountStatusCard) {

    adminAccountStatusCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "admin-account-status.html";

        }
    );

}


const adminActivityCard =
    document.getElementById(
        "adminActivityCard"
    );

if (adminActivityCard) {

    adminActivityCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "admin-activity-log.html";

        }
    );

}
// =========================================
// ADMIN SYSTEM HEALTH CARD NAVIGATION
// =========================================

const adminSystemHealthCard =
    document.getElementById(
        "adminSystemHealthCard"
    );

if (adminSystemHealthCard) {

    adminSystemHealthCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "admin-system-health.html";

        }
    );

}
// =========================================
// ADMIN SYSTEM HEALTH
// =========================================

const healthCustomers =
    document.getElementById(
        "healthCustomers"
    );

const healthTransactions =
    document.getElementById(
        "healthTransactions"
    );

const healthNotifications =
    document.getElementById(
        "healthNotifications"
    );

const healthActivities =
    document.getElementById(
        "healthActivities"
    );

const healthDatabase =
    document.getElementById(
        "healthDatabase"
    );

const systemHealthMessage =
    document.getElementById(
        "systemHealthMessage"
    );


if (
    healthCustomers &&
    healthTransactions &&
    healthNotifications &&
    healthActivities &&
    healthDatabase
) {

    fetch(
        "/api/admin/system-health"
    )

    .then(response =>
        response.json()
    )

    .then(data => {

        if (data.status === "success") {

            healthCustomers.textContent =
                data.total_customers;

            healthTransactions.textContent =
                data.total_transactions;

            healthNotifications.textContent =
                data.total_notifications;

            healthActivities.textContent =
                data.total_activities;

            healthDatabase.textContent =
                data.database_status;

            systemHealthMessage.textContent =
                "Banking system health loaded successfully.";

        } else {

            healthCustomers.textContent =
                "Unavailable";

            healthTransactions.textContent =
                "Unavailable";

            healthNotifications.textContent =
                "Unavailable";

            healthActivities.textContent =
                "Unavailable";

            healthDatabase.textContent =
                "Unavailable";

            systemHealthMessage.textContent =
                data.message ||
                "Unable to load system health.";

        }

    })

    .catch(error => {

        console.error(
            "Admin system health error:",
            error
        );

        healthCustomers.textContent =
            "Unavailable";

        healthTransactions.textContent =
            "Unavailable";

        healthNotifications.textContent =
            "Unavailable";

        healthActivities.textContent =
            "Unavailable";

        healthDatabase.textContent =
            "Unavailable";

        systemHealthMessage.textContent =
            "Unable to connect to the banking server.";

    });

}
// =========================================
// ADMIN SYSTEM HEALTH ACCESS PROTECTION
// =========================================

const adminSystemHealthPage =
    document.getElementById(
        "healthDatabase"
    );

if (adminSystemHealthPage) {

    const adminLoggedIn =
        sessionStorage.getItem(
            "adminLoggedIn"
        );

    if (adminLoggedIn !== "true") {

        alert(
            "Admin login required."
        );

        window.location.href =
            "admin-login.html";
    }

}
// =========================================
// ADMIN CUSTOMER SEARCH
// =========================================

const adminCustomerSearchForm =
    document.getElementById(
        "adminCustomerSearchForm"
    );

if (adminCustomerSearchForm) {

    adminCustomerSearchForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            const accountNumber =
                document.getElementById(
                    "searchCustomerAccount"
                ).value.trim();

            const message =
                document.getElementById(
                    "customerSearchMessage"
                );

            if (!accountNumber) {

                message.textContent =
                    "Please enter an account number.";

                return;
            }


            message.textContent =
                "Searching customer...";


            fetch(
                `http://127.0.0.1:50001/api/admin/customer-search/${accountNumber}`
            )

            .then(response =>
                response.json()
            )

            .then(data => {

                if (data.status === "success") {

                    document.getElementById(
                        "searchCustomerName"
                    ).textContent =
                        data.name || "Not available";

                    document.getElementById(
                        "searchCustomerAccountNumber"
                    ).textContent =
                        data.account_no;

                    document.getElementById(
                        "searchCustomerEmail"
                    ).textContent =
                        data.email || "Not available";

                    document.getElementById(
                        "searchCustomerMobile"
                    ).textContent =
                        data.mobile || "Not available";

                    document.getElementById(
                        "searchCustomerBalance"
                    ).textContent =
                        "₹" +
                        Number(
                            data.balance
                        ).toLocaleString(
                            "en-IN",
                            {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            }
                        );

                    document.getElementById(
                        "searchCustomerStatus"
                    ).textContent =
                        data.account_status;

                    document.getElementById(
                        "searchCustomerCreatedAt"
                    ).textContent =
                        data.created_at || "Not available";

                    message.textContent =
                        "Customer details loaded successfully.";

                } else {

                    message.textContent =
                        data.message ||
                        "Customer account not found.";

                }

            })

            .catch(error => {

                console.error(
                    "Admin customer search error:",
                    error
                );

                message.textContent =
                    "Unable to connect to the banking server.";

            });

        }
    );

}
// =========================================
// ADMIN CUSTOMER SEARCH CARD NAVIGATION
// =========================================

const adminCustomerSearchCard =
    document.getElementById(
        "adminCustomerSearchCard"
    );

if (adminCustomerSearchCard) {

    adminCustomerSearchCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "admin-customer-search.html";

        }
    );

}
const adminCustomerSearchPage =
    document.getElementById(
        "adminCustomerSearchForm"
    );

if (adminCustomerSearchPage) {

    const adminLoggedIn =
        sessionStorage.getItem(
            "adminLoggedIn"
        );

    if (adminLoggedIn !== "true") {

        alert(
            "Admin login required."
        );

        window.location.href =
            "admin-login.html";

    }

}
const adminCustomerDetailsForm =
    document.getElementById(
        "adminCustomerDetailsForm"
    );

if (adminCustomerDetailsForm) {

    const adminLoggedIn =
        sessionStorage.getItem(
            "adminLoggedIn"
        );

    if (adminLoggedIn !== "true") {

        alert(
            "Admin login required."
        );

        window.location.href =
            "admin-login.html";

    } else {

        adminCustomerDetailsForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();

                const accountNumber =
                    document.getElementById(
                        "detailsCustomerAccount"
                    ).value.trim();

                const message =
                    document.getElementById(
                        "customerDetailsMessage"
                    );

                if (!accountNumber) {

                    message.textContent =
                        "Please enter an account number.";

                    return;
                }

                message.textContent =
                    "Loading customer details...";

                fetch(
                    `http://127.0.0.1:50001/api/admin/customer-details/${accountNumber}`
                )

                .then(response =>
                    response.json()
                )

                .then(data => {

                    if (data.status === "success") {

                        document.getElementById(
                            "detailsCustomerName"
                        ).textContent =
                            data.name || "Not available";

                        document.getElementById(
                            "detailsCustomerAccountNumber"
                        ).textContent =
                            data.account_no;

                        document.getElementById(
                            "detailsCustomerEmail"
                        ).textContent =
                            data.email || "Not available";

                        document.getElementById(
                            "detailsCustomerMobile"
                        ).textContent =
                            data.mobile || "Not available";

                        document.getElementById(
                            "detailsCustomerBalance"
                        ).textContent =
                            "₹" +
                            Number(
                                data.balance
                            ).toLocaleString(
                                "en-IN",
                                {
                                    minimumFractionDigits: 2,
                                    maximumFractionDigits: 2
                                }
                            );

                        document.getElementById(
                            "detailsCustomerStatus"
                        ).textContent =
                            data.account_status;

                        document.getElementById(
                            "detailsCustomerCreatedAt"
                        ).textContent =
                            data.created_at ||
                            "Not available";

                        message.textContent =
                            "Customer details loaded successfully.";

                    } else {

                        message.textContent =
                            data.message ||
                            "Customer account not found.";

                    }

                })

                .catch(error => {

                    console.error(
                        "Admin customer details error:",
                        error
                    );

                    message.textContent =
                        "Unable to connect to the banking server.";

                });

            }
        );

    }

}
const adminCustomerDetailsCard =
    document.getElementById(
        "adminCustomerDetailsCard"
    );

if (adminCustomerDetailsCard) {

    adminCustomerDetailsCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "admin-customer-details.html";

        }
    );

}
const adminTransactionSearchCard =
    document.getElementById(
        "adminTransactionSearchCard"
    );

if (adminTransactionSearchCard) {

    adminTransactionSearchCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "admin-transaction-search.html";

        }
    );

}
const adminTransactionFilterCard =
    document.getElementById(
        "adminTransactionFilterCard"
    );

if (adminTransactionFilterCard) {

    adminTransactionFilterCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "admin-transaction-filter.html";

        }
    );

}

const adminTransactionSearchForm =
    document.getElementById(
        "adminTransactionSearchForm"
    );

if (adminTransactionSearchForm) {

    const adminLoggedIn =
        sessionStorage.getItem(
            "adminLoggedIn"
        );

    if (adminLoggedIn !== "true") {

        alert(
            "Admin login required."
        );

        window.location.href =
            "admin-login.html";

    } else {

        adminTransactionSearchForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();

                const transactionId =
                    document.getElementById(
                        "searchTransactionId"
                    ).value
                        .trim()
                        .replace(/^["']|["']$/g, "");

                const message =
                    document.getElementById(
                        "transactionSearchMessage"
                    );

                if (!transactionId) {

                    message.textContent =
                        "Please enter a transaction ID.";

                    return;
                }

                message.textContent =
                    "Searching transaction...";

                fetch(
                    `http://127.0.0.1:50001/api/admin/transaction-search/${transactionId}`
                )

                .then(response =>
                    response.json()
                )

                .then(data => {

                    if (data.status === "success") {

                        document.getElementById(
                            "searchTransactionIdResult"
                        ).textContent =
                            data.transaction_id;

                        document.getElementById(
                            "searchTransactionCustomerName"
                        ).textContent =
                            data.customer_name ||
                            "Not available";

                        document.getElementById(
                            "searchTransactionAccount"
                        ).textContent =
                            data.account_no;

                        document.getElementById(
                            "searchTransactionType"
                        ).textContent =
                            data.transaction_type;

                        document.getElementById(
                            "searchTransactionAmount"
                        ).textContent =
                            "₹" +
                            Number(
                                data.amount
                            ).toLocaleString(
                                "en-IN",
                                {
                                    minimumFractionDigits: 2,
                                    maximumFractionDigits: 2
                                }
                            );

                        document.getElementById(
                            "searchTransactionSender"
                        ).textContent =
                            data.sender_account ||
                            "Not applicable";

                        document.getElementById(
                            "searchTransactionReceiver"
                        ).textContent =
                            data.receiver_account ||
                            "Not applicable";

                        document.getElementById(
                            "searchTransactionDate"
                        ).textContent =
                            data.date ||
                            "Not available";

                        document.getElementById(
                            "searchTransactionStatus"
                        ).textContent =
                            data.status;

                        message.textContent =
                            "Transaction details loaded successfully.";

                    } else {

                        message.textContent =
                            data.message ||
                            "Transaction not found.";

                    }

                })

                .catch(error => {

                    console.error(
                        "Admin transaction search error:",
                        error
                    );

                    message.textContent =
                        "Unable to connect to the banking server.";

                });

            }
        );

    }

}
const adminTransactionFilterForm =
    document.getElementById(
        "adminTransactionFilterForm"
    );

if (adminTransactionFilterForm) {

    const adminLoggedIn =
        sessionStorage.getItem(
            "adminLoggedIn"
        );

    if (adminLoggedIn !== "true") {

        alert(
            "Admin login required."
        );

        window.location.href =
            "admin-login.html";

    } else {

        adminTransactionFilterForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();

                const accountNumber =
                    document.getElementById(
                        "filterAccountNumber"
                    ).value.trim();

                const transactionType =
                    document.getElementById(
                        "filterTransactionType"
                    ).value;

                const transactionDate =
                    document.getElementById(
                        "filterTransactionDate"
                    ).value;

                const message =
                    document.getElementById(
                        "transactionFilterMessage"
                    );

                const results =
                    document.getElementById(
                        "transactionFilterResults"
                    );


                if (
                    !accountNumber &&
                    !transactionType &&
                    !transactionDate
                ) {

                    message.textContent =
                        "Please select at least one filter.";

                    results.innerHTML = "";

                    return;
                }


                message.textContent =
                    "Filtering transactions...";

                results.innerHTML = "";


                const parameters =
                    new URLSearchParams();


                if (accountNumber) {

                    parameters.append(
                        "account_no",
                        accountNumber
                    );

                }


                if (transactionType) {

                    parameters.append(
                        "transaction_type",
                        transactionType
                    );

                }


                if (transactionDate) {

                    parameters.append(
                        "transaction_date",
                        transactionDate
                    );

                }


                fetch(
                    `http://127.0.0.1:50001/api/admin/transaction-filter?${parameters.toString()}`
                )

                .then(response =>
                    response.json()
                )

                .then(data => {

                    if (data.status === "success") {

                        if (
                            data.transactions.length === 0
                        ) {

                            message.textContent =
                                "No transactions found.";

                            return;

                        }


                        message.textContent =
                            `${data.total_transactions} transaction(s) found.`;


                        data.transactions.forEach(
                            transaction => {

                                const card =
                                    document.createElement(
                                        "div"
                                    );

                                card.className =
                                    "dashboard-service-card";


                                card.innerHTML = `

                                    <div class="service-icon">
                                        💳
                                    </div>

                                    <h3>
                                        ${transaction.transaction_type}
                                    </h3>

                                    <p>
                                        <strong>
                                            Transaction ID:
                                        </strong>
                                        ${transaction.transaction_id}
                                    </p>

                                    <p>
                                        <strong>
                                            Customer:
                                        </strong>
                                        ${transaction.customer_name}
                                    </p>

                                    <p>
                                        <strong>
                                            Account:
                                        </strong>
                                        ${transaction.account_no}
                                    </p>

                                    <p>
                                        <strong>
                                            Amount:
                                        </strong>
                                        ₹${Number(
                                            transaction.amount
                                        ).toLocaleString(
                                            "en-IN",
                                            {
                                                minimumFractionDigits: 2,
                                                maximumFractionDigits: 2
                                            }
                                        )}
                                    </p>

                                    <p>
                                        <strong>
                                            Sender:
                                        </strong>
                                        ${
                                            transaction.sender_account ||
                                            "Not applicable"
                                        }
                                    </p>

                                    <p>
                                        <strong>
                                            Receiver:
                                        </strong>
                                        ${
                                            transaction.receiver_account ||
                                            "Not applicable"
                                        }
                                    </p>

                                    <p>
                                        <strong>
                                            Date:
                                        </strong>
                                        ${transaction.date}
                                    </p>

                                    <p>
                                        <strong>
                                            Status:
                                        </strong>
                                        ${transaction.status}
                                    </p>

                                `;


                                results.appendChild(
                                    card
                                );

                            }
                        );

                    } else {

                        message.textContent =
                            data.message ||
                            "Unable to filter transactions.";

                    }

                })

                .catch(error => {

                    console.error(
                        "Admin transaction filter error:",
                        error
                    );

                    message.textContent =
                        "Unable to connect to the banking server.";

                });

            }
        );

    }

}
const clearTransactionFilter =
    document.getElementById(
        "clearTransactionFilter"
    );

if (clearTransactionFilter) {

    clearTransactionFilter.addEventListener(
        "click",
        function () {

            document.getElementById(
                "filterAccountNumber"
            ).value = "";

            document.getElementById(
                "filterTransactionType"
            ).value = "";

            document.getElementById(
                "filterTransactionDate"
            ).value = "";

            document.getElementById(
                "transactionFilterResults"
            ).innerHTML = "";

            document.getElementById(
                "transactionFilterMessage"
            ).textContent = "";

        }
    );

}
const bankingSummaryPage =
    document.getElementById(
        "summaryDepositTransactions"
    );

if (bankingSummaryPage) {

    const adminLoggedIn =
        sessionStorage.getItem(
            "adminLoggedIn"
        );

    if (adminLoggedIn !== "true") {

        alert(
            "Admin login required."
        );

        window.location.href =
            "admin-login.html";

    } else {

        const summaryDepositTransactions =
            document.getElementById(
                "summaryDepositTransactions"
            );

        const summaryDepositAmount =
            document.getElementById(
                "summaryDepositAmount"
            );

        const summaryWithdrawalTransactions =
            document.getElementById(
                "summaryWithdrawalTransactions"
            );

        const summaryWithdrawalAmount =
            document.getElementById(
                "summaryWithdrawalAmount"
            );

        const summaryTransferTransactions =
            document.getElementById(
                "summaryTransferTransactions"
            );

        const summaryTransferAmount =
            document.getElementById(
                "summaryTransferAmount"
            );

        const summarySuccessfulTransactions =
            document.getElementById(
                "summarySuccessfulTransactions"
            );

        const summaryFailedTransactions =
            document.getElementById(
                "summaryFailedTransactions"
            );

        const summaryActiveBalance =
            document.getElementById(
                "summaryActiveBalance"
            );

        const bankingSummaryMessage =
            document.getElementById(
                "bankingSummaryMessage"
            );


        fetch(
            "/api/admin/banking-summary"
        )

        .then(response =>
            response.json()
        )

        .then(data => {

            if (data.status === "success") {

                summaryDepositTransactions.textContent =
                    data.total_deposit_transactions;

                summaryDepositAmount.textContent =
                    "₹" +
                    Number(
                        data.total_deposit_amount
                    ).toLocaleString(
                        "en-IN",
                        {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        }
                    );

                summaryWithdrawalTransactions.textContent =
                    data.total_withdrawal_transactions;

                summaryWithdrawalAmount.textContent =
                    "₹" +
                    Number(
                        data.total_withdrawal_amount
                    ).toLocaleString(
                        "en-IN",
                        {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        }
                    );

                summaryTransferTransactions.textContent =
                    data.total_transfer_transactions;

                summaryTransferAmount.textContent =
                    "₹" +
                    Number(
                        data.total_transfer_amount
                    ).toLocaleString(
                        "en-IN",
                        {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        }
                    );

                summarySuccessfulTransactions.textContent =
                    data.total_successful_transactions;

                summaryFailedTransactions.textContent =
                    data.total_failed_transactions;

                summaryActiveBalance.textContent =
                    "₹" +
                    Number(
                        data.total_active_balance
                    ).toLocaleString(
                        "en-IN",
                        {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        }
                    );

                bankingSummaryMessage.textContent =
                    "Banking summary loaded successfully.";

            } else {

                bankingSummaryMessage.textContent =
                    data.message ||
                    "Unable to load banking summary.";

            }

        })

        .catch(error => {

            console.error(
                "Banking summary error:",
                error
            );

            bankingSummaryMessage.textContent =
                "Unable to connect to the banking server.";

        });

    }

}
const adminBankingSummaryCard =
    document.getElementById(
        "adminBankingSummaryCard"
    );

if (adminBankingSummaryCard) {

    adminBankingSummaryCard.addEventListener(
        "click",
        function () {

            window.location.href =
                "admin-banking-summary.html";

        }
    );

}
const changePasswordForm =
    document.getElementById(
        "changePasswordForm"
    );

if (changePasswordForm) {

    const accountNumber =
        sessionStorage.getItem(
            "accountNumber"
        );

    changePasswordForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            const currentPassword =
                document.getElementById(
                    "currentPassword"
                ).value;

            const newPassword =
                document.getElementById(
                    "newPassword"
                ).value;

            const confirmPassword =
                document.getElementById(
                    "confirmPassword"
                ).value;

            const message =
                document.getElementById(
                    "changePasswordMessage"
                );

            if (!accountNumber) {

                message.textContent =
                    "Customer session not found.";

                return;
            }

            if (
                !currentPassword ||
                !newPassword ||
                !confirmPassword
            ) {

                message.textContent =
                    "Please fill in all password fields.";

                return;
            }

            if (newPassword.length < 6) {

                message.textContent =
                    "New password must contain at least 6 characters.";

                return;
            }

            if (newPassword !== confirmPassword) {

                message.textContent =
                    "New password and confirmation password do not match.";

                return;
            }

            if (currentPassword === newPassword) {

                message.textContent =
                    "New password must be different from the current password.";

                return;
            }

            const confirmation =
                confirm(
                    "Are you sure you want to change your password?"
                );

            if (!confirmation) {

                return;
            }

            message.textContent =
                "Changing password...";

            fetch(
                "/api/change-password",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        account_no:
                            accountNumber,

                        current_password:
                            currentPassword,

                        new_password:
                            newPassword
                    })
                }
            )
            .then(response =>
                response.json()
            )
            .then(data => {

                if (data.status === "success") {

                    message.textContent =
                        data.message;

                    changePasswordForm.reset();

                } else {

                    message.textContent =
                        data.message ||
                        "Unable to change password.";

                }

            })
            .catch(error => {

                console.error(
                    "Change password error:",
                    error
                );

                message.textContent =
                    "Unable to connect to the banking server.";

            });

        }
    );

}

const filterTransactionRangeBtn =
    document.getElementById(
        "filterTransactionRangeBtn"
    );

const clearTransactionRangeBtn =
    document.getElementById(
        "clearTransactionRangeBtn"
    );

const transactionStartDate =
    document.getElementById(
        "transactionStartDate"
    );

const transactionEndDate =
    document.getElementById(
        "transactionEndDate"
    );

const transactionRangeMessage =
    document.getElementById(
        "transactionRangeMessage"
    );


if (filterTransactionRangeBtn) {

    filterTransactionRangeBtn.addEventListener(
        "click",
        function () {

            const startDate =
                transactionStartDate.value;

            const endDate =
                transactionEndDate.value;

            const accountNumber =
                sessionStorage.getItem(
                    "accountNumber"
                );


            if (!startDate || !endDate) {

                transactionRangeMessage.textContent =
                    "Please select both start date and end date.";

                return;
            }


            if (startDate > endDate) {

                transactionRangeMessage.textContent =
                    "Start date cannot be later than end date.";

                return;
            }


            if (!accountNumber) {

                transactionRangeMessage.textContent =
                    "Customer session not found.";

                return;
            }


            transactionRangeMessage.textContent =
                "Loading transactions...";


            fetch(
                `http://127.0.0.1:50001/api/transactions/${accountNumber}/date-range?start_date=${startDate}&end_date=${endDate}`
            )
            .then(response =>
                response.json()
            )
            .then(data => {

                if (data.status === "success") {

                    transactionList.innerHTML =
                        "";


                    if (
                        data.transactions.length === 0
                    ) {

                        transactionList.innerHTML =
                            "<p>No transactions found for the selected date range.</p>";

                        transactionRangeMessage.textContent =
                            "No transactions found.";

                        return;
                    }


                    data.transactions.forEach(
                        transaction => {

                            const transactionCard =
                                document.createElement(
                                    "div"
                                );

                            transactionCard.className =
                                "transaction-card";


                            transactionCard.innerHTML = `
                                <h3>
                                    ${transaction.transaction_type}
                                </h3>

                                <p>
                                    Transaction ID:
                                    ${transaction.transaction_id}
                                </p>

                                <p>
                                    Amount:
                                    ₹${transaction.amount}
                                </p>

                                <p>
                                    Date:
                                    ${transaction.date}
                                </p>

                                <p>
                                    Status:
                                    ${transaction.status}
                                </p>
                            `;


                            transactionList.appendChild(
                                transactionCard
                            );

                        }
                    );


                    transactionRangeMessage.textContent =
                        `${data.transactions.length} transaction(s) found.`;

                } else {

                    transactionRangeMessage.textContent =
                        data.message ||
                        "Unable to filter transactions.";

                }

            })
            .catch(error => {

                console.error(
                    "Date range filter error:",
                    error
                );

                transactionRangeMessage.textContent =
                    "Unable to connect to the banking server.";

            });

        }
    );

}


if (clearTransactionRangeBtn) {

    clearTransactionRangeBtn.addEventListener(
        "click",
        function () {

            transactionStartDate.value =
                "";

            transactionEndDate.value =
                "";

            transactionRangeMessage.textContent =
                "";

            location.reload();

        }
    );

}
const filterTransactionTypeBtn =
    document.getElementById(
        "filterTransactionTypeBtn"
    );

const clearTransactionTypeBtn =
    document.getElementById(
        "clearTransactionTypeBtn"
    );

const transactionTypeFilter =
    document.getElementById(
        "transactionTypeFilter"
    );

const transactionTypeMessage =
    document.getElementById(
        "transactionTypeMessage"
    );


if (filterTransactionTypeBtn) {

    filterTransactionTypeBtn.addEventListener(
        "click",
        function () {

            const selectedType =
                transactionTypeFilter.value;

            const accountNumber =
                sessionStorage.getItem(
                    "accountNumber"
                );


            if (!selectedType) {

                transactionTypeMessage.textContent =
                    "Please select a transaction type.";

                return;
            }


            if (!accountNumber) {

                transactionTypeMessage.textContent =
                    "Customer session not found.";

                return;
            }


            transactionTypeMessage.textContent =
                "Loading transactions...";


            fetch(
                `http://127.0.0.1:50001/api/transactions/${accountNumber}/type?type=${encodeURIComponent(selectedType)}`
            )
            .then(response =>
                response.json()
            )
            .then(data => {

                if (data.status === "success") {

                    transactionList.innerHTML =
                        "";


                    if (
                        data.transactions.length === 0
                    ) {

                        transactionList.innerHTML =
                            "<p>No transactions found for the selected type.</p>";

                        transactionTypeMessage.textContent =
                            "No transactions found.";

                        return;
                    }


                    data.transactions.forEach(
                        transaction => {

                            const transactionCard =
                                document.createElement(
                                    "div"
                                );

                            transactionCard.className =
                                "transaction-card";


                            transactionCard.innerHTML = `
                                <h3>
                                    ${transaction.transaction_type}
                                </h3>

                                <p>
                                    Transaction ID:
                                    ${transaction.transaction_id}
                                </p>

                                <p>
                                    Amount:
                                    ₹${transaction.amount}
                                </p>

                                <p>
                                    Date:
                                    ${transaction.date}
                                </p>

                                <p>
                                    Status:
                                    ${transaction.status}
                                </p>
                            `;


                            transactionList.appendChild(
                                transactionCard
                            );

                        }
                    );


                    transactionTypeMessage.textContent =
                        `${data.transactions.length} transaction(s) found.`;

                } else {

                    transactionTypeMessage.textContent =
                        data.message ||
                        "Unable to filter transactions.";

                }

            })
            .catch(error => {

                console.error(
                    "Transaction type filter error:",
                    error
                );

                transactionTypeMessage.textContent =
                    "Unable to connect to the banking server.";

            });

        }
    );

}


if (clearTransactionTypeBtn) {

    clearTransactionTypeBtn.addEventListener(
        "click",
        function () {

            transactionTypeFilter.value =
                "";

            transactionTypeMessage.textContent =
                "";

            location.reload();

        }
    );

}
const filterTransactionTypeDateBtn =
    document.getElementById(
        "filterTransactionTypeDateBtn"
    );

const clearTransactionTypeDateBtn =
    document.getElementById(
        "clearTransactionTypeDateBtn"
    );

const transactionTypeDateFilter =
    document.getElementById(
        "transactionTypeDateFilter"
    );

const transactionTypeDate =
    document.getElementById(
        "transactionTypeDate"
    );

const transactionTypeDateMessage =
    document.getElementById(
        "transactionTypeDateMessage"
    );


if (filterTransactionTypeDateBtn) {

    filterTransactionTypeDateBtn.addEventListener(
        "click",
        function () {

            const selectedType =
                transactionTypeDateFilter.value;

            const selectedDate =
                transactionTypeDate.value;

            const accountNumber =
                sessionStorage.getItem(
                    "accountNumber"
                );


            if (!selectedType) {

                transactionTypeDateMessage.textContent =
                    "Please select a transaction type.";

                return;
            }


            if (!selectedDate) {

                transactionTypeDateMessage.textContent =
                    "Please select a date.";

                return;
            }


            if (!accountNumber) {

                transactionTypeDateMessage.textContent =
                    "Customer session not found.";

                return;
            }


            transactionTypeDateMessage.textContent =
                "Loading transactions...";


            fetch(
                `http://127.0.0.1:50001/api/transactions/${accountNumber}/type-date?type=${encodeURIComponent(selectedType)}&date=${selectedDate}`
            )
            .then(response =>
                response.json()
            )
            .then(data => {

                if (data.status === "success") {

                    transactionList.innerHTML =
                        "";


                    if (
                        data.transactions.length === 0
                    ) {

                        transactionList.innerHTML =
                            "<p>No transactions found for the selected type and date.</p>";

                        transactionTypeDateMessage.textContent =
                            "No transactions found.";

                        return;
                    }


                    data.transactions.forEach(
                        transaction => {

                            const transactionCard =
                                document.createElement(
                                    "div"
                                );

                            transactionCard.className =
                                "transaction-card";


                            transactionCard.innerHTML = `
                                <h3>
                                    ${transaction.transaction_type}
                                </h3>

                                <p>
                                    Transaction ID:
                                    ${transaction.transaction_id}
                                </p>

                                <p>
                                    Amount:
                                    ₹${transaction.amount}
                                </p>

                                <p>
                                    Date:
                                    ${transaction.date}
                                </p>

                                <p>
                                    Status:
                                    ${transaction.status}
                                </p>
                            `;


                            transactionList.appendChild(
                                transactionCard
                            );

                        }
                    );


                    transactionTypeDateMessage.textContent =
                        `${data.transactions.length} transaction(s) found.`;

                } else {

                    transactionTypeDateMessage.textContent =
                        data.message ||
                        "Unable to filter transactions.";

                }

            })
            .catch(error => {

                console.error(
                    "Type and date filter error:",
                    error
                );

                transactionTypeDateMessage.textContent =
                    "Unable to connect to the banking server.";

            });

        }
    );

}


if (clearTransactionTypeDateBtn) {

    clearTransactionTypeDateBtn.addEventListener(
        "click",
        function () {

            transactionTypeDateFilter.value =
                "";

            transactionTypeDate.value =
                "";

            transactionTypeDateMessage.textContent =
                "";

            location.reload();

        }
    );

}
const sortTransactionsBtn =
    document.getElementById(
        "sortTransactionsBtn"
    );

const clearTransactionSortBtn =
    document.getElementById(
        "clearTransactionSortBtn"
    );

const transactionSort =
    document.getElementById(
        "transactionSort"
    );

const transactionSortMessage =
    document.getElementById(
        "transactionSortMessage"
    );


if (sortTransactionsBtn) {

    sortTransactionsBtn.addEventListener(
        "click",
        function () {

            const selectedSort =
                transactionSort.value;

            const accountNumber =
                sessionStorage.getItem(
                    "accountNumber"
                );


            if (!selectedSort) {

                transactionSortMessage.textContent =
                    "Please select a sorting option.";

                return;
            }


            if (!accountNumber) {

                transactionSortMessage.textContent =
                    "Customer session not found.";

                return;
            }


            transactionSortMessage.textContent =
                "Sorting transactions...";


            fetch(
                `http://127.0.0.1:50001/api/transactions/${accountNumber}/sort?sort=${encodeURIComponent(selectedSort)}`
            )
            .then(response =>
                response.json()
            )
            .then(data => {

                if (data.status === "success") {

                    transactionList.innerHTML =
                        "";


                    if (
                        data.transactions.length === 0
                    ) {

                        transactionList.innerHTML =
                            "<p>No transactions found.</p>";

                        transactionSortMessage.textContent =
                            "No transactions found.";

                        return;
                    }


                    data.transactions.forEach(
                        transaction => {

                            const transactionCard =
                                document.createElement(
                                    "div"
                                );

                            transactionCard.className =
                                "transaction-card";


                            transactionCard.innerHTML = `
                                <h3>
                                    ${transaction.transaction_type}
                                </h3>

                                <p>
                                    Transaction ID:
                                    ${transaction.transaction_id}
                                </p>

                                <p>
                                    Amount:
                                    ₹${transaction.amount}
                                </p>

                                <p>
                                    Date:
                                    ${transaction.date}
                                </p>

                                <p>
                                    Status:
                                    ${transaction.status}
                                </p>
                            `;


                            transactionList.appendChild(
                                transactionCard
                            );

                        }
                    );


                    transactionSortMessage.textContent =
                        `${data.transactions.length} transaction(s) sorted successfully.`;

                } else {

                    transactionSortMessage.textContent =
                        data.message ||
                        "Unable to sort transactions.";

                }

            })
            .catch(error => {

                console.error(
                    "Transaction sorting error:",
                    error
                );

                transactionSortMessage.textContent =
                    "Unable to connect to the banking server.";

            });

        }
    );

}


if (clearTransactionSortBtn) {

    clearTransactionSortBtn.addEventListener(
        "click",
        function () {

            transactionSort.value =
                "";

            transactionSortMessage.textContent =
                "";

            location.reload();

        }
    );

}
// TRANSACTION SUMMARY

const loadTransactionSummaryBtn = document.getElementById("loadTransactionSummaryBtn");

if (loadTransactionSummaryBtn) {

    loadTransactionSummaryBtn.addEventListener("click", async function () {

        const accountNumber = localStorage.getItem("accountNumber");

        if (!accountNumber) {
            document.getElementById("transactionSummaryMessage").textContent =
                "Account information not found.";
            return;
        }

        try {

            const response = await fetch(
                `http://127.0.0.1:50001/api/transactions/${accountNumber}/summary`
            );

            const data = await response.json();

            if (data.status !== "success") {

                document.getElementById("transactionSummaryMessage").textContent =
                    data.message || "Unable to load transaction summary.";

                return;
            }

            document.getElementById("summaryTotalTransactions").textContent =
                data.total_transactions;

            document.getElementById("summaryTotalCredits").textContent =
                Number(data.total_credits).toFixed(2);

            document.getElementById("summaryTotalDebits").textContent =
                Number(data.total_debits).toFixed(2);

            document.getElementById("transactionSummaryMessage").textContent =
                "Transaction summary loaded successfully.";

        } catch (error) {

            console.error("Transaction summary error:", error);

            document.getElementById("transactionSummaryMessage").textContent =
                "Unable to connect to the server.";

        }

    });

}
// TRANSACTION SEARCH

const searchTransactionBtn = document.getElementById("searchTransactionBtn");

if (searchTransactionBtn) {

    searchTransactionBtn.addEventListener("click", async function () {

        const accountNumber = sessionStorage.getItem("accountNumber");
        
        const searchInput = document.getElementById("transactionSearchInput");
        const message = document.getElementById("transactionSearchMessage");
        const results = document.getElementById("transactionSearchResults");

        const searchText = searchInput.value.trim();

        results.innerHTML = "";
        message.textContent = "";

        if (!accountNumber) {
            message.textContent = "Account information not found.";
            return;
        }

        if (!searchText) {
            message.textContent = "Please enter a transaction ID.";
            return;
        }

        try {

            const response = await fetch(
                `http://127.0.0.1:50001/api/transactions/${accountNumber}/search?q=${encodeURIComponent(searchText)}`
            );

            const data = await response.json();

            if (data.status !== "success") {
                message.textContent =
                    data.message || "Unable to search transactions.";
                return;
            }

            if (data.transactions.length === 0) {
                message.textContent = "No matching transaction found.";
                return;
            }

            data.transactions.forEach(function (transaction) {

                const card = document.createElement("div");

                card.className = "transaction-card";

                card.innerHTML = `
                    <h3>${transaction.transaction_type}</h3>

                    <p>
                        <strong>Transaction ID:</strong>
                        ${transaction.transaction_id}
                    </p>

                    <p>
                        <strong>Amount:</strong>
                        ₹${Number(transaction.amount).toFixed(2)}
                    </p>

                    <p>
                        <strong>Date:</strong>
                        ${transaction.date || "N/A"}
                    </p>

                    <p>
                        <strong>Status:</strong>
                        ${transaction.status}
                    </p>

                    <p>
                        <strong>Sender Account:</strong>
                        ${transaction.sender_account || "N/A"}
                    </p>

                    <p>
                        <strong>Receiver Account:</strong>
                        ${transaction.receiver_account || "N/A"}
                    </p>
                `;

                results.appendChild(card);

            });

            message.textContent =
                `${data.transactions.length} transaction(s) found.`;

        } catch (error) {

            console.error("Transaction search error:", error);

            message.textContent =
                "Unable to connect to the server.";

        }

    });

}
// CLEAR TRANSACTION SEARCH

const clearTransactionSearchBtn = document.getElementById("clearTransactionSearchBtn");

if (clearTransactionSearchBtn) {

    clearTransactionSearchBtn.addEventListener("click", function () {

        document.getElementById("transactionSearchInput").value = "";

        document.getElementById("transactionSearchMessage").textContent = "";

        document.getElementById("transactionSearchResults").innerHTML = "";

    });

}
// EXPORT ACCOUNT STATEMENT

const exportAccountStatementBtn = document.getElementById("exportAccountStatementBtn");

if (exportAccountStatementBtn) {

    exportAccountStatementBtn.addEventListener("click", function () {

        const accountNumber = session
        Storage.getItem("accountNumber");

        const message = document.getElementById("exportStatementMessage");

        if (!accountNumber) {

            message.textContent =
                "Account information not found.";

            return;
        }

        const downloadUrl =
            `http://127.0.0.1:50001/api/transactions/${accountNumber}/export`;

        const link = document.createElement("a");

        link.href = downloadUrl;

        link.download =
            `account_statement_${accountNumber}.csv`;

        document.body.appendChild(link);

        link.click();

        document.body.removeChild(link);

        message.textContent =
            "Account statement exported successfully.";

    });

}
