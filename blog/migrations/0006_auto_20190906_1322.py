# Generated by Django 2.1.7 on 2019-09-06 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.CharField(default='visitor', max_length=60),
        ),
    ]
