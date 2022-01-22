# Generated by Django 4.0.1 on 2022-01-22 18:25

import authentication.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='', max_length=512, upload_to=authentication.utils.content_file_name),
        ),
    ]
