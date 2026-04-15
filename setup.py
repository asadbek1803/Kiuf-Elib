#!/usr/bin/env python
"""
KIUF Elektron Kutubxona - Setup Script
This script helps set up the project with sample data.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kiuf_elib.settings')
django.setup()

from accounts.models import Student
from library.models import Category, Book, Announcement


def create_sample_data():
    """Create sample data for testing"""
    
    print("🚀 Sample data yaratilmoqda...")
    
    # Create categories
    categories_data = [
        {'name': 'Dasturlash', 'emoji': '💻', 'color': '#007bff', 'slug': 'dasturlash'},
        {'name': 'Matematika', 'emoji': '🔢', 'color': '#28a745', 'slug': 'matematika'},
        {'name': 'Fizika', 'emoji': '⚛️', 'color': '#dc3545', 'slug': 'fizika'},
        {'name': 'Ingliz tili', 'emoji': '🇬🇧', 'color': '#17a2b8', 'slug': 'ingliz-tili'},
        {'name': 'Tarix', 'emoji': '📚', 'color': '#6c757d', 'slug': 'tarix'},
        {'name': 'Kimyo', 'emoji': '🧪', 'color': '#fd7e14', 'slug': 'kimyo'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f"✅ Kategoriya yaratildi: {category.name}")
    
    # Create sample students
    students_data = [
        {'hemis_id': '2024001', 'full_name': 'Ali Valiyev', 'faculty': 'IT', 'specialty': 'Software Engineering', 'year': 2},
        {'hemis_id': '2024002', 'full_name': 'Dilshoda Karimova', 'faculty': 'IT', 'specialty': 'Data Science', 'year': 3},
        {'hemis_id': '2024003', 'full_name': 'Javlon Toshmatov', 'faculty': 'Matematika', 'specialty': 'Applied Mathematics', 'year': 1},
        {'hemis_id': '2024004', 'full_name': 'Malika Axmedova', 'faculty': 'Fizika', 'specialty': 'Physics', 'year': 2},
    ]
    
    for student_data in students_data:
        student, created = Student.objects.get_or_create(
            hemis_id=student_data['hemis_id'],
            defaults=student_data
        )
        if created:
            print(f"✅ Talaba yaratildi: {student.full_name}")
    
    # Create sample announcements
    announcements_data = [
        {
            'title': 'Yangi kitoblar qo\'shildi!',
            'body': 'Kutubxonamizga dasturlash bo\'yicha 10 ta yangi kitob qo\'shildi. Barcha talabalarni tanovis qilamiz!',
            'color': '#28a745'
        },
        {
            'title': 'Kutubxona ish vaqti o\'zgartirildi',
            'body': 'Kutubxona endi 8:00 dan 18:00 gacha ishlaydi. Dam olish kunlari 9:00 dan 15:00 gacha.',
            'color': '#007bff'
        },
        {
            'title': 'Online kitob o\'qish xizmati',
            'body': 'Endi barcha kitoblarni onlayn o\'qishingiz mumkin. Faqat tizimga kiring va kitobni tanlang!',
            'color': '#17a2b8'
        },
    ]
    
    for ann_data in announcements_data:
        announcement, created = Announcement.objects.get_or_create(
            title=ann_data['title'],
            defaults=ann_data
        )
        if created:
            print(f"✅ E\'lon yaratildi: {announcement.title}")
    
    print("\n🎉 Sample data muvaffaqiyatli yaratildi!")
    print("\n📝 Kirish ma\'lumotlari:")
    print("Admin panel:")
    print("  URL: http://127.0.0.1:8000/admin/")
    print("  HEMIS ID: admin")
    print("  Parol: admin123")
    print("\nTalaba uchun:")
    print("  URL: http://127.0.0.1:8000/accounts/login/")
    print("  HEMIS ID: 2024001 (parol kerak emas)")
    print("  Yoki boshqa HEMIS ID: 2024002, 2024003, 2024004")


if __name__ == '__main__':
    create_sample_data()
