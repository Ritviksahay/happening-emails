from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Connection
import ssl
import logging
from celery.signals import task_failure
from celery.signals import task_prerun, task_success, task_failure

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emailworker.settings')



app = Celery('emailworker')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()
broker_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE  # or ssl.CERT_OPTIONAL / ssl.CERT_REQUIRED
}

app.conf.broker_transport_options = {"visibility_timeout": 3600}  # Optional
app.conf.broker_use_ssl = broker_use_ssl


@task_prerun.connect
def log_task_start(sender=None, task_id=None, task=None, **kwargs):
    logger.info(f"Celery task {task_id} started: {task.name}")

@task_success.connect
def log_task_success(sender=None, task_id=None, result=None, **kwargs):
    logger.info(f"Celery task {task_id} completed successfully with result: {result}")

@task_failure.connect
def log_task_failure(sender=None, task_id=None, exception=None, **kwargs):
    logger.error(f"Celery task {task_id} failed: {exception}")



