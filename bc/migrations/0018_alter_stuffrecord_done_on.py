# Generated by Django 4.1.4 on 2023-07-07 09:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bc', '0017_alter_shoprecord_added_on_alter_shoprecord_done_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stuffrecord',
            name='done_on',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
