# Generated by Django 3.1.2 on 2021-01-15 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20210115_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='strength_data',
            field=models.IntegerField(null=True),
        ),
    ]
