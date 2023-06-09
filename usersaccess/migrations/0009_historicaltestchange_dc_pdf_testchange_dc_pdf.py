# Generated by Django 4.2 on 2023-04-25 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersaccess', '0008_alter_historicaltestchange_my_field_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltestchange',
            name='dc_pdf',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='testchange',
            name='dc_pdf',
            field=models.ImageField(blank=True, null=True, upload_to='deathCertificatesPdf/'),
        ),
    ]
