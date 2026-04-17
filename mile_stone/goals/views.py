from django.shortcuts import render,  redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Goal

@login_required
def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

@login_required
def dayGoals(request):
    goals = Goal.objects.filter(user=request.user)

    context = {
        "dailygoals": goals.filter(goal_period='day')
    }

    return render(request, 'daygoals.html', context)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})