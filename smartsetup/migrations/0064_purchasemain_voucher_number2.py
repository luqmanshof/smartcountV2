# Generated by Django 3.0 on 2020-08-10 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0063_expensemain_voucher_number2'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasemain',
            name='voucher_number2',
            field=models.CharField(default='', max_length=256, null=True),
        ),
    ]
