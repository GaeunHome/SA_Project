# Generated by Django 4.1.4 on 2022-12-29 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_member_id_alter_member_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='GPOINT',
            field=models.CharField(default=0, max_length=10000),
            preserve_default=False,
        ),
    ]
