# Generated by Django 2.2.17 on 2020-11-25 17:31

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0023_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=2000)),
                ('added', models.DateField(default=django.utils.timezone.now)),
                ('register_end', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
