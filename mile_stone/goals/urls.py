from django.urls import path
from .views import main,  dayGoals, weekGoals

urlpatterns = [
    path('', main, name='main'),
    path('daygoals/', dayGoals, name='daygoals'),
    path('weekgoals/', weekGoals, name='weekgoals')
]