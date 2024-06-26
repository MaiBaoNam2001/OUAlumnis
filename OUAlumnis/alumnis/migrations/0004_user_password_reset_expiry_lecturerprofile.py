# Generated by Django 5.0.4 on 2024-04-20 08:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumnis', '0003_alter_academicdegree_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_reset_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='LecturerProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('image', models.ImageField(upload_to='images/%Y/%m')),
                ('bio', models.TextField(blank=True, null=True)),
                ('is_locked', models.BooleanField(default=False)),
                ('academic_degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alumnis.academicdegree')),
                ('academic_rank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alumnis.academicrank')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alumnis.faculty')),
            ],
        ),
    ]
