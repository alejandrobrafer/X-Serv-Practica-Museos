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
                ('Commentary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Museums',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Name', models.CharField(max_length=128)),
                ('Description', models.TextField(blank=True, null=True)),
                ('Schedule', models.TextField(blank=True, null=True)),
                ('Transport', models.TextField(blank=True, null=True)),
                ('Accessibility', models.IntegerField(choices=[(0, '0'), (1, '1')])),
                ('URL', models.URLField(max_length=500, blank=True, null=True)),
                ('Street_Name', models.CharField(max_length=64, blank=True, null=True)),
                ('Street_Type', models.CharField(max_length=32, blank=True, null=True)),
                ('Street_Num', models.FloatField(blank=True, null=True)),
                ('Locality', models.CharField(max_length=32, blank=True, null=True)),
                ('Province', models.CharField(max_length=32, blank=True, null=True)),
                ('Postal_Code', models.PositiveIntegerField(blank=True, null=True)),
                ('Neighborhood', models.CharField(max_length=32, blank=True, null=True)),
                ('District', models.CharField(max_length=32, blank=True, null=True)),
                ('Coor_X', models.PositiveIntegerField(blank=True, null=True)),
                ('CoorY', models.PositiveIntegerField(blank=True, null=True)),
                ('Latitude', models.FloatField(blank=True, null=True)),
                ('Length', models.FloatField(blank=True, null=True)),
                ('Phone', models.TextField(blank=True, null=True)),
                ('Email', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scored',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Museum', models.ForeignKey(to='museos.Museums')),
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
                ('Title', models.CharField(max_length=64, blank=True, null=True)),
                ('Font', models.CharField(max_length=32, blank=True, null=True)),
                ('Background_Color', models.CharField(max_length=32, blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='Museum',
            field=models.ForeignKey(to='museos.Museums'),
        ),
    ]
