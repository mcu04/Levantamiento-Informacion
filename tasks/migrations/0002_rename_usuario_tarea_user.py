# Generated by Django 5.1.2 on 2024-10-13 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarea',
            old_name='usuario',
            new_name='user',
        ),
    ]
