from django import template
from main import models

register = template.Library()



@register.simple_tag
def get_exercise_options():
    choices = models.StrengthRecords.EXERCISE_CHOICES

    return [i[0] for i in choices]


