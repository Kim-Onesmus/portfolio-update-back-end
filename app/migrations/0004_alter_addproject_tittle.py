# Generated by Django 4.2.11 on 2024-12-08 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_addproject_tittle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addproject',
            name='tittle',
            field=models.CharField(choices=[('graphic_design', 'Graphic Design'), ('web_design', 'Web Design'), ('development', 'Web Development')], max_length=200),
        ),
    ]
