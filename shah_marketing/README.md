# Shah Marketing Pune LLP - B2B E-commerce Backend

Production-ready Django REST backend for dealer/retailer/plumber order punching.

## Features
- Custom JWT authentication with role-based user model.
- Product and category management.
- Cart and bulk order placement with stock validation.
- Order history and status tracking.
- Admin-only product/order management APIs.
- Sales analytics endpoint for dashboarding.
- Django admin enhancements: filters, search, stock warnings.

## Project Structure
```
shah_marketing/
  manage.py
  shah_marketing/
    settings.py
    urls.py
  apps/
    accounts/
    products/
    orders/
    dashboard/
```

## Setup Instructions
1. **Create virtual environment and install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.sample .env
   ```
   Update DB and secret variables.

3. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE shah_marketing_db;
   ```

4. **Run migrations and create admin user**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

## Core API Endpoints
### Authentication
- `POST /api/register/`
- `POST /api/login/`
- `POST /api/token/refresh/`
- `GET /api/profile/`

### Products
- `GET /api/products/`
- `GET /api/products/<id>/`
- `GET /api/categories/`
- `GET|POST /api/admin/products/` (Admin only)
- `GET|PATCH|DELETE /api/admin/products/<id>/` (Admin only)

### Cart
- `POST /api/cart/add/`
- `GET /api/cart/`
- `DELETE /api/cart/remove/<id>/`

### Orders
- `POST /api/orders/create/`
- `GET /api/orders/`
- `GET /api/orders/<id>/`
- `PATCH /api/admin/orders/<id>/status/` (Admin only)

### Dashboard
- `GET /api/dashboard/sales-analytics/` (Admin only)

## Security Notes
- JWT bearer auth for API endpoints.
- CSRF middleware enabled for admin/session flows.
- Password validators enforced.
- DB credentials sourced from environment variables.
- Secure cookie settings auto-enabled when `DEBUG=False`.

## Deployment Notes
- Use Gunicorn + Nginx.
- Serve static files via `collectstatic`.
- Use object storage/CDN for media in production.
- Add centralized logging (Sentry/ELK) and monitoring.
