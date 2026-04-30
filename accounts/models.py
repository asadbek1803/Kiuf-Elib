from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class StudentManager(BaseUserManager):
    def create_user(self, hemis_id, full_name, faculty, year, password=None, **extra_fields):
        if not hemis_id:
            raise ValueError('HEMIS ID kiritilishi shart')
        
        user = self.model(
            hemis_id=hemis_id,
            full_name=full_name,
            faculty=faculty,
            year=year,
            **extra_fields
        )
        
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, hemis_id, full_name, faculty, year, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is_staff=True bo\'lishi kerak')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser is_superuser=True bo\'lishi kerak')
        
        return self.create_user(
            hemis_id=hemis_id,
            full_name=full_name,
            faculty=faculty,
            year=year,
            password=password,
            **extra_fields
        )


class Student(AbstractUser):
    username = None  # Remove username field
    hemis_id = models.CharField(max_length=20, unique=True, verbose_name="HEMIS ID")
    full_name = models.CharField(max_length=100, verbose_name="To'liq ism")
    faculty = models.CharField(max_length=100, verbose_name="Fakultet")
    year = models.IntegerField(null=True, blank=True, verbose_name="Kurs")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan kun")
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = StudentManager()

    USERNAME_FIELD = 'hemis_id'
    REQUIRED_FIELDS = ['full_name', 'faculty']

    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"

    def __str__(self):
        return f"{self.full_name} ({self.hemis_id})"
