# KIUF Elektron Kutubxona

Korea International University Fergana (KIUF) uchun Django asosida yaratilgan elektron kutubxona tizimi.

## Xususiyatlar

### Autentifikatsiya
- **Talaba kirishi**: Faqat HEMIS ID orqali (parol talab qilinmaydi)
- **Admin kirishi**: Django admin paneli orqali (parol bilan)
- Session-based autentifikatsiya

### Asosiy funktsiyalar
- Kitoblar katalogi (qidiruv, filter, sahifalash)
- Kitob tafsilotlari va o'qish
- Kitoblarni saqlash
- O'qish tarixi
- Statistika
- E'lonlar tizimi

## O'rnatish

1. Virtual muhit yaratish:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Dependencies larni o'rnatish:
```bash
pip install -r requirements.txt
```

3. Migratsiyalarni qo'llash:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Superuser yaratish:
```bash
python manage.py createsuperuser
```

5. Serverni ishga tushurish:
```bash
python manage.py runserver
```

## Konfiguratsiya

### Admin panel
- URL: `/admin/`
- Superuser orqali kirish

### Talaba uchun
- Kirish: `/accounts/login/`
- Faqat HEMIS ID talab qilinadi

## Proyekt tuzilmasi

```
kiuf_elib/
├── manage.py
├── requirements.txt
├── kiuf_elib/          # Asosiy config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── library/            # Asosiy app
│   ├── models.py       # Book, Category, Journal, Announcement
│   ├── views.py        # Barcha viewlar
│   ├── urls.py
│   ├── admin.py
│   └── forms.py
├── accounts/           # Autentifikatsiya app
│   ├── models.py       # Student (HEMIS ID)
│   ├── views.py        # login, logout
│   ├── urls.py
│   └── backends.py     # Custom auth backend
└── templates/
    ├── base.html
    ├── accounts/
    │   └── login.html
    └── library/
        ├── index.html
        ├── books.html
        ├── book_detail.html
        ├── saved_books.html
        └── reading_history.html
```

## Modellar

### Student (Custom User)
- `hemis_id` - HEMIS ID (login uchun)
- `full_name` - To'liq ism
- `faculty` - Fakultet
- `specialty` - Mutaxassislik
- `year` - Kurs

### Book
- `title` - Sarlavha
- `author` - Muallif
- `description` - Tavsif
- `category` - Kategoriya
- `file` - PDF fayl
- `badge` - NEW/HOT/FREE/PDF
- `rating` - Reyting
- `read_count` - O'qilganlar soni
- `download_count` - Yuklab olishlar soni

### Category
- `name` - Nomi
- `emoji` - Emoji
- `color` - Rang
- `slug` - URL slug

### ReadingHistory
- `student` - Talaba
- `book` - Kitob
- `progress` - Progress (%)
- `last_page` - Oxirgi sahifa
- `last_read` - Oxirgi o'qilgan vaqt

### SavedBook
- `student` - Talaba
- `book` - Kitob
- `saved_at` - Saqlangan vaqt

### Announcement
- `title` - Sarlavha
- `body` - Matn
- `color` - Rang
- `date` - Sana

### Journal
- `name` - Nomi
- `cover_color` - Cover rangi
- `year` - Yil
- `issues_count` - Sonlar soni

## URL lar

### Asosiy sahifalar
- `/` - Bosh sahifa
- `/books/` - Kitoblar ro'yxati
- `/books/<id>/` - Kitob tafsilotlari
- `/saved/` - Saqlangan kitoblar
- `/history/` - O'qish tarixi
- `/search/` - AJAX qidiruv

### Autentifikatsiya
- `/accounts/login/` - Kirish
- `/accounts/logout/` - Chiqish

### Admin
- `/admin/` - Django admin paneli

## Texnologiyalar

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5.3.0, Font Awesome 6.4.0
- **Database**: SQLite (development)
- **File Storage**: Django file system

## Rivojlantirish

### Yangi kategoriya qo'shish
```python
# Django admin orqali yoki
from library.models import Category
Category.objects.create(name="Dasturlash", emoji="💻", color="#007bff", slug="dasturlash")
```

### Yangi kitob qo'shish
```python
from library.models import Book, Category
category = Category.objects.get(slug="dasturlash")
Book.objects.create(
    title="Python dasturlash",
    author="John Doe",
    description="Python haqida to'liq kitob",
    category=category,
    cover_color="#28a745",
    file="books/python.pdf"
)
```

## Litsenziya

© 2026 KIUF E-Lib. Barcha huquqlar himoyalangan.
