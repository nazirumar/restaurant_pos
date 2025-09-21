# Restaurant POS SaaS

Welcome to the Restaurant POS SaaS, a multi-tenant Point of Sale (POS) system built with Django and `django-tenants` for schema-based tenancy. This application allows restaurant owners to manage menus, orders, inventory, employees, and reports, with support for multiple tenants (e.g., branches) accessible via subdomains (e.g., `demo.localhost:8000`, `lang.localhost:8000`). The system includes a professional dashboard and role-based access control for admin interfaces.

## Features
- **Multi-Tenant Support**: Each tenant (branch) has its own isolated database schema.
- **Dashboard**: Displays pending orders, low stock alerts, and today's sales.
- **Admin Access Control**:
  - Public admin (`http://localhost:8000/admin/`) restricted to staff users.
  - Subdomain admin (e.g., `http://demo.localhost:8000/admin/`) restricted to superusers.
- **Modules**: Manage menus, orders, inventory, employees, and reports.
- **Responsive Design**: Built with Tailwind CSS for a modern UI.
- **Authentication**: Custom user model with role-based permissions.

## Prerequisites
- **Python 3.8+**
- **PostgreSQL** (required for schema support)
- **pip** and **virtualenv** (for environment management)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/restaurant_pos.git
cd restaurant_pos
```

### 2. Set Up a Virtual Environment
```bash
python -m venv .pos_venv
source .pos_venv/bin/activate  # On Windows: .pos_venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL
- Install PostgreSQL and create a database named `restaurant_pos`.
- Update `restaurant_pos/settings.py` with your PostgreSQL credentials:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django_tenants.postgresql_backend',
          'NAME': 'restaurant_pos',
          'USER': 'your_postgres_user',
          'PASSWORD': 'your_postgres_password',
          'HOST': 'localhost',
          'PORT': '5432',
      }
  }
  ```

### 5. Configure Hosts
- Edit your `/etc/hosts` file (or `C:\Windows\System32\drivers\etc\hosts` on Windows with admin privileges) to add:
  ```
  127.0.0.1   demo.localhost
  127.0.0.1   lang.localhost
  ```
- Flush DNS cache if needed:
  ```bash
  ipconfig /flushdns  # Windows
  ```

### 6. Apply Migrations
```bash
python manage.py migrate_schemas --shared
python manage.py migrate_schemas --tenant demo
python manage.py migrate_schemas --tenant lang
```

### 7. Create Superuser and Admin Users
- Create a superuser for all tenants:
  ```bash
  python manage.py createsuperuser
  ```
  - Example: `username=admin`, `email=admin@example.com`, `password=admin123` (set `is_superuser=True` and `is_staff=True`).
- Create a staff user for the public schema:
  ```python
  python manage.py shell
  >>> from users.models import User
  >>> User.objects.create_user(username='public_admin', password='public123', is_staff=True)
  ```

### 8. Run the Development Server
```bash
python manage.py runserver
```
- Access the public admin at `http://localhost:8000/admin/` (staff only).
- Access tenant dashboards at `http://demo.localhost:8000/` or `http://lang.localhost:8000/` (superuser for `/admin/`).

## Usage
- **Public Admin**: Log in with a staff user (e.g., `public_admin`) to manage tenants and users.
- **Tenant Admin**: Log in with a superuser (e.g., `admin`) to manage tenant-specific data (e.g., `http://demo.localhost:8000/admin/`).
- **Dashboard**: View pending orders, low stock items, and sales data after logging in as a tenant user.

## Project Structure
```
restaurant_pos/
├── manage.py
├── restaurant_pos/         # Project settings and URLs
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── urls_public.py
│   └── wsgi.py
├── tenants/               # Tenant and domain models
│   ├── __init__.py
│   ├── models.py
│   └── middleware.py      # Optional custom middleware
├── users/                 # Custom user model
├── menu/                  # Menu management app
├── orders/                # Order management app
├── inventory/             # Inventory management app
├── employees/             # Employee management app
├── dashboard/             # Dashboard app
├── templates/             # HTML templates
│   ├── base.html
│   └── dashboard.html
├── static/                # Static files
└── requirements.txt       # Python dependencies
```

## Configuration
- **Settings**: Adjust `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` in `settings.py` for production.
- **Tenants**: Add more tenants via the admin interface or shell:
  ```python
  from tenants.models import Tenant, Domain
  tenant = Tenant.objects.create(name="New Restaurant", subdomain="new")
  Domain.objects.create(tenant=tenant, domain="new.localhost", is_primary=True)
  python manage.py migrate_schemas --tenant new
  ```

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome-feature`).
3. Commit changes (`git commit -m "Add awesome feature"`).
4. Push to the branch (`git push origin feature/awesome-feature`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
For issues or questions, please open an issue on the GitHub repository or contact support@x.ai.

## Acknowledgments
- Built with [Django](https://www.djangoproject.com/) and [django-tenants](https://django-tenants.readthedocs.io/).
- Styled with [Tailwind CSS](https://tailwindcss.com/).