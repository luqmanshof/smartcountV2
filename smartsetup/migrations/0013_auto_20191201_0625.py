# Generated by Django 2.2.7 on 2019-12-01 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0012_auto_20191128_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiptmain',
            name='client',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.SetupClients', verbose_name='Client Name'),
        ),
    ]
