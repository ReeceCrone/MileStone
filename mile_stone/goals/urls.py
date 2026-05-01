from django.urls import path
from .views import main,  dayGoals, weekGoals,  monthGoals,delete_goal

urlpatterns = [
    path('', main, name='main'),
    path('daygoals/', dayGoals, name='daygoals'),
    path('weekgoals/', weekGoals, name='weekgoals'),
    path('monthgoals/', monthGoals, name='monthgoals'),
    path("api/delete-goal/", delete_goal, name="delete_goal"),
]