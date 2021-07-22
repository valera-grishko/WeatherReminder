import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.views.generic.edit import FormView
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .forms import RegistrationForm, LoginForm, SearchForm, PeriodForm
from .service import periodic_task_create, cities_weather, create_button
from .models import Follow


class Registration(FormView):
    template_name = "main/registration.html"
    form_class = RegistrationForm

    def form_valid(self, form):
        new_user, password = form.save()
        response = requests.post(settings.URL_FOR_TOKEN,
                                 data={'username': new_user.username,
                                       'password': password}).json()
        login(self.request, new_user)
        periodic_task_create(new_user.username, new_user.period)
        return redirect(reverse('profile'), headers={
            'Authorization': 'Bearer ' + response['access']})


class Login(FormView):
    template_name = "main/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user, password = form.sign_in()
        response = requests.post(settings.URL_FOR_TOKEN,
                                 data={'username': user.username,
                                       'password': password}).json()
        login(self.request, user)
        return redirect(reverse('profile'), headers={
            'Authorization': 'Bearer ' + response['access']})


class Profile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_info = []
        for city in Follow.objects.filter(user=request.user):
            all_info.append(cities_weather(city.city))
        context = {'username': request.user.username, 'info': all_info[::-1]}
        return render(request, "main/profile.html", context=context)


class ProfileAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_info = []
        for city in Follow.objects.filter(user=request.user):
            all_info.append(cities_weather(city.city))
        context = {'info': all_info[::-1]}
        return Response(context)


class EditPeriod(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        context = {'form': PeriodForm}
        return render(request, "main/edit_period.html", context=context)

    def post(self, request):
        form = PeriodForm(request.POST)
        if form.is_valid():
            user = form.edit(request.user.id)
            task = PeriodicTask.objects.get(name=user.username)
            if user.notifications:
                task.enabled = True
                schedule, created = IntervalSchedule.objects.get_or_create(
                    every=user.period.seconds,
                    period=IntervalSchedule.SECONDS
                )
                task.interval = schedule
            else:
                task.enabled = False
            task.save()
        return redirect("profile")


class SearchAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, city):
        response = requests.get(settings.APP_URL.format(city)).json()
        context = {'info': response}
        return Response(context)


class Search(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        context = {'form': SearchForm}
        return render(request, "main/city_search.html", context=context)

    def post(self, request):
        form = SearchForm(request.POST)
        context = {'info': None}
        if form.is_valid():
            city = form.cleaned_data['city']
            follow_button = create_button(request.user, city)
            context = {'info': cities_weather(city), 'follow': follow_button}
        return render(request, "main/weather.html", context=context)


class FollowCity(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, city):
        user = request.user
        if Follow.objects.filter(user=user, city=city):
            Follow.objects.get(user=user, city=city).delete()
        else:
            new_follow = Follow(user=user, city=city)
            new_follow.save()
        return redirect("profile")
