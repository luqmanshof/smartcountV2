# Generated by Django 2.2.7 on 2019-11-24 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartsetup', '0005_generalledger_sub_trans'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generalledger',
            old_name='sub_Trans',
            new_name='main_Trans',
        ),
    ]
