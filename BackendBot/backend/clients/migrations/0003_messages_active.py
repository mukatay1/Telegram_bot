# Generated by Django 4.1 on 2022-09-06 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_rename_clients_clientsmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]