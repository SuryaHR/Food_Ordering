# Generated by Django 4.2.3 on 2023-07-28 13:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("foodapp", "0003_customuser_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurant",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]