# Generated by Django 4.2.5 on 2023-09-30 17:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_profile_id_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="last_name",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="profile",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
    ]
