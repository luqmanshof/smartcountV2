# Generated by Django 3.0 on 2020-01-26 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0037_auto_20200110_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasedetails',
            name='expense_main_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='smartsetup.PurchaseMain'),
        ),
    ]