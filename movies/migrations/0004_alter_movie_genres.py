# Generated by Django 3.2 on 2021-04-25 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_collection_collection_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.CharField(blank=True, db_index=True, default='', max_length=30),
        ),
    ]
