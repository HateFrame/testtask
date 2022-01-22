from django.urls import path, include
from .views import RegisterView


urlpatterns = [
    path('clients/create/', RegisterView.as_view(), name='register')
]
