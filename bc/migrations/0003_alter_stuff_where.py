# Generated by Django 4.1.4 on 2023-06-04 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bc', '0002_alter_stuff_where'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stuff',
            name='where',
            field=models.CharField(choices=[('kitchen', 'Kitchen'), ('work room', 'Work Room'), ('bedroom', 'Bedroom'), ('pole room', 'Pole Room'), ('living room', 'Living Room'), ('storage room', 'Storage Room'), ('small toilet', 'Small Toilet'), ('big toilet', 'Big Toilet'), ('garden', 'Garden')], max_length=40),
        ),
    ]
