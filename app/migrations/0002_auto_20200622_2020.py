# Generated by Django 2.2.5 on 2020-06-22 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program',
            old_name='project_name',
            new_name='project',
        ),
    ]
