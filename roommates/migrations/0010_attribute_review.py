# Generated by Django 4.2.4 on 2023-09-23 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roommates', '0009_alter_attribute_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='review',
            field=models.ManyToManyField(blank=True, to='roommates.roommatereview'),
        ),
    ]
