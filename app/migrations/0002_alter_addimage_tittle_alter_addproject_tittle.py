# Generated by Django 4.2.11 on 2024-04-05 19:23

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
        migrations.AlterField(
            model_name='addproject',
            name='tittle',
            field=models.CharField(choices=[('development', 'Development'), ('design', 'Design')], max_length=200),
        ),
    ]
