# Generated by Django 4.1.4 on 2023-01-12 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0049_alter_qrcode_state'),
    ]

    operations = [
        migrations.DeleteModel(
            name='qrcode',
        ),
        migrations.AddField(
            model_name='transaction',
            name='state',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
