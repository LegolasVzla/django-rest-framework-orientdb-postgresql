# Generated by Django 2.2.1 on 2019-05-27 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_auto_20190526_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
