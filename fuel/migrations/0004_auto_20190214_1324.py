# Generated by Django 2.1.5 on 2019-02-14 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuel', '0003_fuelprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelprice',
            name='acquisition_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='取得日'),
        ),
    ]