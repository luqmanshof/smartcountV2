# Generated by Django 2.2.7 on 2019-12-11 14:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0018_auto_20191207_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseMain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Expense Date/Time')),
                ('voucher_number', models.PositiveIntegerField(default=100)),
                ('description', models.TextField(default='')),
                ('pay_mode', models.CharField(choices=[('cash', 'Cash'), ('cheque', 'Cheque'), ('transfer', 'Transfer'), ('draft', 'Draft')], default='Cheque', max_length=50)),
                ('total_amount', models.FloatField(default=0)),
                ('cash_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.ChartSubCategory', verbose_name='Cash Account')),
                ('credit_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.ChartNoteItems')),
                ('vendor', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.SetupVendors')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=256)),
                ('quantity', models.IntegerField(default=1)),
                ('unit_price', models.FloatField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('Debit_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.ChartNoteItems')),
                ('expense_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.ChartSubCategory', verbose_name='Expense Category')),
                ('expense_main_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='smartsetup.ExpenseMain')),
            ],
        ),
    ]
