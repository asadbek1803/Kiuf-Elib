from django.contrib import admin
from django.http import HttpResponse
import csv
import xlsxwriter
from io import BytesIO
from unfold.admin import ModelAdmin
from .models import Book, Category, ReadingHistory, SavedBook, Announcement, Journal


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'emoji', 'color', 'book_count']
    list_filter = ['color']
    search_fields = ['name']
    ordering = ['name']




@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ['title', 'author', 'cover_image', 'category', 'badge', 'read_count', 'download_count', 'rating', 'is_published', 'created_at']
    list_filter = ['category', 'badge', 'is_published', 'is_available', 'created_at']
    search_fields = ['title', 'author', 'description']
    list_editable = ['is_published']
    ordering = ['-created_at']
    readonly_fields = ['read_count', 'download_count']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'author', 'description', 'category', 'cover_color', 'cover_image')
        }),
        ('Media fayllar', {
            'fields': ('file',)
        }),
        ('Statistika', {
            'fields': ('read_count', 'download_count', 'rating', 'badge')
        }),
        ('Nashr', {
            'fields': ('is_published', 'is_available')
        }),
    )
    
    actions = ['export_to_excel', 'export_to_csv']
    
    def export_to_excel(self, request, queryset):
        """Kitoblarni Excel ga eksport qilish"""
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Header
        headers = ['Nomi', 'Muallifi', 'Kategoriyasi', 'Reytingi', 'O\'qilganlar', 'Yuklab olingan', 'Yaratilgan sana']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        
        # Data
        for row, book in enumerate(queryset, 1):
            worksheet.write(row, 0, book.title)
            worksheet.write(row, 1, book.author)
            worksheet.write(row, 2, book.category.name if book.category else '')
            worksheet.write(row, 3, book.rating)
            worksheet.write(row, 4, book.read_count)
            worksheet.write(row, 5, book.download_count)
            worksheet.write(row, 6, book.created_at.strftime('%d.%m.%Y'))
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=kitoblar.xlsx'
        return response
    
    export_to_excel.short_description = 'Excel ga eksport qilish'
    
    def export_to_csv(self, request, queryset):
        """Kitoblarni CSV ga eksport qilish"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=kitoblar.csv'
        
        writer = csv.writer(response)
        headers = ['Nomi', 'Muallifi', 'Kategoriyasi', 'Reytingi', 'O\'qilganlar', 'Yuklab olingan', 'Yaratilgan sana']
        writer.writerow(headers)
        
        for book in queryset:
            writer.writerow([
                book.title,
                book.author,
                book.category.name if book.category else '',
                book.rating,
                book.read_count,
                book.download_count,
                book.created_at.strftime('%d.%m.%Y')
            ])
        
        return response
    
    export_to_csv.short_description = 'CSV ga eksport qilish'


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(ModelAdmin):
    list_display = ['student', 'book', 'last_read']
    list_filter = ['last_read']
    search_fields = ['student__full_name', 'student__hemis_id', 'book__title']
    ordering = ['-last_read']
    raw_id_fields = ['student', 'book']


@admin.register(SavedBook)
class SavedBookAdmin(ModelAdmin):
    list_display = ['student', 'book', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['student__full_name', 'student__hemis_id', 'book__title']
    ordering = ['-saved_at']
    raw_id_fields = ['student', 'book']


@admin.register(Announcement)
class AnnouncementAdmin(ModelAdmin):
    list_display = ['title', 'color', 'date']
    list_filter = ['date', 'color']
    search_fields = ['title', 'body']
    ordering = ['-date']
    readonly_fields = ['date']


@admin.register(Journal)
class JournalAdmin(ModelAdmin):
    list_display = ['name', 'year', 'issues_count']
    list_filter = ['year']
    search_fields = ['name']
    ordering = ['-year', 'name']
    list_editable = ['issues_count']






