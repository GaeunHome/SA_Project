# Generated by Django 4.1.4 on 2022-12-29 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_member_gpoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='GPOINT',
            field=models.IntegerField(),
        ),
    ]
