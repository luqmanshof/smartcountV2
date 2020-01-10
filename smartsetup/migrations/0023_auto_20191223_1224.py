# Generated by Django 3.0 on 2019-12-23 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0022_setupfixedassets_asset_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='setupfixedassets',
            name='accumulated_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accumulated_account', to='smartsetup.ChartNoteItems'),
        ),
        migrations.AddField(
            model_name='setupfixedassets',
            name='expense_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_account', to='smartsetup.ChartNoteItems'),
        ),
    ]
