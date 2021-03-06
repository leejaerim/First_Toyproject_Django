# Generated by Django 3.2.2 on 2021-06-21 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('toy_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=12, null=True)),
                ('isAvailable', models.SmallIntegerField(default=1)),
                ('hasPassword', models.SmallIntegerField(default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toy_auth.user')),
            ],
            options={
                'db_table': 'room',
            },
        ),
    ]
