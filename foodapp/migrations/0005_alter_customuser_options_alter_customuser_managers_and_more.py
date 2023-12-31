# Generated by Django 4.2.3 on 2023-08-08 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("foodapp", "0004_delete_order"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={},
        ),
        migrations.AlterModelManagers(
            name="customuser",
            managers=[],
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="date_joined",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="groups",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="is_staff",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="is_superuser",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="last_login",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="last_name",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="user_permissions",
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="foodapp.customuser",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="password",
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(max_length=30),
        ),
    ]
