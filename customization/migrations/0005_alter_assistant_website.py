# Generated by Django 5.0.6 on 2024-07-24 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customization", "0004_alter_assistant_website"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assistant",
            name="website",
            field=models.URLField(blank=True),
        ),
    ]