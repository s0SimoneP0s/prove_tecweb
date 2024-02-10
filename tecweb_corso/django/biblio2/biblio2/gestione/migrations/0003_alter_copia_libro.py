# Generated by Django 4.0.2 on 2022-02-16 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0002_remove_libro_data_prestito_copia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copia',
            name='libro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copie', to='gestione.libro'),
        ),
    ]