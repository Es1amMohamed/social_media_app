# Generated by Django 4.2.5 on 2023-10-02 17:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_post_video"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="link",
            new_name="like",
        ),
    ]
