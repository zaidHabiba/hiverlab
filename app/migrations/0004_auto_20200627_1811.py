# Generated by Django 2.2.5 on 2020-06-27 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200627_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]