from celery import shared_task
from celery.utils.time import timezone
from dateutil.relativedelta import relativedelta

from users.models import User


@shared_task
def check_last_login():
    users = User.objects.all()
    date_now = timezone.now()
    for user in users:
        if user.last_login < (date_now - relativedelta(months=1)):
            user.is_active = False
            user.save()
        else:
            user.last_login = date_now
            user.save()