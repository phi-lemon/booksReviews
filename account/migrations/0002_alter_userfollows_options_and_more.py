# Generated by Django 4.1.3 on 2022-11-25 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userfollows',
            options={'ordering': ('-date_created',)},
        ),
        migrations.RenameField(
            model_name='userfollows',
            old_name='created',
            new_name='date_created',
        ),
    ]
