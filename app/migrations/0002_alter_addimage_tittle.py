# Generated by Django 4.2.6 on 2023-11-09 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addimage',
            name='tittle',
            field=models.CharField(choices=[('top', 'Top Image'), ('about', 'About Image')], max_length=200),
        ),
    ]
