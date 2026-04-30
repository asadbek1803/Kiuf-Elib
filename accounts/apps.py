from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.contrib import admin
        from .forms import CustomAdminLoginForm
        admin.site.login_form = CustomAdminLoginForm

        # Scheduler setup - har yil 1-sentyabr kuni talabalarning kursini 1 ga oshiradi
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from django_apscheduler.jobstores import DjangoJobStore
        from django.core.management import call_command
        import logging

        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.WARNING)

        try:
            scheduler = BackgroundScheduler()
            scheduler.add_jobstore(DjangoJobStore(), 'default')

            # Har yil 1-sentyabr kuni soat 00:00 da ishlaydi
            scheduler.add_job(
                call_command,
                trigger=CronTrigger(day=1, month=9, hour=0, minute=0),
                args=['update_student_courses'],
                id='update_student_courses',
                max_instances=1,
                replace_existing=True,
            )

            # Eski job executionlarni tozalash (har 10 daqiqada)
            scheduler.add_job(
                'accounts.scheduler_jobs:delete_old_job_executions',
                trigger=CronTrigger(minute='*/10'),
                id='delete_old_job_executions',
                max_instances=1,
                replace_existing=True,
            )

            scheduler.start()
        except Exception as e:
            print(f"Scheduler setup error: {e}")
