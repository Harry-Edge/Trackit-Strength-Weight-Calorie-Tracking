# Generated by Django 3.1.2 on 2021-01-10 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_customer_weight_preference'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputted_calories', models.IntegerField(null=True)),
                ('date_of_entry', models.DateField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
            ],
        ),
    ]
