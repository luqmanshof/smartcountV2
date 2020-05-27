# Generated by Django 3.0 on 2020-03-19 18:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0047_auto_20200312_2249'),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(default='', max_length=256)),
                ('department_code', models.CharField(default='', max_length=256)),
                ('description', models.TextField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetMain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_start', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('period_end', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('description', models.CharField(default='', max_length=256)),
                ('budget_no', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=256)),
                ('budget_type', models.CharField(choices=[('Revenue', 'Revenue'), ('Expenditure', 'Expenditure')], default='', max_length=256)),
                ('budget_dept', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.BudgetDepartment')),
                ('budget_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartsetup.ChartNoteItems')),
                ('budget_main_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='smartsetup.BudgetMain')),
            ],
        ),
    ]