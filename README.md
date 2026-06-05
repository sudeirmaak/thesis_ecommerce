# Dibek Coffee: E-Commerce Platform & Recommendation Engine

## Project Overview

Dibek Coffee is a fully functional, mobile-responsive e-commerce platform built with Django.

It features a custom **Content-Based Recommendation Engine** powered by Scikit-Learn and Pandas, designed to solve the "choice overload" problem by recommending coffees based on text-based features using **TF-IDF Vectorization** and **Cosine Similarity**.

Financial transactions are securely handled via the **Stripe API**.

## Tech Stack

* **Backend:** Python, Django 6.0.3, SQLite (Development)
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
* **Frontend:** HTML5, CSS3, Bootstrap 5, Django Crispy Forms
* **Payment Gateway:** Stripe API & Webhooks
* **Architecture:** MVT (Model-View-Template), Fat Models, Data Immutability

---

## Local Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sudeirmaak/thesis_ecommerce.git
cd thesis_ecommerce
```

### 2. Create and Activate a Virtual Environment

#### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Rename:

```text
.env.example
```

to:

```text
.env
```

Then add the required secure keys provided by the project author.

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the Local Development Server

```bash
python manage.py runserver
```

### 7. (Optional) Start the Stripe Webhook Listener

To test checkout webhooks locally, run:

```bash
stripe listen --forward-to localhost:8000/webhook/
```
