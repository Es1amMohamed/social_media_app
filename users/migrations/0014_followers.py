# Generated by Django 4.2.5 on 2023-10-06 14:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0013_likepost"),
    ]

    operations = [
        migrations.CreateModel(
            name="Followers",
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
                ("follower", models.CharField(max_length=100)),
                ("user", models.CharField(max_length=100)),
            ],
        ),
    ]
