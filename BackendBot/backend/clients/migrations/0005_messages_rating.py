# Generated by Django 4.1 on 2022-09-07 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_clientsmodel_id_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='rating',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
