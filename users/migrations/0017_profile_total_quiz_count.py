# Generated by Django 2.2.7 on 2019-12-15 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_pendingquestion_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='total_quiz_count',
            field=models.IntegerField(default=0),
        ),
    ]