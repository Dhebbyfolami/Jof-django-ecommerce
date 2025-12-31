# 🛒 JOF — Django E-Commerce Platform

![Django](https://img.shields.io/badge/Django-4.x-darkgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Render](https://img.shields.io/badge/Deployed%20on-Render-purple)
![Status](https://img.shields.io/badge/Status-Test%20Ready-success)

---

## 👋 Introduction

**JOF** is a Django-based e-commerce web application built to simulate a real online shopping experience.

This project was created as a **practical, hands-on build**, not just a tutorial clone.  
It focuses on real-world concepts such as cart management, checkout flow, payment options, and deployment readiness.

The goal is simple:  
👉 *Anyone should be able to open the app, browse products, add to cart, checkout, and place an order.*

---

## 🌍 Live Demo (Test Environment)

🔗 **Live App:**  

> This deployment is for **viewing and testing purposes only**.  
> Payment gateways run in **test mode**.

---

## ✨ Key Features

### 🛍️ Store
- Product listing
- Category-based browsing
- Clean and responsive UI

### 🛒 Cart
- Add products to cart
- Increase or decrease quantity
- Remove items
- Dynamic cart total

### 📦 Checkout & Orders
- Checkout form
- Order creation
- Order confirmation page
- Order status tracking (Pending / Paid)

### 💳 Payment Options
- 💵 Cash on Delivery
- 🌊 Flutterwave (Test Mode)
- 💳 Paystack (Test Mode)

### 👤 Users
- Authentication (login / logout)
- Session-based cart handling

---

## 🧩 Project Structure (Simple Explanation)

jof/
├── accounts/        # User authentication
├── cart/            # Cart logic (add, remove, decrease)
├── store/           # Products, categories, listings
├── payments/        # Flutterwave & Paystack integrations
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── media/           # Uploaded files
├── jof/             # Django settings & configuration
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
└── README.md

Each app is **modular**, making the project easy to maintain and extend.

---

## 🛍️ Cart Logic (In Plain English)

- Every visitor has a session-based cart
- Items can be:
  - ➕ Added
  - ➖ Reduced
  - ❌ Removed
- Cart total updates automatically
- Cart persists until checkout or manual removal

---

## 💳 Payments (Important Note)

All online payments are currently in **test mode**.

| Method | Purpose |
|------|--------|
| Cash on Delivery | Works without API keys |
| Flutterwave | Test integration |
| Paystack | Test integration |

No real money is processed in this deployment.

---

## 📸 Screenshots

*(Screenshots will be added here)*

```md
[![Shop Page](screenshots/cart.png)
```

```md
![Cart 

```md
![Checkout Page](screenshot/Jof _ Checkout -.png)



```md
![Order success Page](screenshots/cart.png)
```

⸻

🚀 Deployment

The application is deployed using:
	•	Render
	•	Gunicorn (production server)
	•	WhiteNoise (static files)
	•	Environment variables for security

The deployment is optimized for easy access and testing.

⸻

⚙️ Tech Stack
	•	Backend: Django (Python)
	•	Frontend: HTML, Bootstrap, CSS
	•	Database: SQLite (testing)
	•	Payments: Flutterwave, Paystack
	•	Deployment: Render
	•	Version Control: Git & GitHub

⸻

🧠 Why This Project Exists

This project was built to:
	•	Practice real-world Django development
	•	Understand cart & checkout logic deeply
	•	Work with multiple payment gateways
	•	Learn deployment workflows
	•	Build something reusable and extendable

It reflects how I approach practical problem-solving, not just following tutorials.

⸻

📈 Future Improvements

Planned enhancements include:
	•	Admin sales dashboard
	•	Order status updates
	•	Email notifications
	•	Inventory management
	•	PostgreSQL database
	•	Payment verification webhooks

⸻

🤝 Feedback & Collaboration

If you’re reviewing or testing this project:
	•	Explore the live demo
	•	Try different checkout options
	•	Share feedback or suggestions

This project is open to learning and improvement.

⸻

👤 Author

Project Name: JOF
Built by: DhebbyFolami
Role: Django Developer
Focus: Practical, scalable web solutions

⸻

⭐ If you find this project helpful, feel free to star the repository.

