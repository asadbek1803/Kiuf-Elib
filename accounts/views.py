from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            hemis_id = form.cleaned_data['hemis_id']
            birth_date = form.cleaned_data['birth_date']

            # Custom authentication with hemis_id and birth_date
            from django.contrib.auth import authenticate
            user = authenticate(request, hemis_id=hemis_id, birth_date=birth_date)

            if user is not None:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.full_name}!")
                return redirect('library:home')
            else:
                # HEMIS ID bo'yicha user ni topish
                from .models import Student
                try:
                    student = Student.objects.get(hemis_id=hemis_id)
                    if student.birth_date is None:
                        messages.warning(request, "⚠️ Sizning ma'lumotlaringizda tug'ilgan kuni yo'q. Iltimos, Kutubxona administratsiyasi bilan bog'lanib ma'lumotlaringizni to'ldiring.")
                    else:
                        messages.error(request, "HEMIS ID yoki tug'ilgan kun noto'g'ri. Iltimos, tekshirib qayta kiriting.")
                except Student.DoesNotExist:
                    messages.error(request, "HEMIS ID topilmadi. Iltimos, tekshirib qayta kiriting.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('accounts:login')
