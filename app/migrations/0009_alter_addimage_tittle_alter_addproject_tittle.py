# Generated by Django 4.2.11 on 2024-11-28 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_buymecoffee_status_alter_addimage_tittle_and_more'),
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
            field=models.CharField(choices=[('graphic_design', 'Graphic Design'), ('web_design', 'Web Design'), ('development', 'Web Development')], max_length=200),
        ),
    ]