# Generated by Django 2.0.8 on 2018-08-23 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDD_WEB', '0004_auto_20180823_1249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mongoconn',
            old_name='collection',
            new_name='auth_collection',
        ),
        migrations.AddField(
            model_name='mongoconn',
            name='ssl',
            field=models.BooleanField(default=False),
        ),
    ]
