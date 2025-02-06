# Generated by Django 5.1.5 on 2025-02-06 15:35

import django.contrib.postgres.fields
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=85, unique=True)),
                ('description', models.TextField(blank=True)),
                ('muscle_group', models.CharField(blank=True, max_length=50)),
                ('instructions', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, default=list), size=None)),
                ('target_muscles', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default=list, max_length=50), size=None)),
                ('synergist_muscles', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default=list, max_length=50), size=None)),
                ('equipment', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default=list, max_length=50), size=None)),
                ('compound_movement', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SetDict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_name', models.CharField(max_length=255)),
                ('set_order', models.IntegerField(blank=True, null=True)),
                ('set_number', models.IntegerField(blank=True, null=True)),
                ('set_type', models.CharField(blank=True, max_length=100)),
                ('reps', models.IntegerField(blank=True, null=True)),
                ('focus', models.CharField(blank=True, max_length=150)),
                ('rest', models.IntegerField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_name', models.CharField(max_length=255)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('complete', models.BooleanField(default=False)),
                ('user_weight', models.FloatField(blank=True, null=True)),
                ('sleep_score', models.IntegerField(blank=True, null=True)),
                ('sleep_quality', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
    ]
