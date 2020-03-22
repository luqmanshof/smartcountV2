# Generated by Django 3.0 on 2020-02-26 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0040_purchasedetails_asset_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setupdepartment',
            name='division',
        ),
        migrations.AddField(
            model_name='setupdivision',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.SetupDepartment'),
        ),
    ]
