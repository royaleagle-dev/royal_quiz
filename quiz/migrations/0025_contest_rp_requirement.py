# Generated by Django 2.2.17 on 2020-11-26 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0024_contest'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='RP_requirement',
            field=models.IntegerField(default=50),
        ),
    ]
