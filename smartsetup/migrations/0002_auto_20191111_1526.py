# Generated by Django 2.2.7 on 2019-11-11 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receiptmain',
            options={'ordering': ['-date']},
        ),
    ]
