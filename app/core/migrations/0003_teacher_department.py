# Generated by Django 5.1.2 on 2025-01-26 10:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_initial"),
        ("school", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="teacher",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="teachers",
                to="school.department",
            ),
        ),
    ]
