# Generated by Django 2.2.7 on 2019-12-18 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_profile_total_quiz_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='current_questions_list',
            field=models.CharField(default='1', max_length=2000),
            preserve_default=False,
        ),
    ]
