# Generated by Django 5.1.2 on 2024-11-09 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_shopping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopping',
            name='products',
        ),
        migrations.AddField(
            model_name='shopping',
            name='products',
            field=models.ManyToManyField(to='shop.flower2'),
        ),
    ]
