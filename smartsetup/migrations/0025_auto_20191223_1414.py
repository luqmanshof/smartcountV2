# Generated by Django 3.0 on 2019-12-23 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0024_auto_20191223_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='setupfixedassets',
            name='depreciation_method',
            field=models.CharField(choices=[('Straight-line', 'Straight-line'), ('Double declining balance', 'Double declining balance'), ('Sum of years', 'Sum of years'), ('Units of production', 'Units of production')], default='Single', max_length=50),
        ),
        migrations.AddField(
            model_name='setupfixedassets',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
