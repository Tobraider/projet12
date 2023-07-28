# Generated by Django 4.2.2 on 2023-07-25 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='support_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
