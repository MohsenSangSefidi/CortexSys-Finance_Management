# Finance Management API

🚀 **معرفی پروژه**

پروژه Finance Management Project یک API سبک‌وزن و قدرتمند برای کمک به کاربران در مدیریت مالی شخصی و کسب‌وکارهای کوچک است. این سیستم امکان ردیابی درآمد، هزینه‌ها، بودجه‌ها و اهداف مالی را به روشی امن و سازمان‌یافته فراهم می‌کند.

## 🛠 **تکنولوژی‌های استفاده شده**

- **Backend**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Token)
- **Containerization**: Docker
- **Testing**: pytest 

## 📁 **ساختار پروژه**

```
finance_management/
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── finance_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── managers.py
│   ├── migrations/
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests/
│   └── views.py
├── transactions/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests/
│   └── views.py
├── budgets/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests/
│   └── views.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## ⚙️ **نصب و راه‌اندازی**

### پیش‌نیازها

- Docker
- Python 3.8+ و PostgreSQL

### راه‌اندازی با Docker (توصیه شده)

1. **Clone Project**:
   ```bash
   git clone https://github.com/yourusername/finance-management-api.git
   cd finance-management-api
   ```

2. **.env**:
   ```.env
   # Django Settings
   DEBUG=1
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
   
   # Database Settings ( For Run Without Docker )
   POSTGRES_DB=finance_management_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   
   # Database URL ( Add it When Want Run With Docker )
   DATABASE_URL=postgresql://postgres:postgres@db:5432/finance_management_db
   ```
    
3. **اجرای پروژه با Docker Compose**:
   ```bash
   docker-compose up --build
   ```

4. **اجرای migrations**:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **ایجاد کاربر سوپرادمین**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **دسترسی به پروژه**:
   - API: http://0.0.0.0:8000

### راه‌اندازی برای توسعه (بدون Docker)

1. **نصب dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **تنظیمات**:
   - یک دیتابیس PostgreSQL ایجاد کنید
   - فایل settings.py را با اطلاعات دیتابیس خود به روز کنید

3. **.env**:
   ```.env
   # Django Settings
   DEBUG=1
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
   
   # Database Settings ( For Run Without Docker )
   POSTGRES_DB=finance_management_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

4. **اجرای migrations**:
   ```bash
   python manage.py migrate
   ```

5. **ایجاد کاربر سوپرادمین**:
   ```bash
   python manage.py createsuperuser
   ```

6. **اجرای سرور**:
   ```bash
   python manage.py runserver
   ```

## 📊 **مدل‌های دیتابیس**

### User
- `id` - شناسه کاربر
- `username` - نام کاربری
- `email` - ایمیل
- `password` - رمز عبور

### Transaction
- `id` - شناسه تراکنش
- `title` - عنوان تراکنش
- `amount` - مبلغ
- `type` - نوع (درآمد/هزینه)
- `date` - تاریخ
- `notes` - یادداشت‌ها
- `user_id` - کلید خارجی به کاربر

### Budget
- `id` - شناسه بودجه
- `title` - عنوان بودجه
- `total_amount` - مبلغ کل
- `start_date` - تاریخ شروع
- `end_date` - تاریخ پایان
- `user_id` - کلید خارجی به کاربر

## 📚 **مستندات API**

مستندات کامل API به صورت تعاملی در دسترس است:

- **Api Dog**: [مشاهده](https://share.apidog.com/4b7ea7f3-044c-4fa5-934b-3ad39e0f9619)


## 🧪 **Tests**

برای اجرای تست‌ها از دستور زیر استفاده کنید:

```bash
# با Docker
docker-compose exec web pytest

# یا بدون Docker
pytest
```

هر اپلیکیشن (accounts، transactions، budgets) دارای تست‌های مخصوص به خود است.

## 🐳 **Dockerization**

پروژه به طور کامل داکرایز شده است و شامل سرویس‌های زیر می‌باشد:

- **web**: اپلیکیشن Django
- **db**: پایگاه داده PostgreSQL

برای مدیریت کانتینرها:

```bash
# راه‌اندازی سرویس‌ها
docker-compose up -d

# توقف سرویس‌ها
docker-compose down

# مشاهده لاگ‌ها
docker-compose logs -f web

# اجرای دستورات مدیریتی
docker-compose exec web python manage.py <command>
```

## 📄 **لایسنس**

این پروژه تحت لایسنس MIT منتشر شده است.

⭐ **اگر این پروژه رو دوست داشتید، بهش ستاره بدید!**