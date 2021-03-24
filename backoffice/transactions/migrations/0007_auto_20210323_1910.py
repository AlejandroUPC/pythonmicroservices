# Generated by Django 3.1.7 on 2021-03-23 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_auto_20210323_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.BigIntegerField(default='595429501374353', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='supermarket',
            name='supermarket_id',
            field=models.BigIntegerField(default='663942915765257', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.BigIntegerField(default='234134790036190', primary_key=True, serialize=False),
        ),
    ]