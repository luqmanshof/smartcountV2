# Generated by Django 3.0 on 2020-01-28 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0039_purchasedetails_asset'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasedetails',
            name='asset_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.SetupFixedAssets'),
        ),
    ]
