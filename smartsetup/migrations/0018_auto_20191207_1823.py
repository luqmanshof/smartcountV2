# Generated by Django 2.2.7 on 2019-12-07 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0017_generalledger_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chartnoteitems',
            options={'ordering': ['item_name']},
        ),
        migrations.AlterField(
            model_name='gjournaldetails',
            name='credit',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='gjournaldetails',
            name='debit',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
