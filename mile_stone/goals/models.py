from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    DAY = 'day'
    WEEK = 'weekly'
    MONTH = 'monthly'
    LONG = 'long'

    FITNESS = 'fitness'
    ACADEMIC = 'academic'
    CAREER = 'career'
    LIFE = 'life'


    # denotes if a goal is to be completed that day, week, month, or over a longer period
    GOAL_PERIOD = [
        (DAY, 'Day'),
        (WEEK, 'Week'),
        (MONTH, 'Month'),
        (LONG, 'Long Term'),
    ]

    # describes the nature of the goal
    GOAL_TYPE = [
        (FITNESS, 'Fitness'),
        (ACADEMIC, 'Academic'),
        (CAREER, 'Career'),
        (LIFE, 'Life'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    goal_type = models.CharField(max_length=10, choices=GOAL_TYPE)
    goal_period = models.CharField(max_length=10, choices=GOAL_PERIOD)
    target_value = models.IntegerField(default=1)  # e.g. 20 miles in a week
    current_value = models.IntegerField(default=0)
    complete_by_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    parent_goal = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='sub_goals'
    )

    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
