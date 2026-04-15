from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q, Count
from django.contrib import messages
from .models import Book, Category, ReadingHistory, SavedBook, Announcement, Journal


@login_required
def home(request):
    """Bosh sahifa"""
    # Statistika
    total_books = Book.objects.filter(is_published=True).count()
    total_students = Book.objects.values('reading_history__student').distinct().count()
    total_downloads = Book.objects.aggregate(total=models.Sum('download_count'))['total'] or 0
    total_categories = Category.objects.count()

    # Kategoriyalar
    categories = Category.objects.all()[:8]

    # Yangi kitoblar
    new_books = Book.objects.filter(is_published=True).order_by('-created_at')[:6]

    # Mashhur kitoblar
    popular_books = Book.objects.filter(is_published=True).order_by('-read_count')[:6]

    # E'lonlar
    announcements = Announcement.objects.all()[:3]

    context = {
        'total_books': total_books,
        'total_students': total_students,
        'total_downloads': total_downloads,
        'total_categories': total_categories,
        'categories': categories,
        'new_books': new_books,
        'popular_books': popular_books,
        'announcements': announcements,
    }
    return render(request, 'library/index.html', context)


@login_required
def books_list(request):
    """Kitoblar ro'yxati"""
    books = Book.objects.filter(is_published=True)
    
    # Filter
    category_id = request.GET.get('category')
    search = request.GET.get('search')
    
    if category_id:
        books = books.filter(category_id=category_id)
    
    if search:
        books = books.filter(
            Q(title__icontains=search) | 
            Q(author__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Sahifalash
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    # Jami kitoblar soni
    total_books = books.count()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_id,
        'search_query': search or '',
        'total_books': total_books,
    }
    return render(request, 'library/books.html', context)


@login_required
def book_detail(request, pk):
    """Kitob tafsilotlari"""
    book = get_object_or_404(Book, pk=pk, is_published=True)
    
    # O'qish sonini oshirish
    book.read_count += 1
    book.save(update_fields=['read_count'])
    
    # O'qish tarixini qo'shish
    ReadingHistory.objects.get_or_create(
        student=request.user,
        book=book,
        defaults={'progress': 0, 'last_page': 0}
    )
    
    # Saqlanganligini tekshirish
    is_saved = SavedBook.objects.filter(student=request.user, book=book).exists()
    
    context = {
        'book': book,
        'is_saved': is_saved,
    }
    return render(request, 'library/book_detail.html', context)


@login_required
def save_book(request, pk):
    """Kitobni saqlash"""
    book = get_object_or_404(Book, pk=pk, is_published=True)
    
    saved_book, created = SavedBook.objects.get_or_create(
        student=request.user,
        book=book
    )
    
    if created:
        messages.success(request, f"'{book.title}' saqlanganlar ro'yxatiga qo'shildi.")
    else:
        messages.info(request, f"'{book.title}' allaqachon saqlangan.")
    
    return redirect('library:book_detail', pk=pk)


@login_required
def unsave_book(request, pk):
    """Kitobni saqlashdan o'chirish"""
    book = get_object_or_404(Book, pk=pk, is_published=True)
    
    try:
        saved_book = SavedBook.objects.get(student=request.user, book=book)
        saved_book.delete()
        messages.success(request, f"'{book.title}' saqlanganlar ro'yxatidan olib tashlandi.")
    except SavedBook.DoesNotExist:
        messages.error(request, "Bu kitob saqlanganlar ro'yxatida topilmadi.")
    
    return redirect('library:book_detail', pk=pk)


@login_required
def saved_books(request):
    """Saqlangan kitoblar"""
    saved_books = SavedBook.objects.filter(student=request.user).select_related('book')
    
    # Sahifalash
    paginator = Paginator(saved_books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'library/saved_books.html', context)


@login_required
def reading_history(request):
    """O'qish tarixi"""
    history = ReadingHistory.objects.filter(student=request.user).select_related('book')
    
    # Sahifalash
    paginator = Paginator(history, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'library/reading_history.html', context)


@login_required
def search(request):
    """Qidiruv"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    books = Book.objects.filter(
        is_published=True
    ).filter(
        Q(title__icontains=query) | 
        Q(author__icontains=query)
    )[:10]
    
    results = []
    for book in books:
        results.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'url': book.get_absolute_url(),
            'cover_color': book.cover_color,
            'badge': book.badge,
        })
    
    return JsonResponse({'results': results})


@login_required
def download_book(request, pk):
    """Kitobni yuklab olish"""
    book = get_object_or_404(Book, pk=pk, is_published=True)
    
    # Yuklab olish sonini oshirish
    book.download_count += 1
    book.save(update_fields=['download_count'])
    
    # O'qish tarixini qo'shish
    ReadingHistory.objects.get_or_create(
        student=request.user,
        book=book,
        defaults={'progress': 0, 'last_page': 0}
    )
    
    # Faylni yuklab berish
    if book.file:
        response = HttpResponse(book.file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
        return response
    else:
        messages.error(request, "Kitob fayli topilmadi.")
        return redirect('library:book_detail', pk=pk)


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_help(request):
    """Admin panel yordami"""
    help_content = {
        'Talabalar': {
            'icon': '👥',
            'description': 'Talabalar bo\'limi orqali tizimga kiradigan foydalanuvchilarni boshqarish mumkin. Yangi talaba qo\'shish, tahrirlash, o\'chirish va Excel/CSV formatida eksport qilish mumkin.',
            'features': [
                'Yangi talaba qo\'shish',
                'Talabani tahrirlash',
                'Talabani o\'chirish',
                'Export qilish (Excel/CSV)',
                'Qidiruv (HEMIS ID, ism, fakultet)'
            ]
        },
        'Kategoriyalar': {
            'icon': '📚',
            'description': 'Kategoriyalar bo\'limi orqali kitoblarni guruhlash mumkin. Yangi kategoriya qo\'shish, tahrirlash, o\'chirish va rang tanlash mumkin.',
            'features': [
                'Yangi kategoriya qo\'shish',
                'Kategoriyani tahrirlash',
                'Kategoriyani o\'chirish',
                'Kitoblar soni ko\'rish',
                'Rang tanlash'
            ]
        },
        'Kitoblar': {
            'icon': '📖',
            'description': 'Kitoblar bo\'limi orqali elektron kitoblarni boshqarish mumkin. Yangi kitob qo\'shish, PDF yuklash, nashr qilish va belgi qo\'shish mumkin.',
            'features': [
                'Yangi kitob qo\'shish',
                'Kitobni tahrirlash',
                'Kitobni o\'chirish',
                'PDF yuklash',
                'Nashr qilish',
                'Belgi qo\'shish (NEW/HOT)',
                'Reyting o\'zgartirish'
            ]
        },
        'O\'qish tarixi': {
            'icon': '📝',
            'description': 'O\'qish tarixi bo\'limi orqali talabalarning kitob o\'qish tarixini ko\'rish mumkin. Progress va oxirgi sahifa ma\'lumotlari ko\'rsatiladi.',
            'features': [
                'Qidiruv (talaba ismi, kitob nomi)',
                'Filter (o\'qish vaqti)',
                'Progress ko\'rish',
                'Oxirgi sahifa ko\'rish'
            ]
        },
        'Saqlangan kitoblar': {
            'icon': '❤️',
            'description': 'Saqlangan kitoblar bo\'limi orqali talabalar tomonidan saqlangan kitoblarni ko\'rish mumkin.',
            'features': [
                'Qidiruv (talaba ismi, kitob nomi)',
                'Filter (saqlash vaqti)',
                'Talaba va kitob ma\'lumotlari'
            ]
        },
        'E\'lonlar': {
            'icon': '📢',
            'description': 'E\'lonlar bo\'limi orqali tizimda e\'lonlar joylashtirish mumkin. E\'lonlar bosh sahifada ko\'rsatiladi.',
            'features': [
                'Yangi e\'lon qo\'shish',
                'E\'lonni tahrirlash',
                'E\'lonni o\'chirish',
                'Rang tanlash',
                'Sana belgilash'
            ]
        },
        'Jurnallar': {
            'icon': '📰',
            'description': 'Jurnallar bo\'limi orqali ilmiy jurnallarni boshqarish mumkin. Jurnallar kutubxona katalogida ko\'rsatiladi.',
            'features': [
                'Yangi jurnal qo\'shish',
                'Jurnalni tahrirlash',
                'Jurnalni o\'chirish',
                'Sonlar soni',
                'Yil belgilash'
            ]
        }
    }
    
    return render(request, 'library/admin_help.html', {'help_content': help_content})
