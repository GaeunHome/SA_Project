# Generated by Django 4.1.4 on 2023-01-03 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_alter_transaction_ordid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='qrcode',
        ),
        migrations.AddField(
            model_name='transaction',
            name='PRONAME',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='TIME',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
