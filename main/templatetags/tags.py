from django import template
from main import models
from datetime import datetime, timedelta

register = template.Library()


@register.simple_tag
def get_average_weight(user):

    all_weights = models.Weight.objects.filter(user=user)
    last_30_day_weight_entries = []

    for entry in all_weights:
        if entry.date_of_entry >= (datetime.today().date() - timedelta(days=30)):
            last_30_day_weight_entries.append(entry.inputted_weight)

    if user.weight_preference == 'LBS':
        return f"{round((sum(last_30_day_weight_entries) / len(last_30_day_weight_entries) * 2.20462), 1)}" \
               f" {user.weight_preference}"
    return f"{round(sum(last_30_day_weight_entries) / len(last_30_day_weight_entries), 1)} {user.weight_preference}"


@register.simple_tag
def get_average_calories(user):
    all_calories = models.Calories.objects.filter(user=user)
    last_30_day_calorie_entries = []

    for entry in all_calories:
        if entry.date_of_entry >= (datetime.today().date() - timedelta(days=30)):
            last_30_day_calorie_entries.append(entry.inputted_calories)

    return f"{round(sum(last_30_day_calorie_entries) / len(last_30_day_calorie_entries))}"


@register.simple_tag
def get_correct_target_data(user, target):
    if user.weight_preference == "LBS":
        return round((target * 2.20462))
    return target


@register.simple_tag
def return_correct_weight_data(weight_preference, data):

    """ This will return weight_data depending on the users preference (KG/LBS)"""

    if data is None:
        return "Not Set"
    else:
        if weight_preference == 'LBS':
            data = round((data * 2.20462), 1)
            return f"{data} {weight_preference}"
        else:
            return f"{data} {weight_preference}"


@register.simple_tag
def return_weight_difference(weight_preference, weight_target, current_weight):

    try:
        if weight_preference == 'LBS':
            return f"{round((round((weight_target * 2.20462), 1) - round((current_weight * 2.20462), 1)), 1)}" \
                   f" {weight_preference}"
        else:
            return f"{round((weight_target - current_weight), 1)} {weight_preference}"
    except TypeError:
        return "NA"


@register.simple_tag
def check_if_weight_entry_has_been_made(user):

    """ Checks if a weight entry has ever been inputted by the current user,
     if so, it will display information is the user has targets enabled """

    if models.Weight.objects.filter(user=user):
        return True
    else:
        return False


@register.simple_tag
def check_if_entry_has_been_made(user, exercise):

    """ Checks if any strength entry for a particular exercise has ever been inputted
    by the current user, if so, it will display information is the user has targets enabled """

    if models.StrengthRecords.objects.filter(user=user, exercise=exercise).count() >= 1:
        return True
    else:
        return False


@register.simple_tag
def get_exercise_options():

    """ Get the different exercise options for entry on the selector """

    choices = models.StrengthRecords.EXERCISE_CHOICES

    return [i[0] for i in choices]


@register.simple_tag
def get_all_manual_entries():

    """ Gets all the entries (calories, weight, bench press, etc) so the user can manually add an entry """

    exercises = models.StrengthRecords.EXERCISE_CHOICES

    all_entries_list = ['Weight', 'Calories']
    for i in exercises:
        all_entries_list.append(i[0])

    return all_entries_list




