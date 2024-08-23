# Generated by Django 5.0.7 on 2024-07-22 15:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_alter_tasks_accomplishments_alter_tasks_blockers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='document',
        ),
        migrations.AddField(
            model_name='tasks',
            name='documents',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 7, 22, 15, 50, 5, 180298, tzinfo=datetime.timezone.utc)),
        ),
    ]