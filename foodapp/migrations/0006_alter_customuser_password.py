# Generated by Django 4.2.3 on 2023-08-08 07:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("foodapp", "0005_alter_customuser_options_alter_customuser_managers_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="password",
            field=models.CharField(max_length=255),
        ),
    ]
