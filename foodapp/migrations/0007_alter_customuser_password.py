# Generated by Django 4.2.3 on 2023-08-08 07:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("foodapp", "0006_alter_customuser_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="password",
            field=models.CharField(max_length=8),
        ),
    ]