# Generated by Django 2.2.7 on 2019-12-19 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_profile_current_questions_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_questions_list',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]