from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter
from userapi import views

router=DefaultRouter()

urlpatterns = [
    path("register/",views.CustomerCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    
]

