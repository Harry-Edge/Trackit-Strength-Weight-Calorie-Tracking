from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Weight)

admin.site.register(Calories)
admin.site.register(StrengthRecords)