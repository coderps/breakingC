# Generated by Django 4.1.4 on 2023-06-04 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bc', '0003_alter_stuff_where'),
    ]

    operations = [
        migrations.AddField(
            model_name='stuff',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='stuff',
            name='where',
            field=models.CharField(choices=[('kitchen', 'Kitchen'), ('work room', 'Work Room'), ('bedroom', 'Bedroom'), ('pole room', 'Pole Room'), ('living room', 'Living Room'), ('storage room', 'Storage Room'), ('small toilet', 'Small Toilet'), ('big toilet', 'Big Toilet'), ('garden', 'Garden'), ('bonus', 'Bonus')], max_length=40),
        ),
    ]
