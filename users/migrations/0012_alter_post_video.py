# Generated by Django 4.2.5 on 2023-10-02 17:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0011_rename_link_post_like"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="video",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="videos_uploaded",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"]
                    )
                ],
            ),
        ),
    ]
