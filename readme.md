# Expense Sharing Application Readme

## Design Overview

The Expense Sharing Application is designed to allow users to add and split expenses among a group of people. It keeps track of balances between users, indicating who owes how much to whom. The application is built with the following key components:

### Architecture Diagram

                                 +------------------+
                                 |     Frontend     |
                                 +------------------+
                                          |
                                   (HTTP Requests)
                                          |
                                 +------------------+
                                 |    Web Server    |
                                 +------------------+
                                          |
                                 (Processes Requests)
                                          |
                                 +------------------+
                                 |     Django       |
                                 |   Application    |
                                 | (Expense Models, |
                                 |  Views, etc.)    |
                                 +------------------+
                                          |
                              (Handles Business Logic)
                                          |
                                 +------------------+
                                 |     Database     |
                                 +------------------+

## API Endpoints

### User Management

- `POST /api/users/`: Create a new user.
- `GET /api/users/`: Retrieve a list of all users.


### Expense Management

- `POST /api/expenses/`: Create a new expense.


### Balance Management

- `GET /api/balances/`: Retrieve balances for user.


### Scheduled Jobs

- A scheduled job will run weekly to send emails containing total amounts owed by users to each other.

## Database Schema

The application uses a relational database to store user information, expenses, and balances. The schema includes the following tables:

- `User`: Contains user information (userId, name, email, mobile number).
- `Expense`: Stores details of each expense (expenseId, name, totalAmount, createdBy, type).
- `Participant`: Links users to expenses and includes their share information (expenseId, userId, shareType, amount).
- `Balance`: Tracks balances between users (userId, debtorId, amount).

## Classes and Interfaces

The backend is structured with the following classes:

- `UserModel`: Handles user-related operations.
- `ExpenseModel`: Manages expense creation, retrieval, and modification.
- `BalanceModel`: Handles balance calculations and simplification.
- `ScheduledJob`: Sends weekly reminder emails.

## Optional Features

- The application supports additional features such as expense names, notes, images, and split by share.

## Response Time

All API responses are designed to take less than 50 milliseconds.

## GitHub Repository

The code for this Expense Sharing Application can be found in the [GitHub repository](https://github.com/shameemm/SplitWise-Expense-Management).

For more detailed information on API contracts and class structures, please refer to the respective source code files.
