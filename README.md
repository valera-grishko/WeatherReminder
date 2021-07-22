# WeatherReminder

The app allows you to track the weather in selected cities.  
Information about the weather in the selected cities will also be sent to the user's email.  
The user can change the period for sending messages (1 minute - for tests, 1 hour, 3 hour, 6 hour - default, 12 hour).  
The user can enable / disable sending messages.  

Tech stack: Python, Django, Django REST framework, PostgreSQL, Celery, Redis, HTML, CSS, Third-party weather API  

The application is deployed on heroku. Link: https://weatherreminder21.herokuapp.com/registration/  
Heroku resources: Heroku Postgres, Heroku Redis  
  
  
  
 --- Endpoints ---  

/api/weather/<city>/ ---> API containing information about the city's weather  
/api/profile/ ---> Profile data in API  
/api/token/ ---> get access and refresh  
  
/registration/ ---> new user registration  
/login/ ---> login  
/logout/ ---> logout  
/search/ ---> search city  
/profile/ ---> your profile  
/edit/ ---> edit period  
  
  
For localhosting comment second database and uncomment first database in weather_remider/settings.py  
  
run tests: python manage.py test  
