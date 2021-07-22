from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Follow


class ModelsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test1', password='qwerty')
        Follow.objects.create(user=user, city='test_city')

    def test_follow_city(self):
        follow = Follow.objects.get(id=1)
        max_length = follow._meta.get_field('city').max_length
        self.assertEquals(max_length, 40)
        self.assertEquals(follow.city, 'test_city')


class ViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test1', password='qwerty1',
                                        email='test1@gmail.com')
        Follow.objects.create(user=user, city='Kyiv')

    def test_registration(self):
        client = Client()
        response = client.get(reverse('registration'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "main/registration.html")

    def test_login(self):
        client = Client()
        response = client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "main/login.html")

    def test_profile(self):
        client = Client()
        client.login(username='test1', password='qwerty1')
        response = client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "main/profile.html")

    def test_api_profile(self):
        client = Client()
        client.login(username='test1', password='qwerty1')
        response = client.get(reverse('api_profile'))
        response_json = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_json["info"][0]["country"], "UA")
        self.assertEquals(response_json["info"][0]["city"], "Kyiv")

    def test_search_get(self):
        client = Client()
        client.login(username='test1', password='qwerty1')
        response = client.get(reverse('search'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "main/city_search.html")

    def test_search_post(self):
        client = Client()
        client.login(username='test1', password='qwerty1')
        response = client.post(reverse('search'), {'city': 'Kyiv'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "main/weather.html")

    def test_api_search(self):
        client = Client()
        client.login(username='test1', password='qwerty1')
        response = client.get('/api/weather/Kyiv/')
        response_json = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_json["info"]["sys"]["country"], "UA")
        self.assertEquals(response_json["info"]["name"], "Kyiv")

    def test_follow(self):
        client = Client()
        client.login(username='test1', password='qwerty1')
        user = User.objects.get(username='test1')
        self.assertEquals(
            Follow.objects.filter(user=user, city="London").exists(), False)
        response = client.post('/follow/London/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(
            Follow.objects.filter(user=user, city="London").exists(), True)
