# Generated by Django 3.2.18 on 2023-09-23 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.RemoveField(
            model_name='bus',
            name='id',
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_id',
            field=models.PositiveIntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='busid',
            field=models.CharField(max_length=5, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='userid',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(max_length=5, primary_key=True, serialize=False),
        ),
    ]
