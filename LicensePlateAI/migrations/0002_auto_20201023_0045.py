# Generated by Django 3.1.1 on 2020-10-22 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LicensePlateAI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_type',
            name='ticket_type_name',
            field=models.CharField(choices=[('D', 'Vé ngày'), ('M', 'Vé tháng')], max_length=100),
        ),
    ]