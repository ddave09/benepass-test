# Generated by Django 3.2.6 on 2021-08-12 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0002_commands_result'),
    ]

    operations = [
        migrations.RenameField(
            model_name='machine',
            old_name='name',
            new_name='address',
        ),
        migrations.AddField(
            model_name='machine',
            name='password',
            field=models.CharField(default='', max_length=10000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='machine',
            name='user',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
