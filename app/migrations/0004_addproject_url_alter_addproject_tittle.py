# Generated by Django 4.2.11 on 2024-04-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_addimage_tittle'),
    ]

    operations = [
        migrations.AddField(
            model_name='addproject',
            name='url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='addproject',
            name='tittle',
            field=models.CharField(choices=[('development', 'Development'), ('design', 'Design')], max_length=200),
        ),
    ]
