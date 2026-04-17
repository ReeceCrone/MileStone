from django.urls import path
from .views import main,  dayGoals

urlpatterns = [
    path('', main, name='main'),
    path('daygoals/', dayGoals, name='daygoals')
]