# 💰 Finance Data Processing & Access Control Backend

## 📌 Project Overview

This project is a backend system for managing financial data and user access control. It provides APIs for handling users, financial transactions, and dashboard analytics with role-based permissions.

The system is designed to demonstrate backend engineering concepts such as API design, database modeling, access control, validation, and data aggregation.

---

## 🚀 Tech Stack

* **Backend Framework:** Flask (Python)
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **API Testing:** Thunder Client (VS Code)

---

## ⚙️ Features Implemented

### 👤 User & Role Management

* Create users
* Assign roles (Admin, Analyst, Viewer)
* Manage user status

### 💰 Financial Records Management

* Create transactions
* View transactions
* Update transactions
* Delete transactions
* Filter transactions by type (income/expense)

### 📊 Dashboard Summary APIs

* Total Income
* Total Expenses
* Net Balance calculation

### 🔐 Role-Based Access Control

* Admin → Full access (create transactions)
* Analyst → Access dashboard
* Viewer → Limited access

### ✅ Input Validation & Error Handling

* Required field validation
* Data validation (amount, type)
* Proper error responses with status codes

### 🗄️ Data Persistence

* SQLite database used for storing users and transactions

---

## 📂 Project Structure

```
finance-backend/
│
├── app.py
├── models.py
├── requirements.txt
│
├── routes/
│   ├── user_routes.py
│   ├── transaction_routes.py
│   └── dashboard_routes.py
│
├── utils/
│   └── role_checker.py
```

---

## ⚙️ Setup Instructions

1. Clone the repository:

```
git clone https://github.com/avishgithub/finance-backend.git
cd finance-backend
```

2. Create virtual environment:

```
python -m venv venv
venv\Scripts\activate   (Windows)
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run the application:

```
python app.py
```

---

## 🌐 API Endpoints

### 👤 Users

* **POST /users** → Create user
* **GET /users** → Get all users

---

### 💰 Transactions

* **POST /transactions → Create transaction (Admin only)
* **GET /transactions → Get all transactions
* **GET /transactions?type=income → Filter transactions
* **PUT /transactions/<id> → Update transaction (Admin only)
* **DELETE /transactions/<id> → Delete transaction (Admin only)

---

### 📊 Dashboard

* **GET /dashboard** → Get summary (Admin, Analyst)

---

## 🔐 Access Control

| Role    | Permissions         |
| ------- | ------------------- |
| Admin   | Full access         |
| Analyst | View dashboard      |
| Viewer  | Limited (read-only) |

Role is passed via request headers:

```
role: admin
```

---

## 🧠 Technical Decisions & Trade-offs

* Flask was chosen for its simplicity and flexibility, allowing rapid backend development.
* SQLite was used for ease of setup and lightweight storage.
* SQLAlchemy ORM was used to manage database interactions cleanly.
* Role-based access control is implemented using request headers instead of full authentication to keep the scope focused.
* Modular project structure was used for better maintainability and readability.

Trade-offs:

* No authentication (JWT/session) implemented to keep the project simple.
* SQLite used instead of production-grade database.
* Minimal UI (backend-only project).

---

## 📝 Additional Notes

* APIs were tested using Thunder Client.
* The project is designed for demonstration purposes and can be extended easily.
* Possible future improvements:

  * JWT Authentication
  * Pagination
  * Swagger API documentation
  * Advanced filtering

---

## ✅ Conclusion

This project demonstrates a complete backend system with proper architecture, access control, validation, and data processing. It focuses on clarity, correctness, and maintainability.
