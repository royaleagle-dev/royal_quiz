# Generated by Django 2.2.7 on 2019-12-23 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_profile_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='attainable_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='percentage_score',
            field=models.IntegerField(default=0),
        ),
    ]