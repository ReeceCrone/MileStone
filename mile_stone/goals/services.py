
def complete_goal(goal):
    goal.is_completed = True
    goal.current_value = goal.target_value
    goal.save()

    parent = goal.parent_goal

    while parent:
        parent.current_value += 1

        if parent.current_value >= parent.target_value:
            parent.is_completed = True

        parent.save()
        parent = parent.parent_goal