from django import template
from main import models


register = template.Library()


@register.simple_tag
def return_correct_weight_data(weight_preference, data):

    """ This will return weight_data depending on the users preference (KG/LBS)"""

    if data is None:
        return "Not Set"
    else:
        if weight_preference == 'LBS':
            data = round((data * 2.20462), 1)
            return data
        else:
            return data


@register.simple_tag
def return_weight_difference(weight_preference, weight_target, current_weight):

    try:
        if weight_preference == 'LBS':
            return round((round((weight_target * 2.20462), 1) - round((current_weight * 2.20462), 1)), 1)
        else:
            return round((weight_target - current_weight), 1)
    except TypeError:
        return "NA"

@register.simple_tag
def check_if_entry_has_been_made(user, exercise):

    if models.StrengthRecords.objects.filter(user=user, exercise=exercise).count() >= 1:
        return True
    else:
        return False


@register.simple_tag
def get_exercise_options():
    choices = models.StrengthRecords.EXERCISE_CHOICES

    return [i[0] for i in choices]