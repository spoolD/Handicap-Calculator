# Generated by Django 4.0.5 on 2022-10-20 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=64)),
                ('date', models.DateField()),
                ('score', models.IntegerField()),
                ('rating', models.FloatField()),
                ('slope', models.IntegerField()),
                ('differential', models.FloatField()),
                ('golfer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
