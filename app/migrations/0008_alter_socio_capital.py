# Generated by Django 5.0.1 on 2024-02-03 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_socio_fecha_cuota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socio',
            name='capital',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]