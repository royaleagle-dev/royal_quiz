# Generated by Django 2.2.4 on 2019-08-05 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0012_subject_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='temp_question_range',
            field=models.IntegerField(default=0),
        ),
    ]
