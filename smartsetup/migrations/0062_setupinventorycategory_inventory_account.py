# Generated by Django 3.0 on 2020-07-26 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0061_auto_20200726_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='setupinventorycategory',
            name='inventory_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventory_account', to='smartsetup.ChartNoteItems'),
        ),
    ]