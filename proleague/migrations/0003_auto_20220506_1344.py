# Generated by Django 3.2.5 on 2022-05-06 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proleague', '0002_auto_20220506_0342'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='developer',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='game',
            name='developer_website',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='game',
            name='website',
            field=models.CharField(default='', max_length=255),
        ),
    ]
