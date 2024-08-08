# Generated by Django 5.0.6 on 2024-07-29 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customization", "0005_alter_assistant_website"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assistant",
            name="website",
        ),
        migrations.AddField(
            model_name="assistant",
            name="websites",
            field=models.JSONField(default=list),
        ),
    ]
