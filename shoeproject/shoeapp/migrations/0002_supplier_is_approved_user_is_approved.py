# Generated by Django 5.1.4 on 2024-12-31 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]