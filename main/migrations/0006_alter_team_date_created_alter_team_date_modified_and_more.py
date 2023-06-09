# Generated by Django 4.0.7 on 2023-03-25 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_team_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='team',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Modified'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Modified'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Modified'),
        ),
    ]
