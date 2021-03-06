# Generated by Django 3.1 on 2020-11-22 18:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseAdjustment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_gray', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RGBAdjustments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('red_value', models.IntegerField(default=100)),
                ('green_value', models.IntegerField(default=100)),
                ('blue_value', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='TypeAdjustment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_brightness', models.BooleanField(default=True)),
            ],
        ),
    ]
