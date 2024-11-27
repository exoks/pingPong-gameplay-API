from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchmaking_service.settings')

# Replace 'your_project' with your project's name.
app = Celery('matchmaking_service', broker='redis://localhost:6379/0')

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_default_queue = 'matchmaking_queue'

# Load tasks from all registered Django app configs.
app.autodiscover_tasks()
