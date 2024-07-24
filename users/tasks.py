from datetime import datetime, timedelta

import pytz
from celery import shared_task
from celery.utils.time import timezone
from dateutil.relativedelta import relativedelta
from django.conf import settings

from users.models import User


@shared_task
def check_last_login():
    """Blocks the user if he has not logged in for more than 1 month"""
    now = timezone.now()
    inactive = now - relativedelta(months=1)
    users = User.objects.filter(last_login__lte=inactive)
    for user in users:
        user.is_active = False
        user.save()
