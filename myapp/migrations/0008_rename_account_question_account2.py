# Generated by Django 4.1.4 on 2022-12-29 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='account',
            new_name='account2',
        ),
    ]