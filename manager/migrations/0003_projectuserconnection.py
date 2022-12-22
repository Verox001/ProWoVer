# Generated by Django 4.1.4 on 2022-12-10 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectUserConnection',
            fields=[
                ('project_user_connection_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('partner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partner', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
