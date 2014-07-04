# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessPoint',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('ssid', models.CharField(max_length=128)),
                ('bssid', models.CharField(unique=True, max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('token', models.CharField(max_length=128)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeviceBatteryCheckin',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('value', models.DecimalField(max_digits=8, decimal_places=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeviceCheckin',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('when', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(to='recdep.Device')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='devicebatterycheckin',
            name='checkin',
            field=models.ForeignKey(to='recdep.DeviceCheckin'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='DeviceWifiCheckin',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('strength', models.IntegerField()),
                ('associated', models.BooleanField(default=False)),
                ('access_point', models.ForeignKey(to='recdep.AccessPoint')),
                ('checkin', models.ForeignKey(to='recdep.DeviceCheckin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.TextField()),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='accesspoint',
            name='location',
            field=models.ForeignKey(to='recdep.Place', null=True),
            preserve_default=True,
        ),
    ]
