# Generated by Django 5.1.4 on 2024-12-31 06:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeapp', '0002_supplier_is_approved_user_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='supplier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shoeapp.supplier'),
            preserve_default=False,
        ),
    ]
