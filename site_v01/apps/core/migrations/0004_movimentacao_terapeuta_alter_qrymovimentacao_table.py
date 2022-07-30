# Generated by Django 4.0.6 on 2022-07-28 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_qrylistaordensservico'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentacao',
            name='terapeuta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.terapeuta'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='qrymovimentacao',
            table='qry_movimentacao',
        ),
    ]