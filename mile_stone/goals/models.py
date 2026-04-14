from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    LONG_TERM = 'long'

    GOAL_TYPES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (LONG_TERM, 'Long Term'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    goal_type = models.CharField(max_length=10, choices=GOAL_TYPES)

    target_value = models.IntegerField(default=1)  # e.g. 5 workouts/week
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
