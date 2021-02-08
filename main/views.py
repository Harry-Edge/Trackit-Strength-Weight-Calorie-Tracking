from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .decorators import unauthenticated_user
from .models import *
from main import process
from datetime import datetime
from .forms import *


@unauthenticated_user
def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Username or Password Incorrect')
            return render(request, 'main/login.html')

    return render(request, 'main/login.html')


@unauthenticated_user
def register(request):

    if request.method == 'POST':
        user_creation_form = UserSignUpForm(request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            username = user_creation_form.cleaned_data.get('username')
            raw_password = user_creation_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            Customer.objects.create(user=user,
                                    first_name=user_creation_form.cleaned_data.get('first_name'),
                                    last_name=user_creation_form.cleaned_data.get('last_name'),
                                    email=user_creation_form.cleaned_data.get('email'),
                                    weight_preference='KG')
            messages.add_message(request, messages.SUCCESS, "Account Created Successfully")
            return redirect('login')
    else:
        user_creation_form = UserSignUpForm(request.POST)

    context = {'user_creation_form': user_creation_form}

    return render(request, 'main/register.html', context=context)


def logout_user(request):

    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):

    user = Customer.objects.get(user=request.user)

    # Input Weight Entry
    inputted_weight = request.POST.get('input_weight')
    if inputted_weight is not None:
        # Checks to see of a entry has already been made on the same date
        if Weight.objects.filter(user=user, date_of_entry=datetime.today()).count() == 0:
            process.add_weight_entry(user, inputted_weight)
        else:
            messages.add_message(request, messages.ERROR, 'Weight entry has already been made today')

    # Gets weight data/labels depending on users data range choice
    if 'previous_weight_entries' in request.GET:
        weight_labels, weight_data = process.get_weight_labels_and_data(user, "+10")
    elif 'next_weight_entries' in request.GET:
        weight_labels, weight_data = process.get_weight_labels_and_data(user, "-10")
    else:
        weight_labels, weight_data = process.get_weight_labels_and_data(user, 0)

    # Input Calorie Entry
    input_calories = request.POST.get('input_calories')
    if input_calories is not None:
        # Checks to see of a entry has already been made on the same date
        if Calories.objects.filter(user=user, date_of_entry=datetime.today()).count() == 0:
            process.add_calorie_entry(user, input_calories)
        else:
            messages.add_message(request, messages.ERROR, 'Calorie entry has already been made today')

    # Gets calorie data/labels depending on users data range choice
    if 'previous_calorie_entries' in request.GET:
        calorie_label, calorie_data = process.get_calorie_labels_and_data(user, "+10")
    elif 'next_calorie_entries' in request.GET:
        calorie_label, calorie_data = process.get_calorie_labels_and_data(user, "-10")
    else:
        calorie_label, calorie_data = process.get_calorie_labels_and_data(user, 0)

    # Input Strength Record Entry
    exercise = request.POST.get('exercise_record')
    record_weight_amount = request.POST.get('input_record')
    if exercise is not None and record_weight_amount is not None:
        if exercise == 'Select Exercise':
            messages.add_message(request, messages.ERROR, 'Please select a exercise when inputting a record')
        else:
            # Checks to see of a entry has already been made on the same date
            if StrengthRecords.objects.filter(user=user, exercise=exercise,
                                              date_of_record=datetime.today()).count() == 0:
                process.add_strength_entry(user, exercise, record_weight_amount)
            else:
                messages.add_message(request, messages.ERROR,
                                     'Record entry for this exercise has already been make today')

    # Gets Strength Record labels depending on users data range choice
    if 'previous_record_entries' in request.GET:
        strength_record_label = process.get_strength_records_label(user, "+20")
    elif 'next_record_entries' in request.GET:
        strength_record_label = process.get_strength_records_label(user, "-20")
    else:
        strength_record_label = process.get_strength_records_label(user, 0)

    # Gets strength data depending on exercise
    deadlift_data = process.get_strength_record_data(user, strength_record_label, 'Deadlift', user.deadlift_record)
    bench_press_data = process.get_strength_record_data(user, strength_record_label, 'Bench Press',
                                                        user.bench_press_record)
    squat_data = process.get_strength_record_data(user, strength_record_label, 'Squat', user.squat_record)
    overhead_press_data = process.get_strength_record_data(user, strength_record_label, 'Overhead Press',
                                                           user.overhead_press_record)

    context = {'user': user, 'weight_labels': weight_labels, 'weight_data': weight_data,
               'calorie_labels': calorie_label, 'calorie_data': calorie_data,
               'strength_record_labels': strength_record_label, 'deadlift_data': deadlift_data,
               'squat_data': squat_data, 'bench_press_data': bench_press_data,
               'overhead_press_data': overhead_press_data}

    return render(request, 'main/dashboard.html', context=context)


