# Generated by Django 2.2.7 on 2020-01-23 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20191225_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='3', upload_to='media/'),
            preserve_default=False,
        ),
    ]
