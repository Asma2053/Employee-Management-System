# Generated by Django 4.2.13 on 2025-01-08 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0002_remove_employee_model_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_model',
            name='name',
            field=models.CharField(default='Unknown', max_length=50),
        ),
    ]
