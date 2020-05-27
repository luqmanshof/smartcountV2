# Generated by Django 3.0 on 2020-05-27 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0054_auto_20200520_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='website',
            field=models.URLField(blank=True, default=''),
        ),
    ]
