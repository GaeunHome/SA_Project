# Generated by Django 4.1.4 on 2023-01-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0033_member_ac_code_alter_member_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIwash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MEM', models.CharField(max_length=20)),
                ('GPOINT', models.IntegerField()),
            ],
        ),
    ]
