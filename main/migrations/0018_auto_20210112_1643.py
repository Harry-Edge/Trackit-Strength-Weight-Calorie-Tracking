# Generated by Django 3.1.2 on 2021-01-12 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20210111_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='squat_record',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='weight',
            name='inputted_weight',
            field=models.FloatField(null=True),
        ),
    ]
