# Generated by Django 2.0 on 2018-01-13 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mons', '0008_auto_20171229_1958'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodForTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(default='', max_length=100, verbose_name='Tag')),
                ('display', models.CharField(default='', max_length=100, verbose_name='Tag Display')),
            ],
        ),
        migrations.RemoveField(
            model_name='monster',
            name='good_for',
        ),
        migrations.AddField(
            model_name='monster',
            name='good_for',
            field=models.ManyToManyField(to='mons.GoodForTag'),
        ),
    ]
