from django.shortcuts import render,  redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Goal
from django.contrib.auth import login
from .forms import GoalForm

@login_required
def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

@login_required
def dayGoals(request):
    goals = Goal.objects.filter(user=request.user, goal_period="day")

    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.goal_period = "day"
            goal.save()
            return redirect("daygoals")
    else:
        form = GoalForm()

    return render(request, "daygoals.html", {
        "dailygoals": goals,
        "form": form,
    })

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})