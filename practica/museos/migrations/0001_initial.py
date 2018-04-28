# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='Museums',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Name', models.CharField(max_length=128)),
                ('Accessibility', models.IntegerField(choices=[(0, '0'), (1, '1')])),
                ('URL', models.URLField(max_length=500)),
                ('Street_Name', models.CharField(max_length=64)),
                ('Street_Type', models.CharField(max_length=32)),
                ('Locality', models.CharField(max_length=32)),
                ('Province', models.CharField(max_length=32)),
                ('Neighborhood', models.CharField(max_length=32)),
                ('District', models.CharField(max_length=32)),
                ('Coor_X', models.PositiveIntegerField()),
                ('CoorY', models.PositiveIntegerField()),
                ('Latitude', models.FloatField(blank=True, null=True)),
                ('Length', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Selected',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('User', models.CharField(max_length=32)),
                ('Date', models.DateField(auto_now=True)),
                ('Museum', models.ForeignKey(to='museos.Museums')),
            ],
        ),
        migrations.CreateModel(
            name='User_Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('User', models.CharField(max_length=32)),
                ('Title', models.CharField(max_length=64, default='')),
                ('Font', models.CharField(max_length=32, blank=True, null=True)),
                ('Background_Color', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='Museum',
            field=models.ForeignKey(to='museos.Museums'),
        ),
    ]
