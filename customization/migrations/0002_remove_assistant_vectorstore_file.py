# Generated by Django 5.0.6 on 2024-07-22 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customization", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assistant",
            name="vectorStore",
        ),
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="assistant_files/")),
                ("upload_date", models.DateTimeField(auto_now_add=True)),
                (
                    "assistant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="customization.assistant",
                    ),
                ),
            ],
        ),
    ]