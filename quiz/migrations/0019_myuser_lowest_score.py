# Generated by Django 2.2.4 on 2019-08-15 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0018_auto_20190815_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='lowest_score',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]