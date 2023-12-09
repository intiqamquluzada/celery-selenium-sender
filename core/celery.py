from __future__ import absolute_import, unicode_literals
from datetime import timedelta
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'run-every-10-minutes': {
        'task': 'currency.tasks.get_currency',
        'schedule': timedelta(minutes=2),
    },
}

app.autodiscover_tasks()