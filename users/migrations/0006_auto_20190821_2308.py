# Generated by Django 2.2.4 on 2019-08-21 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190821_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='userCategory',
            field=models.CharField(blank=True, choices=[('1', 'basic user'), ('2', 'advanced user'), ('3', 'master user'), ('4', 'basic admin')], default='1', max_length=2),
        ),
    ]