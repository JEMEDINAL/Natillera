# Generated by Django 5.0.1 on 2024-01-29 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_natillera_socio_natillera_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socio',
            name='Celular',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='socio',
            name='ciudad',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='socio',
            name='correo',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='socio',
            name='departamento',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='socio',
            name='pais',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
