# Generated by Django 5.0 on 2024-02-09 02:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KabKota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dapil_dpr', models.IntegerField()),
                ('dapil_dprdprov', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provinsi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kecamatan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dapil_kabkota', models.IntegerField()),
                ('laki_laki', models.IntegerField()),
                ('perempuan', models.IntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('kabkota', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wilayah.kabkota')),
            ],
        ),
        migrations.CreateModel(
            name='KelDesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kabkota', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wilayah.kabkota')),
                ('kecamatan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wilayah.kecamatan')),
                ('provinsi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wilayah.provinsi')),
            ],
        ),
        migrations.AddField(
            model_name='kabkota',
            name='provinsi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wilayah.provinsi'),
        ),
        migrations.CreateModel(
            name='Tps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.IntegerField()),
                ('lat', models.FloatField(default=0)),
                ('lng', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kabkota', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wilayah.kabkota')),
                ('kecamatan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wilayah.kecamatan')),
                ('keldesa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wilayah.keldesa')),
                ('provinsi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wilayah.provinsi')),
            ],
            options={
                'unique_together': {('keldesa', 'no')},
            },
        ),
    ]
