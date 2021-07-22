from django.urls import path
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt import views as jwt_views
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('registration/', views.Registration.as_view(), name='registration'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('edit/', views.EditPeriod.as_view(), name='edit'),
    path('search/', views.Search.as_view(), name='search'),
    path('api/profile/', views.ProfileAPI.as_view(), name='api_profile'),
    path('api/weather/<city>/', views.SearchAPI.as_view(), name='api_search'),
    path('follow/<city>/', views.FollowCity.as_view(),
         name='follow'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
]
