# Generated by Django 5.1.4 on 2025-04-10 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_app', '0015_company_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
