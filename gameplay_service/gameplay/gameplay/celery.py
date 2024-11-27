# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameplay.settings')

app = Celery('gameplay')

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_default_queue = 'gameplay_queue'

# Load tasks from all registered Django app configs.
app.autodiscover_tasks()
