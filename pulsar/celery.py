from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pulsar.settings")


app = Celery("pulsar")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
