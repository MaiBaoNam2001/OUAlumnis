# Generated by Django 5.0.4 on 2024-05-01 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumnis', '0004_user_password_reset_expiry_lecturerprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumniprofile',
            name='is_confirmed',
            field=models.BooleanField(default=True),
        ),
    ]