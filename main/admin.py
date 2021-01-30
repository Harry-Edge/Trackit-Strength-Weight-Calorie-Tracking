from django.contrib import admin
from .models import *

admin.site.register(Customer)

@admin.register(Calories)
class CalorieAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_entry', 'inputted_calories')


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_entry', 'inputted_weight')


@admin.register(StrengthRecords)
class StrengthRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'weight_record', 'date_of_record')