# Generated by Django 4.1.4 on 2022-12-14 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_project_dazs_projectuserconnection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectuserconnection',
            name='partner',
        ),
        migrations.AddField(
            model_name='projectuserconnection',
            name='is_partner',
            field=models.BooleanField(default=False),
        ),
    ]
