# Generated by Django 4.0.4 on 2022-05-07 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketapp', '0004_alter_basket_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]