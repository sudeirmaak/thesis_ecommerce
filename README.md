# Dibek Coffee: E-Commerce Platform & Recommendation Engine

## Project Overview
Dibek Coffee is a fully functional, mobile-responsive e-commerce platform built with Django. It features a custom **Content-Based Recommendation Engine** powered by Scikit-Learn and Pandas, designed to solve the "choice overload" problem by recommending coffees based on text-based features (TF-IDF vectorization and Cosine Similarity). Financial transactions are securely handled via the Stripe API.

## Tech Stack
**Backend:** Python, Django 6.0.3, SQLite (Development)
**Machine Learning:** Scikit-Learn, Pandas, NumPy
**Frontend:** HTML5, CSS3, Bootstrap 5, Django Crispy Forms
**Payment Gateway:** Stripe API & Webhooks
**Architecture:** MVT (Model-View-Template), Fat Models, Data Immutability 

## Local Installation & Setup

**1. Clone the repository**
`git clone https://github.com/sudeirmaak/thesis_ecommerce.git`
`cd thesis_ecommerce`

**2. Create and activate a virtual environment**
`python -m venv venv`
`source venv/bin/activate` (Mac/Linux) OR `venv\Scripts\activate` (Windows)

**3. Install dependencies**
`pip install -r requirements.txt`

**4. Environment Variables**
Rename `.env.example` to `.env` and input the secure keys provided by the author.

**5. Run Database Migrations**
`python manage.py makemigrations`
`python manage.py migrate`

**6. Start the Local Development Server**
`python manage.py runserver`

**7. (Optional) Start Stripe Webhook Listener**
To test the checkout webhook locally, run the Stripe CLI:
`stripe listen --forward-to localhost:8000/webhook/`