@login_required
def edit_entries(request):

    user = Customer.objects.get(user=request.user)

    # Edits entries
    edit_weight = request.POST.get('edit_weight')
    if edit_weight is not None:
        process.change_weight_entry\
            (user, edit_weight,
             datetime.strptime(request.POST.get('date_of_weight_entry'), '%b. %d, %Y').strftime('%Y-%m-%d'))
    edit_calories = request.POST.get('edit_calories')
    if edit_calories is not None:
        process.change_calorie_entry\
            (user, edit_calories,
             datetime.strptime(request.POST.get('date_of_calorie_entry'), '%b. %d, %Y').strftime('%Y-%m-%d'))
    edit_strength_record = request.POST.get('edit_record')
    if edit_strength_record is not None:
        process.change_strength_record_entry\
            (user, edit_strength_record, request.POST.get('edit_exercise'),
             datetime.strptime(request.POST.get('date_of_record_entry'), '%b. %d, %Y').strftime('%Y-%m-%d') )

    # Deletes entries
    delete_weight_entry = request.POST.get('delete_weight_entry')
    if delete_weight_entry is not None:
        process.delete_weight_entry(user, datetime.strptime(delete_weight_entry, '%b. %d, %Y').strftime('%Y-%m-%d'))
    delete_calorie_entry = request.POST.get('delete_calorie_entry')
    if delete_calorie_entry is not None:
        process.delete_calorie_entry(user, datetime.strptime(delete_calorie_entry, '%b. %d, %Y').strftime('%Y-%m-%d'))
    delete_strength_record = request.POST.get('delete_strength_entry')
    if delete_strength_record is not None:
        process.delete_strength_record\
            (user, datetime.strptime(delete_strength_record, '%b. %d, %Y').strftime('%Y-%m-%d'),
             request.POST.get('delete_exercise'))

    # Gets all of the weight/calorie/strength record entries and orders them
    weight_entries = Weight.objects.filter(user=user).order_by("-date_of_entry")
    calorie_entries = Calories.objects.filter(user=user).order_by("-date_of_entry")
    strength_records = StrengthRecords.objects.filter(user=user).order_by("-date_of_record")

    context = {'user': user, 'weight_entries': weight_entries, 'calorie_entries': calorie_entries,
               'strength_records': strength_records}

    return render(request, 'main/edit_entries.html', context=context)


@login_required(login_url='login')
def profile(request):

    # Update Profile Form
    if request.method == 'POST':
        user_update_form = UserProfileForm(request.POST, instance=request.user)
        if user_update_form.is_valid():
            user_update_form.save()
            messages.add_message(request, messages.INFO, 'Your account has been updated')
            return redirect('profile')
    else:
        user_update_form = UserProfileForm(instance=request.user)

    context = {'user_update_form': user_update_form}

    return render(request, 'main/profile.html', context=context)


@login_required(login_url='login')
def change_password(request):

    # Change Password Form
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=form.user)
            messages.add_message(request, messages.INFO, 'Your Password has been updated')
            return redirect('profile')
        else:
            messages.add_message(request, messages.ERROR, 'Incorrect information supplied')
            return redirect('change_password')
    else:
        form = ChangePasswordForm(user=request.user)
        context = {'form': form}

        return render(request, 'main/change_password.html', context=context)


@login_required(login_url='login')
def settings(request):

    user = Customer.objects.get(user=request.user)

    # Changes weight preference to 'KG' or 'LBS'
    weight_preference = request.POST.get('change_weight_preference')
    if weight_preference != user.weight_preference and weight_preference is not None:
        process.change_weight_preference(user, weight_preference)
        messages.add_message(request, messages.INFO, "Updated Weight Preference")

    # Enables/disables targets
    enable_targets = request.POST.get('enable_targets')
    if enable_targets == 'yes':
        enable_targets = True
    elif enable_targets == 'no':
        enable_targets = False
    if enable_targets != user.targets_enabled and enable_targets is not None:
        process.enable_or_disable_targets(user, enable_targets)
        messages.add_message(request, messages.INFO, "Enabled/Disabled Targets")

    # Changes target depending on weight/exercise
    edit_weight_target = request.POST.get('edit_weight_target')
    if edit_weight_target:
        process.change_target(user, 'Weight', edit_weight_target)
        messages.add_message(request, messages.INFO, "Updated Weight Target")
    edit_deadlift_target = request.POST.get('edit_deadlift_target')
    if edit_deadlift_target:
        process.change_target(user, 'Deadlift', edit_deadlift_target)
        messages.add_message(request, messages.INFO, "Updated Deadlift Target")
    edit_bench_press_target = request.POST.get('edit_bench_press_target')
    if edit_bench_press_target:
        process.change_target(user, 'Bench Press', edit_bench_press_target)
        messages.add_message(request, messages.INFO, "Updated Bench Press Target")
    edit_squat_target = request.POST.get('edit_squat_target')
    if edit_squat_target:
        process.change_target(user, 'Squat', edit_squat_target)
        messages.add_message(request, messages.INFO, "Updated Squat Target")
    edit_overhead_press_target = request.POST.get('edit_overhead_press_target')
    if edit_overhead_press_target:
        process.change_target(user, 'Overhead Press', edit_overhead_press_target)
        messages.add_message(request, messages.INFO, "Updated Overhead Press Target")

    context = {'user': user}

    return render(request, 'main/settings.html', context=context)