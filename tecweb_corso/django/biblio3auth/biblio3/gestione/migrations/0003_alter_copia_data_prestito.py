# Generated by Django 4.0.4 on 2022-04-15 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0002_alter_copia_utente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copia',
            name='data_prestito',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
