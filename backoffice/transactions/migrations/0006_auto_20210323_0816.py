# Generated by Django 3.1.7 on 2021-03-23 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20210323_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.BigIntegerField(default='202574869033724', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='supermarket',
            name='supermarket_id',
            field=models.BigIntegerField(default='734702218553807', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.BigIntegerField(default='593017270690510', primary_key=True, serialize=False),
        ),
    ]
