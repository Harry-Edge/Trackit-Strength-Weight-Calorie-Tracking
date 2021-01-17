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
import json

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
            messages.error(request, 'Username or Password Incorrect')
            return render(request, 'main/login.html')

    return render(request, 'main/login.html')


def register(request):
    if request.method =='POST':
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
            messages.success(request, messages.INFO, "Account Created Successfully")

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

    """ INPUT WEIGHT """
    inputted_weight = request.POST.get('input_weight')
    if inputted_weight is not None:
        if Weight.objects.filter(user=user, date_of_entry=datetime.today()).count() == 0:
            process.add_weight_entry(user, inputted_weight)
        else:
            messages.error(request, 'Weight entry has already been made today')

    if 'previous_weight_entries' in request.POST:
        weight_labels, weight_data = process.get_weight_labels_and_data(user, "+10")
    elif 'next_weight_entries' in request.POST:
        weight_labels, weight_data = process.get_weight_labels_and_data(user, "-10")
    else:
        weight_labels, weight_data = process.get_weight_labels_and_data(user, 0)

    """ INPUT CALORIES """
    input_calories = request.POST.get('input_calories')
    if input_calories is not None:
        if Calories.objects.filter(user=user, date_of_entry=datetime.today()).count() == 0:
            Calories.objects.get_or_create(user=user, inputted_calories=input_calories, date_of_entry=datetime.today().date())
        else:
            messages.error(request, 'Calorie entry has already been made today')

    if 'previous_calorie_entries' in request.POST:
        calorie_label, calorie_data = process.get_calorie_labels_and_data(user, "+10")
    elif 'next_calorie_entries' in request.POST:
        calorie_label, calorie_data = process.get_calorie_labels_and_data(user, "-10")
    else:
        calorie_label, calorie_data = process.get_calorie_labels_and_data(user, 0)

    """Strength Records"""
    exercise = request.POST.get('exercise_record')
    record_weight_amount = request.POST.get('input_record')
    if exercise is not None and record_weight_amount is not None:
        process.add_strength_entry(user, exercise, record_weight_amount)

    if 'previous_record_entries' in request.POST:
        strength_record_label = process.get_strength_records_label(user, "+20")
    elif 'next_record_entries' in request.POST:
        strength_record_label = process.get_strength_records_label(user, "-20")
    else:
        strength_record_label = process.get_strength_records_label(user, 0)

    deadlift_data = process.get_strength_record_data(user, strength_record_label, 'Deadlift', user.deadlift_record)
    bench_press_data = process.get_strength_record_data(user, strength_record_label, 'Bench Press',
                                                        user.bench_press_record)
    squat_data = process.get_strength_record_data(user, strength_record_label, 'Squat', user.squat_record)
    overhead_press_data = process.get_strength_record_data(user, strength_record_label, 'Overhead Press',
                                                           user.overhead_press_record)

    context = {'user': user, 'weight_labels': weight_labels, 'weight_data': weight_data,
               'calorie_labels': calorie_label, 'calorie_data': calorie_data,
               'strength_record_labels': strength_record_label, 'deadlift_data': deadlift_data, 'squat_data': squat_data,
               'bench_press_data': bench_press_data, 'overhead_press_data': overhead_press_data}

    return render(request, 'main/dashboard.html', context=context)

@login_required(login_url='login')
def profile(request):

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

    weight_preference = request.POST.get('change_weight_preference')
    if weight_preference != user.weight_preference and weight_preference is not None:
        print("cjge")
        process.change_weight_preference(user, weight_preference)
        messages.add_message(request, messages.INFO, "Updated Weight Preference")

    enable_targets = request.POST.get('enable_targets')
    if enable_targets == 'yes':
        enable_targets = True
    elif enable_targets == 'no':
        enable_targets = False
    if enable_targets != user.targets_enabled and enable_targets is not None:
        process.enable_or_disable_targets(user, enable_targets)
        messages.add_message(request, messages.INFO, "Enabled/Disabled Targets")

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

"""
    - can selected an black exercise
    - can add entries multipul entries on the same day 
    - MEssages is al over the place 
    - says 20 when account is created 
    - Targets still show option even if the user had made no entries 
    
"""



