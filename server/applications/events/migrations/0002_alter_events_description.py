# Generated by Django 5.0.6 on 2024-06-09 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='description',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]