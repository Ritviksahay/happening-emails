from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Connection
import ssl

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emailworker.settings')



app = Celery('emailworker')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()
broker_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE  # or ssl.CERT_OPTIONAL / ssl.CERT_REQUIRED
}

app.conf.broker_transport_options = {"visibility_timeout": 3600}  # Optional
app.conf.broker_use_ssl = broker_use_ssl
