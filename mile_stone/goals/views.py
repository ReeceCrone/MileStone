from django.shortcuts import render,  redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Goal
from django.contrib.auth import login
from .forms import GoalForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

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

@login_required
@require_POST
def update_progress_ajax(request):
    data = json.loads(request.body)

    goal_id = data.get("goal_id")
    value = data.get("value")

    goal = Goal.objects.get(id=goal_id, user=request.user)

    goal.current_value = value
    goal.is_completed = int(goal.current_value) >= int(goal.target_value)
    goal.save()

    return JsonResponse({
        "success": True,
        "current_value": goal.current_value,
        "is_completed": goal.is_completed,
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