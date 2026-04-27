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
def weekGoals(request):
    goals = Goal.objects.filter(user=request.user, goal_period="weekly")

    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.goal_period = "weekly"
            goal.save()
            return redirect("weekgoals")
    else:
        form = GoalForm()

    return render(request, "weekgoals.html", {
        "weeklygoals": goals,
        "form": form,
    })

@login_required
@require_POST
def update_progress_ajax(request):
    data = json.loads(request.body)

    goal_id = data.get("goal_id")
    clicked_value = int(data.get("value"))

    goal = Goal.objects.get(id=goal_id, user=request.user)

    current = goal.current_value

    # toggle logic
    if current == clicked_value:
        goal.current_value = clicked_value - 1
    else:
        goal.current_value = clicked_value

    # clamp at 0 (prevents negatives)
    if goal.current_value < 0:
        goal.current_value = 0

    goal.is_completed = goal.current_value >= goal.target_value
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