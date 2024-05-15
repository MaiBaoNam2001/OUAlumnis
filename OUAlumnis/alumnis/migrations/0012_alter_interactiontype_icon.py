# Generated by Django 5.0.4 on 2024-05-12 08:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumnis', '0011_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interactiontype',
            name='icon',
            field=models.FileField(unique=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(['svg'])]),
        ),
    ]