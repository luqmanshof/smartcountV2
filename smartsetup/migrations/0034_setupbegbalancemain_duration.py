# Generated by Django 3.0 on 2020-01-05 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0033_auto_20200105_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='setupbegbalancemain',
            name='duration',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], default='12', max_length=50),
        ),
    ]
