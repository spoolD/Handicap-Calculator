# Generated by Django 4.0.5 on 2022-10-27 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_score_holes'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='handicap',
            field=models.FloatField(blank=True, null=True),
        ),
    ]