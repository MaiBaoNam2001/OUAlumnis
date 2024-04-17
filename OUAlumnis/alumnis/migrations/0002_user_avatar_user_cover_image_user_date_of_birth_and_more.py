# Generated by Django 5.0.4 on 2024-04-16 05:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumnis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/%Y/%m'),
        ),
        migrations.AddField(
            model_name='user',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='cover_images/%Y/%m'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alumnis.gender'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='alumnis.role'),
        ),
        migrations.CreateModel(
            name='AlumniProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('student_id', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(upload_to='images/%Y/%m')),
                ('workplace', models.CharField(blank=True, max_length=255, null=True)),
                ('position', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alumnis.faculty')),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alumnis.major')),
                ('school_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alumnis.schoolyear')),
            ],
        ),
    ]