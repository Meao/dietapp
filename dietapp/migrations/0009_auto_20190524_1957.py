# Generated by Django 2.1.7 on 2019-05-24 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dietapp', '0008_auto_20190524_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='calcuim_qty',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='vit_a_qty',
            field=models.IntegerField(default=0),
        ),
    ]
