import json
import requests
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .models import Follow


def periodic_task_create(username, period):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=period.seconds,
        period=IntervalSchedule.SECONDS
    )
    task = PeriodicTask.objects.create(
        interval=schedule,
        name=username,
        task='send_weather',
        args=json.dumps([username]),
        start_time=timezone.now()
    )
    task.save()


def send(info, email):
    send_mail(
        'Regular weather information',
        info,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def cities_weather(city):
    response = requests.get(settings.APP_URL.format(city)).json()
    info = {
        'city': city,
        'country': response["sys"]["country"],
        'temp': response["main"]["temp"],
        'icon': response["weather"][0]["icon"]
    }
    return info


def create_button(user, city):
    return "Unfollow" if Follow.objects.filter(user=user,
                                               city=city) else "Follow"
