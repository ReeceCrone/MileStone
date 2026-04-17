from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Goal

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def dayGoals(request):
    goals = Goal.objects.filter(goal_period='day')

    context = {
        "dailygoals": goals
    }

    return render(request, 'daygoals.html', context)