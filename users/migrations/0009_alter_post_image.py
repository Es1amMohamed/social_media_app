# Generated by Django 4.2.5 on 2023-10-01 18:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_post"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="post_images"),
        ),
    ]
