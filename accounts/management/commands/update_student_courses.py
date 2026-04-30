from django.core.management.base import BaseCommand
from accounts.models import Student


class Command(BaseCommand):
    help = "Har yili sentyabr 1-kunida talabalarning kursini 1 ga oshiradi va agar 4 kursdan oshsa is_active=False qiladi. Adminlar (year=null) o'tkazib yuboriladi."

    def handle(self, *args, **options):
        # Faqat year fieldi null bo'lmagan talabalarni olish (adminlar emas)
        students = Student.objects.filter(year__isnull=False)
        updated = 0
        deactivated = 0
        skipped = 0

        for student in students:
            student.year += 1
            if student.year > 4:
                student.is_active = False
                deactivated += 1
            student.save()
            updated += 1

        # Null year bo'lgan foydalanuvchilar (adminlar)
        skipped = Student.objects.filter(year__isnull=True).count()

        self.stdout.write(
            self.style.SUCCESS(
                f'{updated} talaba kursi yangilandi, {deactivated} talaba akkaunti muzlatildi, {skipped} admin o\'tkazib yuborildi.'
            )
        )