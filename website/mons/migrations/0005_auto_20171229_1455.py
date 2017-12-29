# Generated by Django 2.0 on 2017-12-29 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mons', '0004_auto_20171229_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monster',
            name='element',
            field=models.CharField(choices=[('Dark', 'Dark'), ('Fire', 'Fire'), ('Light', 'Light'), ('Water', 'Water'), ('Wind', 'Wind')], default='Fire', max_length=50, verbose_name='Element'),
        ),
    ]
