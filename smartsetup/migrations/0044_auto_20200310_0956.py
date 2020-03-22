# Generated by Django 3.0 on 2020-03-10 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0043_auto_20200305_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='setupvendors',
            name='payer_id',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='setupvendors',
            name='tin_number',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='setupvendors',
            name='vendor_type',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='setupvendors',
            name='city',
            field=models.CharField(default='', max_length=200),
        ),
    ]
