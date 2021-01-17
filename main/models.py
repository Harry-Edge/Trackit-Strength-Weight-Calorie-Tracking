from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):

    WEIGHT_CHOICES = [('KG', 'KG'), ('LBS', 'LBS')]

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    weight_preference = models.CharField(choices=WEIGHT_CHOICES, null=True, max_length=3)
    current_weight = models.FloatField(null=True)

    # Records
    deadlift_record = models.FloatField(null=True)
    bench_press_record = models.FloatField(null=True)
    squat_record = models.FloatField(null=True)
    overhead_press_record = models.FloatField(null=True)

    # Targets
    targets_enabled = models.BooleanField(default=False)
    weight_target = models.FloatField(null=True)
    deadlift_target = models.IntegerField(null=True)
    bench_press_target = models.IntegerField(null=True)
    squat_target = models.IntegerField(null=True)
    overhead_press_target = models.IntegerField(null=True)

    # Temporary store of data for previous/next entries
    weight_data_date_range = models.IntegerField(default=0)
    calorie_data_date_range = models.IntegerField(default=0)
    strength_data_date_range = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Weight(models.Model):

    user = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    inputted_weight = models.FloatField(null=True)
    date_of_entry = models.DateField(auto_now_add=False, null=True)

    def __str__(self):
        return f"{self.user} {self.date_of_entry} ({self.inputted_weight})"

    class Meta:
        verbose_name_plural = "Weight"


class Calories(models.Model):

    user = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    inputted_calories = models.IntegerField(null=True)
    date_of_entry = models.DateField(auto_now_add=False, null=True)

    def __str__(self):
        return f'{self.user} {self.date_of_entry} {self.inputted_calories}'

    class Meta:
        verbose_name_plural = "Calories"


class StrengthRecords(models.Model):

    EXERCISE_CHOICES = [('Deadlift', 'Deadlift'), ('Squat', 'Squat'), ('Bench Press', 'Bench Press'),
                        ('Overhead Press', 'Overhead Press')]

    user = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    exercise = models.CharField(choices=EXERCISE_CHOICES, null=True, max_length=20)
    weight_record = models.FloatField(null=True)
    date_of_record = models.DateField(auto_now_add=False, null=True)


    def __str__(self):
        return f'{self.user} {self.exercise} {self.weight_record} {self.date_of_record}'

    class Meta:
        verbose_name_plural = 'Strength Records'