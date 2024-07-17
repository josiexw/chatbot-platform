# Generated by Django 5.0.6 on 2024-07-10 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Assistant",
            fields=[
                (
                    "id",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=256)),
                ("instructions", models.TextField(max_length=512)),
                (
                    "tools",
                    models.CharField(
                        choices=[
                            ("code_interpreter", "Code Interpreter"),
                            ("file_search", "File Search"),
                        ],
                        max_length=50,
                    ),
                ),
                ("vectorStore", models.CharField(max_length=100)),
                (
                    "model",
                    models.CharField(
                        choices=[
                            ("gpt-4o", "GPT-4o"),
                            ("gpt-4-turbo", "GPT-4 Turbo"),
                            ("gpt-4-turbo-2024-04-09", "GPT-4 Turbo with Vision"),
                            ("gpt-4-0125-preview", "GPT-4 Turbo preview 0125"),
                            ("gpt-4-1106-preview", "GPT-4 Turbo preview 1106"),
                            ("gpt-4-0613", "GPT-4 from June 13th 2023"),
                            ("gpt-3.5-turbo-0125", "GPT-3.5 Turbo"),
                            ("gpt-3.5-turbo-1106", "GPT-3.5 Turbo 1106"),
                            ("gpt-3.5-turbo-instruct", "GPT-3.5 Turbo Instruct"),
                        ],
                        max_length=50,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Chat",
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
                ("title", models.CharField(max_length=200)),
                ("header_color", models.CharField(max_length=7)),
                ("assistant_color", models.CharField(max_length=7)),
                ("user_color", models.CharField(max_length=7)),
                ("assistant_start_message", models.TextField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name="VectorStore",
            fields=[
                (
                    "id",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=200)),
                ("upload", models.FileField(upload_to="uploads/")),
                ("expiration", models.IntegerField()),
            ],
        ),
    ]