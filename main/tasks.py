import requests
from django.conf import settings
from weather_remider.celery import app
from .models import User, Follow
from .service import send


@app.task(name='send_weather')
def send_weather(username):
    all_info = ""
    user = User.objects.get(username=username)
    follows = Follow.objects.filter(user=user)
    for follow in follows:
        response = requests.get(settings.APP_URL.format(follow.city)).json()
        all_info += "CITY: " + follow.city + "\n"
        all_info += "COUNTRY: " + response["sys"]["country"] + "\n"
        all_info += "TEMPERATURE: " + str(response["main"]["temp"]) + "\n\n\n"
    send(all_info, user.email)
    return
