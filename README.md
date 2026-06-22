
# 🛒 FastAPI E-Commerce Backend System

### A scalable and secure e-commerce backend system built using FastAPI, SQLAlchemy, and PostgreSQL with full authentication, cart, and order management.

---

## 🚀 Live Demo

🔗 **Live API:**
[FastAPI E-Commerce Backend System](https://fastapi-ecommerce-backend-system.onrender.com)

📄 **API Docs (Swagger UI):**
[API Documentation](https://fastapi-ecommerce-backend-system.onrender.com/docs)

> ⚠️ Hosted on Render free tier — first request may be slow due to cold starts.

---

## 🛠 Tech Stack

* **Backend Framework:** FastAPI
* **Database:** PostgreSQL (Neon)
* **ORM:** SQLAlchemy
* **Authentication:** JWT (python-jose)
* **Password Hashing:** Passlib (bcrypt)
* **Server:** Uvicorn
* **Validation:** Pydantic
* **Deployment:** Render

---

## 💡 Features

* 👤 User registration & login system
* 🔐 JWT-based authentication
* 🔑 Secure password hashing (bcrypt)
* 📦 Product management (add & view products)
* 🛒 Cart system (add, view, remove items)
* 💰 Real-time cart total calculation
* 📑 Order creation from cart
* 📉 Automatic stock management
* 📜 Order history & order details
* ⚡ Fully RESTful API design
* 📄 Interactive Swagger documentation

---

## 📂 Project Structure

```
fastapi-ecommerce-backend-system/
├── main.py              # API endpoints & business logic
├── models.py            # Database models (User, Item, Cart, Order)
├── database.py          # DB connection & session setup
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
├── .gitignore           # Ignored files
└── README.md            # Project documentation
```

---

## ⚙️ Database Models

### 👤 User

* id
* name
* email (unique)
* password

### 📦 Item (Product)

* id
* name
* description
* price
* stock_quantity

### 🛒 Cart

* id
* user_id (FK)
* product_id (FK)
* quantity

### 📑 Order

* id
* user_id (FK)
* total_amount
* status
* created_at

### 📦 OrderItem

* id
* order_id (FK)
* product_id (FK)
* quantity
* price_at_purchase

---

## 🚀 Installation & Local Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/PavanSurisetti/FastAPI-Ecommerce-Backend-System
```

### 2️⃣ Navigate to project

```bash
cd FastAPI-Ecommerce-Backend-System
```

### 3️⃣ Create virtual environment

```bash
python -m venv venv
```

**Activate:**

* Windows:

```bash
venv\Scripts\activate
```

* Mac/Linux:

```bash
source venv/bin/activate
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Configure environment variables

Create `.env` file:

```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

### 6️⃣ Run the server

```bash
uvicorn main:app --reload
```

### 7️⃣ Open API docs

```
http://127.0.0.1:8000/docs
```

---

## 🔗 API Endpoints

| Method | Endpoint              | Description            |
| ------ | --------------------- | ---------------------- |
| GET    | `/`                   | Welcome message        |
| POST   | `/register`           | Register user          |
| POST   | `/login`              | Login user (JWT token) |
| GET    | `/profile`            | Get user profile       |
| POST   | `/product`            | Add product            |
| GET    | `/Products`           | Get all products       |
| GET    | `/product/{id}`       | Get product by ID      |
| POST   | `/cart`               | Add item to cart       |
| GET    | `/cart`               | View cart              |
| DELETE | `/cart/remove/{id}`   | Remove item from cart  |
| POST   | `/order/create`       | Create order           |
| GET    | `/orders/view`        | View all orders        |
| GET    | `/order/details/{id}` | Order details          |

---

## 🧠 How It Works

1. User registers and logs in
2. JWT token is generated for authentication
3. User adds products to cart
4. Cart calculates total dynamically
5. Order is created from cart items
6. Stock is reduced automatically
7. Cart is cleared after order placement

---

## 🚀 Deployment

* Hosted on **Render**
* Database powered by **Neon PostgreSQL**
* Environment variables securely managed
* Auto deployment via GitHub integration

---

## 🔮 Future Improvements

* Role-based access (Admin/User)
* Product categories & filters
* Pagination for products & orders
* Email notifications for orders
* Docker containerization
* Payment gateway integration 💳

---

## 📫 Contact

* GitHub: [PavanSurisetti](https://github.com/PavanSurisetti)
* LinkedIn: [Pavan Surisetti LinkedIn](https://www.linkedin.com/in/pavan-surisetti-b3281228b/)

---

## 📄 License

This project is licensed under the **MIT License**.
