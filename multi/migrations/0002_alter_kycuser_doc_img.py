# Generated by Django 5.0.6 on 2024-07-01 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kycuser',
            name='doc_img',
            field=models.FileField(upload_to='kyc_docs'),
        ),
    ]
