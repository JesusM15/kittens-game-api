# Generated by Django 4.2.17 on 2025-01-15 01:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(choices=[('ES', 'Español'), ('EN', 'English')], default='ES', max_length=3)),
                ('volume', models.FloatField(help_text='Valor decimal entre 0 y 1', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='settings',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='social.setting'),
        ),
    ]
