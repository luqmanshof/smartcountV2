# Generated by Django 3.0 on 2019-12-23 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0023_auto_20191223_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setupfixedassets',
            name='asset_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asset_account', to='smartsetup.ChartNoteItems'),
        ),
    ]
