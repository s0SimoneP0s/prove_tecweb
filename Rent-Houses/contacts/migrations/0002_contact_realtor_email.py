# Generated by Django 3.0.1 on 2019-12-20 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='realtor_email',
            field=models.EmailField(default='example@mail.com', max_length=254),
            preserve_default=False,
        ),
    ]
