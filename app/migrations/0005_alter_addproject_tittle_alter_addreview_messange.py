# Generated by Django 4.2.11 on 2024-04-06 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_addproject_url_addreview_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addproject',
            name='tittle',
            field=models.CharField(choices=[('development', 'Development'), ('design', 'Design')], max_length=200),
        ),
        migrations.AlterField(
            model_name='addreview',
            name='messange',
            field=models.TextField(max_length=1000),
        ),
    ]