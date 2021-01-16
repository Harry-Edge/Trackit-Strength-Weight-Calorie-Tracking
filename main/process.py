from .models import *
from datetime import datetime, timedelta


def add_weight_entry(user, inputted_weight):

    if user.weight_preference == 'LBS':
        inputted_weight = round((float(inputted_weight) / 2.20462), 1)
    Weight.objects.get_or_create(user=user, inputted_weight=float(inputted_weight),
                                 date_of_entry=datetime.today().date())


def add_calorie_entry(user, inputted_calories):

    Calories.objects.get_or_create(user=user, inputted_calories=inputted_calories,
                                   date_of_entry=datetime.today().date())


def add_strength_entry(user, exercise, record_weight_amount):

    if user.weight_preference == 'LBS':
        record_weight_amount = round((float(record_weight_amount) / 2.20462), 1)

    StrengthRecords.objects.get_or_create(user=user, exercise=exercise, weight_record=record_weight_amount,
                                          date_of_record=datetime.today().date())
    if exercise == 'Deadlift':
        user.deadlift_record = record_weight_amount
    elif exercise == 'Squat':
        user.squat_record = record_weight_amount
    elif exercise == 'Bench Press':
        user.bench_press_record = record_weight_amount
    elif exercise == 'Overhead Press':
        user.overhead_press_record = record_weight_amount
    user.save()


def get_weight_labels_and_data(user, date_range):

    if date_range == '+10':
        user.weight_data += 10
    elif date_range == '-10':
        user.weight_data -= 10
    else:
        user.weight_data = 0
    user.save()

    weight_labels = []
    weight_data = []

    previous_days = 20
    while previous_days != -1:
        weight_labels.append(((datetime.today().date() - timedelta(days=user.weight_data))
                              - timedelta(days=previous_days)).strftime('%d%m'))
        previous_days -= 1

    for entry in weight_labels:
        def check_if_entry_has_been_made(variable):
            for weight_entry in Weight.objects.filter(user=user):
                if variable == weight_entry.date_of_entry.strftime('%d%m'):
                    if user.weight_preference == 'LBS':
                        weight_data.append(weight_entry.inputted_weight * 2.20462)
                    else:
                        weight_data.append(weight_entry.inputted_weight)
                    return True

        if check_if_entry_has_been_made(entry) is not True:
            weight_data.append('null')

    return weight_labels, weight_data


def get_calorie_labels_and_data(user, date_range):

    if date_range == '+10':
        user.calorie_data += 10
    elif date_range == '-10':
        user.calorie_data -= 10
    else:
        user.calorie_data = 0
    user.save()

    calorie_labels = []
    calorie_data = []

    previous_days = 20
    while previous_days != -1:
        calorie_labels.append(((datetime.today().date() - timedelta(days=user.calorie_data))
                               - timedelta(days=previous_days)).strftime('%d%m'))
        previous_days -= 1

    for entry in calorie_labels:
        def check_if_entry_has_been_made(variable):
            for calorie_entry in Calories.objects.filter(user=user):
                if variable == calorie_entry.date_of_entry.strftime('%d%m'):
                    calorie_data.append(calorie_entry.inputted_calories)
                    return True

        if check_if_entry_has_been_made(entry) is not True:
            calorie_data.append('null')

    return calorie_labels, calorie_data


def get_strength_records_label(user, date_range):

    if date_range == '+20':
        user.strength_data += 20
    elif date_range == '-20':
        user.strength_data -= 20
    else:
        user.strength_data = 0
    user.save()

    # This generates labels for strength records based on the last 31 days
    strength_record_label = []
    previous_days = 31
    while previous_days != -1:
        strength_record_label.append(((datetime.today().date() - timedelta(days=user.strength_data))
                                     - timedelta(days=previous_days)).strftime('%d%m'))
        previous_days -= 1

    return strength_record_label


def get_strength_record_data(user, strength_record_label, exercise, current_record):

    strength_data = []

    for entry in strength_record_label:
        def check_if_entry_has_been_made(variable):
            for record in StrengthRecords.objects.filter(user=user, exercise=exercise):
                if variable == record.date_of_record.strftime('%d%m'):
                    if user.weight_preference == 'LBS':
                        strength_data.append(record.weight_record * 2.20462)
                    else:
                        strength_data.append(record.weight_record)
                    return True

        if check_if_entry_has_been_made(entry) is not True:
            strength_data.append('null')

    if StrengthRecords.objects.filter(user=user).count() >=1:
        if StrengthRecords.objects.filter(user=user, exercise=exercise).count() >= 1:
            if user.weight_preference == 'LBS':
                strength_data[-1] = current_record * 2.20462
            else:
                strength_data[-1] = current_record

    return strength_data


def change_weight_preference(user, option):

    if option == 'KG':
        user.weight_preference = 'KG'
    else:
        user.weight_preference = 'LBS'
    user.save()

def enable_or_disable_targets(user, option):

    if option == 'no':
        user.targets_enabled = False
    else:
        user.targets_enabled = True

    user.save()

