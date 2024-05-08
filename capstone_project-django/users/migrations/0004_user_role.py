# Generated by Django 5.0.2 on 2024-04-11 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.role'),
        ),
    ]