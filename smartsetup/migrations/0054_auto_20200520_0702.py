# Generated by Django 3.0 on 2020-05-20 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0053_auto_20200401_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensedetails',
            name='budget_dept',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.BudgetDetails'),
        ),
    ]
