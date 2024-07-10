# Generated by Django 5.0.7 on 2024-07-09 23:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_tasks_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='accomplishments',
            field=models.TextField(blank=True, default='Custom Accomplishment'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='blockers',
            field=models.TextField(blank=True, default='Custom Blockers'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 7, 9, 23, 51, 12, 433970, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='document',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
