# Generated by Django 3.0 on 2020-01-09 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0034_setupbegbalancemain_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setupbegbalancemain',
            name='entrydate',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='setupbegbalancemain',
            name='periodend',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='setupbegbalancemain',
            name='periodstart',
            field=models.DateTimeField(),
        ),
    ]
