# Generated by Django 3.1.2 on 2021-01-15 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20210115_2104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='track_calorie_data',
            new_name='calorie_data',
        ),
    ]
