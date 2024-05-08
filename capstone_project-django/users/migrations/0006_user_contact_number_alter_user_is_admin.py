# Generated by Django 5.0.2 on 2024-04-11 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_role_user_is_admin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contact_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]