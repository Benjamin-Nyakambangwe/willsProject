# Generated by Django 4.0.1 on 2023-04-18 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersaccess', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
            ],
        ),
    ]
