from .models import *
from datetime import datetime, timedelta


def add_weight_entry(user, inputted_weight):

    """ Any inputted weight data is always stored in KG on the database,
     is the users preference is 'LBS' it is converted to KG before being stored """

    if user.weight_preference == 'LBS':
        inputted_weight = round((float(inputted_weight) / 2.20462), 1)
    Weight.objects.get_or_create(user=user, inputted_weight=float(inputted_weight),
                                 date_of_entry=datetime.today().date())

    user.current_weight = inputted_weight
    user.save()


def add_calorie_entry(user, inputted_calories):

    Calories.objects.get_or_create(user=user, inputted_calories=inputted_calories,
                                   date_of_entry=datetime.today().date())


def add_strength_entry(user, exercise, record_weight_amount):

    """ Any inputted strength data is always stored in KG on the database,
         is the users preference is 'LBS' it is converted to KG before being stored """

    if user.weight_preference == 'LBS':
        record_weight_amount = round((float(record_weight_amount) / 2.20462), 1)

    StrengthRecords.objects.get_or_create(user=user, exercise=exercise, weight_record=record_weight_amount,
                                          date_of_record=datetime.today().date())

    # Saves the new record to the customer model
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

    """ This function gets both the data and labels for the Weight line chart depending on the user date range. """

    # Adjusts date range by - or + 10 days
    if date_range == '+10':
        user.weight_data_date_range += 10
    elif date_range == '-10':
        user.weight_data_date_range -= 10
    else:
        user.weight_data_date_range = 0
    user.save()

    weight_labels = []
    weight_data = []

    # Generate labels for previous 20 days depending on date range
    previous_days = 20
    while previous_days != -1:
        weight_labels.append(((datetime.today().date() - timedelta(days=user.weight_data_date_range))
                              - timedelta(days=previous_days)).strftime('%d%m'))
        previous_days -= 1

    for entry in weight_labels:

        """ This checks in a weight entry has been made in the database compared to the label dates.
         If so, it is added to the weight data. If not, a value of 'null' is added. """

        def check_if_entry_has_been_made(label_date):
            for weight_entry in Weight.objects.filter(user=user):
                if label_date == weight_entry.date_of_entry.strftime('%d%m'):
                    if user.weight_preference == 'LBS':
                        weight_data.append(weight_entry.inputted_weight * 2.20462)
                    else:
                        weight_data.append(weight_entry.inputted_weight)
                    return True

        if check_if_entry_has_been_made(entry) is not True:
            weight_data.append('null')

    return weight_labels, weight_data


def get_calorie_labels_and_data(user, date_range):

    """ This function gets both the data and labels for the Calorie line chart depending on the user date range."""

    # Adjusts date range by - or + 10 days
    if date_range == '+10':
        user.calorie_data_date_range += 10
    elif date_range == '-10':
        user.calorie_data_date_range -= 10
    else:
        user.calorie_data_date_range = 0
    user.save()

    calorie_labels = []
    calorie_data = []

    previous_days = 20
    while previous_days != -1:
        calorie_labels.append(((datetime.today().date() - timedelta(days=user.calorie_data_date_range))
                               - timedelta(days=previous_days)).strftime('%d%m'))
        previous_days -= 1

    for entry in calorie_labels:

        """ This checks in a calorie entry has been made in the database compared to the label dates.
            If so, it is added to the calorie data. If not, a value of 'null' is added. """

        def check_if_entry_has_been_made(label_date):
            for calorie_entry in Calories.objects.filter(user=user):
                if label_date == calorie_entry.date_of_entry.strftime('%d%m'):
                    calorie_data.append(calorie_entry.inputted_calories)
                    return True

        if check_if_entry_has_been_made(entry) is not True:
            calorie_data.append('null')

    return calorie_labels, calorie_data


def get_strength_records_label(user, date_range):

    """ This function get labels for the Strength Record line chart depending on the user date range."""

    # Adjusts date range by - or + 10 days
    if date_range == '+20':
        user.strength_data_date_range += 20
    elif date_range == '-20':
        user.strength_data_date_range -= 20
    else:
        user.strength_data_date_range = 0
    user.save()

    # Generates labels for strength records for the previous 31 days depending on date range
    strength_record_label = []
    previous_days = 31
    while previous_days != -1:
        strength_record_label.append(((datetime.today().date() - timedelta(days=user.strength_data_date_range))
                                     - timedelta(days=previous_days)).strftime('%d%m'))
        previous_days -= 1

    return strength_record_label


def get_strength_record_data(user, strength_record_label, exercise, current_record):

    strength_data = []

    for entry in strength_record_label:

        """ This checks in a strength for a given exercise entry has been made in the database compared to
            the label dates. If so, it is added to the strength data. If not, a value of 'null' is added. """

        def check_if_entry_has_been_made(label_date):
            for record in StrengthRecords.objects.filter(user=user, exercise=exercise):
                if label_date == record.date_of_record.strftime('%d%m'):
                    if user.weight_preference == 'LBS':
                        strength_data.append(record.weight_record * 2.20462)
                    else:
                        strength_data.append(record.weight_record)
                    return True

        if check_if_entry_has_been_made(entry) is not True:
            strength_data.append('null')

    """ Below checks first to see if a user has entered any strength data for a particular exercise. If any entry has
        been made, the current data entry is appended from 'null' to the user current record. This is done so the line
        chart visually looks better due to the likely-hood of strength records taking weeks/months to be broken. """

    if StrengthRecords.objects.filter(user=user, exercise=exercise).count() >= 1:
        if user.weight_preference == 'LBS':
            strength_data[-1] = current_record * 2.20462
        else:
            strength_data[-1] = current_record

    return strength_data


def change_weight_preference(user, option):

    if option == 'KG':
        user.weight_preference = 'KG'
    elif option == 'LBS':
        user.weight_preference = 'LBS'

    user.save()


def enable_or_disable_targets(user, option):

    if option is False:
        user.targets_enabled = False
    else:
        user.targets_enabled = True

    user.save()


def change_target(user, option, new_amount):

    if option == 'Weight':
        user.weight_target = new_amount
    elif option == 'Deadlift':
        user.deadlift_target = new_amount
    elif option == 'Bench Press':
        user.bench_press_target = new_amount
    elif option == 'Squat':
        user.squat_target = new_amount
    elif option == 'Overhead Press':
        user.overhead_press_target = new_amount

    user.save()