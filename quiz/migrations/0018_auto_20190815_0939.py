# Generated by Django 2.2.4 on 2019-08-15 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0017_myuser_score_depo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='highest_score',
            field=models.CharField(max_length=200),
        ),
    ]
