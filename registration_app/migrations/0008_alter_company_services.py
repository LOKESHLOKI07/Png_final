# Generated by Django 5.1.3 on 2024-12-17 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_app', '0007_company_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='services',
            field=models.TextField(max_length=255, null=True),
        ),
    ]
