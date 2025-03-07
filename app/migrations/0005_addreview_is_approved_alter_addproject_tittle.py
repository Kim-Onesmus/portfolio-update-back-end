# Generated by Django 4.2.11 on 2025-01-12 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_addproject_tittle'),
    ]

    operations = [
        migrations.AddField(
            model_name='addreview',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='addproject',
            name='tittle',
            field=models.CharField(choices=[('web_design', 'Web Design'), ('graphic_design', 'Graphic Design'), ('development', 'Web Development')], max_length=200),
        ),
    ]
