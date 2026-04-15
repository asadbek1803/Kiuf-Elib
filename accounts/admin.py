from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse
from django.contrib import messages
from django.shortcuts import render
import csv
import xlsxwriter
import openpyxl
from io import BytesIO, TextIOWrapper
from unfold.admin import ModelAdmin
from unfold.decorators import action as unfold_action   # ← QO'SHILDI
from .models import Student


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    change_list_template = 'admin/accounts/student/change_list.html'
    list_display = ('hemis_id', 'full_name', 'faculty', 'specialty', 'year', 'is_active', 'date_joined')
    list_filter = ('is_active', 'faculty', 'year')
    search_fields = ('hemis_id', 'full_name', 'faculty', 'specialty')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')

    # actions_list — Unfold tugmalari (unfold_action kerak)
    # actions      — oddiy Django dropdown (admin.action kerak)
    actions_list = ['export_to_excel', 'export_to_csv']
    actions = ['export_to_excel', 'export_to_csv']

    fieldsets = (
        (None, {'fields': ('hemis_id',)}),
        ('Personal info', {'fields': ('full_name', 'faculty', 'specialty', 'year')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import/', self.admin_site.admin_view(self.import_view), name='accounts_student_import'),
            path('import/template/', self.admin_site.admin_view(self.download_template), name='accounts_student_template'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['import_url'] = reverse('admin:accounts_student_import')
        return super().changelist_view(request, extra_context=extra_context)

    def import_view(self, request):
        if request.method == 'POST':
            file = request.FILES.get('import_file')
            if not file:
                messages.error(request, "Fayl tanlanmadi!")
                return HttpResponseRedirect(request.path)

            filename = file.name.lower()
            try:
                if filename.endswith('.xlsx') or filename.endswith('.xls'):
                    created, updated, errors = self._import_from_excel(file)
                elif filename.endswith('.csv'):
                    created, updated, errors = self._import_from_csv(file)
                else:
                    messages.error(request, "Faqat .xlsx yoki .csv fayl qabul qilinadi!")
                    return HttpResponseRedirect(request.path)

                if created:
                    messages.success(request, f"✅ {created} ta yangi talaba qo'shildi.")
                if updated:
                    messages.warning(request, f"🔄 {updated} ta talaba yangilandi.")
                if errors:
                    for err in errors[:10]:
                        messages.error(request, err)

            except Exception as e:
                messages.error(request, f"Xato yuz berdi: {str(e)}")

            return HttpResponseRedirect(reverse('admin:accounts_student_changelist'))

        context = {
            **self.admin_site.each_context(request),
            'title': "Talabalarni import qilish",
            'template_url': reverse('admin:accounts_student_template'),
            'opts': self.model._meta,
        }
        return render(request, 'admin/accounts/student/import.html', context)

    def _import_from_excel(self, file):
        wb = openpyxl.load_workbook(file)
        ws = wb.active
        return self._process_rows(list(ws.iter_rows(min_row=2, values_only=True)))

    def _import_from_csv(self, file):
        decoded = TextIOWrapper(file, encoding='utf-8-sig')
        reader = csv.reader(decoded)
        next(reader, None)
        return self._process_rows(list(reader))

    def _process_rows(self, rows):
        created = updated = 0
        errors = []

        for i, row in enumerate(rows, start=2):
            try:
                if not any(row):
                    continue

                hemis_id  = str(row[0]).strip() if row[0] else None
                full_name = str(row[1]).strip() if len(row) > 1 and row[1] else ''
                faculty   = str(row[2]).strip() if len(row) > 2 and row[2] else ''
                specialty = str(row[3]).strip() if len(row) > 3 and row[3] else ''
                year      = int(row[4]) if len(row) > 4 and row[4] else 1
                is_active = str(row[5]).strip().lower() in ('ha', 'true', '1', 'yes') if len(row) > 5 and row[5] else True

                if not hemis_id:
                    errors.append(f"Qator {i}: HEMIS ID bo'sh!")
                    continue

                student, is_new = Student.objects.get_or_create(
                    hemis_id=hemis_id,
                    defaults={
                        'full_name': full_name,
                        'faculty': faculty,
                        'specialty': specialty,
                        'year': year,
                        'is_active': is_active,
                    }
                )

                if is_new:
                    student.set_unusable_password()
                    student.save()
                    created += 1
                else:
                    student.full_name = full_name
                    student.faculty = faculty
                    student.specialty = specialty
                    student.year = year
                    student.is_active = is_active
                    student.save()
                    updated += 1

            except Exception as e:
                errors.append(f"Qator {i}: {str(e)}")

        return created, updated, errors

    def download_template(self, request):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Talabalar')

        header_fmt = workbook.add_format({
            'bold': True, 'bg_color': '#4472C4', 'font_color': 'white',
            'border': 1, 'align': 'center', 'valign': 'vcenter'
        })
        example_fmt = workbook.add_format({'bg_color': '#EBF3FB', 'border': 1})
        note_fmt = workbook.add_format({'italic': True, 'font_color': '#888888'})

        headers = ["HEMIS ID", "To'liq ism", "Fakultet", "Mutaxassislik", "Kurs", "Faol (Ha/Yo'q)"]
        for col, h in enumerate(headers):
            worksheet.write(0, col, h, header_fmt)

        examples = [
            ['2024001', 'Ali Valiyev', 'IT', 'Software Engineering', 2, 'Ha'],
            ['2024002', 'Malika Yusupova', 'Iqtisodiyot', 'Moliya', 1, 'Ha'],
            ['2024003', 'Jasur Toshmatov', 'Huquq', 'Xalqaro huquq', 3, "Yo'q"],
        ]
        for row, data in enumerate(examples, 1):
            for col, val in enumerate(data):
                worksheet.write(row, col, val, example_fmt)

        worksheet.write(5, 0, "* 1-qator sarlavha, o'zgartirmang. Faqat ma'lumot qo'shing.", note_fmt)
        worksheet.set_column(0, 0, 12)
        worksheet.set_column(1, 1, 22)
        worksheet.set_column(2, 3, 20)
        worksheet.set_column(4, 4, 8)
        worksheet.set_column(5, 5, 15)
        worksheet.set_row(0, 22)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=talabalar_shablon.xlsx'
        return response

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_unusable_password()
        super().save_model(request, obj, form, change)

    # ↓↓↓ actions_list uchun @unfold_action — bu muhim! ↓↓↓
    @unfold_action(description="Excel ga eksport qilish")
    def export_to_excel(self, request, queryset=None):
        if queryset is None or not queryset.exists():
            queryset = Student.objects.all()

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True, 'bg_color': '#4472C4', 'font_color': 'white'})
        headers = ["HEMIS ID", "To'liq ism", "Fakultet", "Mutaxassislik", "Kurs", "Faol", "Ro'yxatga olingan"]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold)

        for row, student in enumerate(queryset, 1):
            worksheet.write(row, 0, student.hemis_id)
            worksheet.write(row, 1, student.full_name)
            worksheet.write(row, 2, student.faculty)
            worksheet.write(row, 3, student.specialty)
            worksheet.write(row, 4, student.year)
            worksheet.write(row, 5, "Ha" if student.is_active else "Yo'q")
            worksheet.write(row, 6, student.date_joined.strftime('%d.%m.%Y'))

        worksheet.set_column(0, 0, 15)
        worksheet.set_column(1, 1, 25)
        worksheet.set_column(2, 3, 20)
        worksheet.set_column(4, 6, 15)
        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=talabalar.xlsx'
        return response

    @unfold_action(description="CSV ga eksport qilish")
    def export_to_csv(self, request, queryset=None):
        if queryset is None or not queryset.exists():
            queryset = Student.objects.all()

        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename=talabalar.csv'
        writer = csv.writer(response)
        writer.writerow(["HEMIS ID", "To'liq ism", "Fakultet", "Mutaxassislik", "Kurs", "Faol", "Ro'yxatga olingan"])

        for student in queryset:
            writer.writerow([
                student.hemis_id, student.full_name, student.faculty,
                student.specialty, student.year,
                "Ha" if student.is_active else "Yo'q",
                student.date_joined.strftime('%d.%m.%Y'),
            ])
        return response