# Generated by Django 5.0.6 on 2024-07-22 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatbot", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="thread",
            name="id",
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
