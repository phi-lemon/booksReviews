# Generated by Django 4.1.3 on 2022-11-30 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='upload',
            field=models.ImageField(blank=True, null=True, upload_to='covers/'),
        ),
    ]
