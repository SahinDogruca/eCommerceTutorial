# Generated by Django 3.1.5 on 2021-04-30 18:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210430_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='contact',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
