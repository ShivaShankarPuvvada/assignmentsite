from .views import ConsumerCreate, ConsumerLogin, logout
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path("consumer/create", ConsumerCreate.as_view(), name="register"),
    path("",ConsumerLogin.as_view(),name="login"),
    path("logout/",logout,name="logout")
]