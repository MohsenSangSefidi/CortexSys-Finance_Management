# Finance Management API

## 🚀 معرفی پروژه

پروژه Finance Management Project یک API سبک‌وزن و قدرتمند برای کمک به کاربران در مدیریت مالی شخصی و کسب‌وکارهای کوچیک است. این سیستم امکان ردیابی درآمد، هزینه‌ها، بودجه‌ها و اهداف مالی را به روشی امن و سازمان‌یافته فراهم می‌کند.

## 🛠 تکنولوژی‌های استفاده شده

- **Backend**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Token)
- **Testing**: pytest (هر اپلیکیشن تست‌های مخصوص به خود را دارد)

### Documantion
ApiDog : https://share.apidog.com/4b7ea7f3-044c-4fa5-934b-3ad39e0f9619

## 📁 ساختار پروژه

```
finance_management/
├── manage.py
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

## ⚙️ نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8+
- PostgreSQL

### مراحل نصب

1. کلون کردن ریپازیتوری:
```bash
git clone https://github.com/yourusername/finance-management-api.git
cd finance-management-api
```

2. نصب dependencies:
```bash
pip install -r requirements.txt
```

3. تنظیمات دیتابیس:
- یک دیتابیس PostgreSQL ایجاد کنید
- فایل `settings.py` را با اطلاعات دیتابیس خود به روز کنید

4. اجرای migrations:
```bash
python manage.py migrate
```

5. ایجاد کاربر سوپرادمین:
```bash
python manage.py createsuperuser
```

6. اجرای سرور:
```bash
python manage.py runserver
```

## 🗃 مدل‌های دیتابیس

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

## 🧪 تست‌ها

برای اجرای تست‌ها از دستور زیر استفاده کنید:

```bash
pytest
```

هر اپلیکیشن (accounts، transactions، budgets) دارای تست‌های مخصوص به خود است.


## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.


## 🤝 مشارکت

مشارکت‌ها، ایسوها و درخواست‌های pull همیشه مورد استقبال هستند!


---


⭐ اگر این پروژه رو دوست داشتید، بهش ستاره بدید!
