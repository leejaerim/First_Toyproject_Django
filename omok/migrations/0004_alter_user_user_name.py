# Generated by Django 3.2.2 on 2021-05-23 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omok', '0003_todo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(default='Guest', max_length=16),
        ),
    ]
