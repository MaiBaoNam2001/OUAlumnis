# Generated by Django 5.0.4 on 2024-04-16 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnis', '0002_user_avatar_user_cover_image_user_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='academicdegree',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='academicrank',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='faculty',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='gender',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='major',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='schoolyear',
            options={'ordering': ['-created_at']},
        ),
    ]