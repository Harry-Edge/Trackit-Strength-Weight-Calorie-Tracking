# Generated by Django 3.1.2 on 2021-01-10 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_weight_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weight',
            old_name='calories',
            new_name='inputted_weight',
        ),
    ]
