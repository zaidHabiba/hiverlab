# Generated by Django 2.2.5 on 2020-06-28 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_program_custome_command'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program',
            old_name='custome_command',
            new_name='custom_args',
        ),
    ]
