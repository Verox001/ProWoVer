# Generated by Django 4.1.4 on 2022-12-07 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_alter_user_email_alter_user_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
