# Generated by Django 4.2.3 on 2023-08-02 08:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("foodapp", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Order",
        ),
    ]