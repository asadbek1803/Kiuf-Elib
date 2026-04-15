from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    emoji = models.CharField(max_length=10, blank=True, verbose_name="Emoji")
    color = models.CharField(max_length=7, default="#007bff", verbose_name="Rang")
    slug = models.SlugField(unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def book_count(self):
        return self.books.filter(is_published=True).count()


class Book(models.Model):
    BADGE_CHOICES = [
        ('new', 'NEW'),
        ('hot', 'HOT'),
        ('free', 'FREE'),
        ('pdf', 'PDF'),
    ]

    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    author = models.CharField(max_length=100, verbose_name="Muallif")
    description = models.TextField(verbose_name="Tavsif")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', verbose_name="Kategoriya")
    cover_color = models.CharField(max_length=7, default="#28a745", verbose_name="Cover rangi")
    file = models.FileField(upload_to='books/', verbose_name="PDF fayl")
    badge = models.CharField(max_length=10, choices=BADGE_CHOICES, blank=True, verbose_name="Belgi")
    rating = models.FloatField(default=0.0, verbose_name="Reyting")
    read_count = models.IntegerField(default=0, verbose_name="O'qilganlar soni")
    download_count = models.IntegerField(default=0, verbose_name="Yuklab olishlar soni")
    is_published = models.BooleanField(default=True, verbose_name="Nashr qilingan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.author}"

    def get_absolute_url(self):
        return reverse('library:book_detail', kwargs={'pk': self.pk})


class ReadingHistory(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_history')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_history')
    progress = models.IntegerField(default=0, verbose_name="Progress (%)")
    last_page = models.IntegerField(default=1, verbose_name="Oxirgi sahifa")
    last_read = models.DateTimeField(auto_now=True, verbose_name="Oxirgi o'qilgan vaqt")

    class Meta:
        verbose_name = "O'qish tarixi"
        verbose_name_plural = "O'qish tarixlari"
        unique_together = ['student', 'book']
        ordering = ['-last_read']

    def __str__(self):
        return f"{self.student.full_name} - {self.book.title}"


class SavedBook(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True, verbose_name="Saqlangan vaqt")

    class Meta:
        verbose_name = "Saqlangan kitob"
        verbose_name_plural = "Saqlangan kitoblar"
        unique_together = ['student', 'book']
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.student.full_name} - {self.book.title}"


class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    body = models.TextField(verbose_name="Matn")
    color = models.CharField(max_length=7, default="#17a2b8", verbose_name="Rang")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    class Meta:
        verbose_name = "E'lon"
        verbose_name_plural = "E'lonlar"
        ordering = ['-date']

    def __str__(self):
        return self.title


class Journal(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    cover_color = models.CharField(max_length=7, default="#6c757d", verbose_name="Cover rangi")
    year = models.IntegerField(verbose_name="Yil")
    issues_count = models.IntegerField(default=0, verbose_name="Sonlar soni")

    class Meta:
        verbose_name = "Jurnal"
        verbose_name_plural = "Jurnallar"
        ordering = ['-year', 'name']

    def __str__(self):
        return f"{self.name} ({self.year})"
