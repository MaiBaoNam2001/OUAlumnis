# Generated by Django 5.0.4 on 2024-05-11 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumnis', '0008_alter_alumniprofile_bio_alter_lecturerprofile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumniprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lecturerprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
