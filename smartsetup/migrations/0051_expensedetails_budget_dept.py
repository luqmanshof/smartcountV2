# Generated by Django 3.0 on 2020-03-23 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0050_auto_20200323_0416'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensedetails',
            name='budget_dept',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.BudgetDepartment'),
        ),
    ]
