# Generated by Django 4.1.4 on 2022-12-29 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_product_productpoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='productimage1',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='productimage2',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]