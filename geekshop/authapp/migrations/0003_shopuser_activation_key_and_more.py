# Generated by Django 4.0.4 on 2022-06-04 22:29

import authapp.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_alter_shopuser_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='activation_key',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='activation_key_expiry',
            field=models.DateTimeField(default=authapp.models.get_activation_key_expiry),
        ),
    ]
