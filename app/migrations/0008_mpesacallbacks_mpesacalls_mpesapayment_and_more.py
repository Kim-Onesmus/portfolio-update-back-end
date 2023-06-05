# Generated by Django 4.2 on 2023-06-05 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_addproject_tittle'),
    ]

    operations = [
        migrations.CreateModel(
            name='MpesaCallBacks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ip_address', models.TextField()),
                ('caller', models.TextField()),
                ('conversation_id', models.TextField()),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': 'Mpesa Call Back',
                'verbose_name_plural': 'Mpesa Call Backs',
            },
        ),
        migrations.CreateModel(
            name='MpesaCalls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ip_address', models.TextField()),
                ('caller', models.TextField()),
                ('conversation_id', models.TextField()),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': 'Mpesa Call',
                'verbose_name_plural': 'Mpesa Calls',
            },
        ),
        migrations.CreateModel(
            name='MpesaPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('type', models.TextField()),
                ('reference', models.TextField()),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.TextField()),
                ('organization_balance', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Mpesa Payment',
                'verbose_name_plural': 'Mpesa Payments',
            },
        ),
        migrations.AlterField(
            model_name='addimage',
            name='tittle',
            field=models.CharField(choices=[('about', 'About Image'), ('top', 'Top Image')], max_length=200),
        ),
        migrations.AlterField(
            model_name='addproject',
            name='tittle',
            field=models.CharField(choices=[('design', 'Design'), ('development', 'Development')], max_length=200),
        ),
    ]
