# Generated by Django 5.0.2 on 2024-04-10 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rlab', '0001_initial'),
        ('rooms', '0002_room_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowedequipment',
            name='room',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rooms.room'),
            preserve_default=False,
        ),
    ]
