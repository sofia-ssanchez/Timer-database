# URL file tells the app which view to run 

from django.urls import path
from . import views  # Import your views module

urlpatterns = [
    path('register/', views.register_users, name='register_user'),  # Correct pattern
]
