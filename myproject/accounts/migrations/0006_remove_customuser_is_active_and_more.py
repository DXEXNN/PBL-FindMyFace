# Generated by Django 5.1 on 2024-11-12 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_customuser_id_alter_customuser_custom_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_staff',
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='User',
        ),
    ]
