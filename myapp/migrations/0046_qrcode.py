# Generated by Django 4.1.4 on 2023-01-12 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0045_alter_aiwash_tax_alter_transaction_cdate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='qrcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mem', models.CharField(max_length=43)),
                ('TIME', models.IntegerField(null=True)),
                ('state', models.BooleanField()),
            ],
        ),
    ]
