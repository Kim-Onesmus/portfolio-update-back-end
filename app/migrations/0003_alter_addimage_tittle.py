# Generated by Django 4.2.11 on 2024-04-02 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_addproject_tittle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addimage',
            name='tittle',
            field=models.CharField(choices=[('about', 'About Image'), ('top', 'Top Image')], max_length=200),
        ),
    ]
