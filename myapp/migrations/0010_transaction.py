# Generated by Django 4.1.4 on 2022-12-29 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_rename_account2_question_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('ORDID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('MEMID', models.CharField(max_length=20)),
                ('CDATE', models.DateTimeField()),
                ('GPOINT', models.IntegerField()),
                ('AMOUNT', models.IntegerField()),
                ('APPID', models.IntegerField()),
            ],
        ),
    ]