# Generated by Django 3.0.5 on 2020-09-10 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import osler.core.validators
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('core', '0004_auto_20200909_2326'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drug',
            options={'ordering': ['name'], 'permissions': [('export_csv', 'Can export drug inventory')]},
        ),
        migrations.AlterField(
            model_name='drug',
            name='stock',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.CreateModel(
            name='HistoricalDrug',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[osler.core.validators.validate_name])),
                ('dose', models.FloatField()),
                ('stock', models.PositiveSmallIntegerField()),
                ('expiration_date', models.DateField(help_text='MM/DD/YYYY')),
                ('lot_number', models.CharField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('category', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.DrugCategory')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('manufacturer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.Manufacturer')),
                ('unit', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.MeasuringUnit')),
            ],
            options={
                'verbose_name': 'historical drug',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='DispenseHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('written_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('dispense', models.PositiveSmallIntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('author_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.Group')),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Drug')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Patient')),
            ],
            options={
                'verbose_name_plural': 'dispense history',
                'ordering': ['written_datetime'],
            },
        ),
    ]