# Generated by Django 5.0.7 on 2024-07-11 01:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='type',
        ),
        migrations.CreateModel(
            name='TypeTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='task_types', to='issue_tracker.task', verbose_name='Task')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='type_tasks', to='issue_tracker.type', verbose_name='Type')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='types',
            field=models.ManyToManyField(related_name='tasks', through='issue_tracker.TypeTask', to='issue_tracker.type', verbose_name='Type'),
        ),
    ]
