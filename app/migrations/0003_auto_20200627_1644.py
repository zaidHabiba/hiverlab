# Generated by Django 2.2.5 on 2020-06-27 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200622_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='create_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='program',
            name='description',
            field=models.TextField(null=True),
        ),
    ]