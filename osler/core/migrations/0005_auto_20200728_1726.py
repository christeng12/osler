# Generated by Django 3.0.5 on 2020-07-28 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200722_1457'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patient',
            options={'permissions': [('patient.can_case_manage', 'Can act as a case manager.')]},
        ),
    ]