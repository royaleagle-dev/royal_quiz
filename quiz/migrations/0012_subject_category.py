# Generated by Django 2.2.4 on 2019-08-05 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_auto_20190805_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.Category'),
        ),
    ]