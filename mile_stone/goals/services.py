def complete_goal(goal):
    goal.is_completed = True
    goal.current_value = goal.target_value
    goal.save()