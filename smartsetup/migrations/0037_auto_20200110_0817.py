# Generated by Django 3.0 on 2020-01-10 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0036_auto_20200109_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setupbegbalancemain',
            name='entrydate',
            field=models.DateTimeField(),
        ),
    ]
