# Generated by Django 4.1.4 on 2023-01-08 08:39

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0029_delete_qrcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='LOGIN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FKcheck', models.CharField(default=myapp.models.UUIDrand, max_length=36)),
                ('Rstate', models.CharField(max_length=42)),
                ('Raccesscode', models.CharField(max_length=43)),
            ],
        ),
    ]