# Generated by Django 4.0.2 on 2022-03-14 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_movimentacao_data_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentacao',
            name='data_hora',
            field=models.DateField(null=True, verbose_name='Data da operação'),
        ),
    ]
