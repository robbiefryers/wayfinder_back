# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.IntegerField()),
                ('carer', models.OneToOneField(related_name=b'own', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('picture', models.ImageField(upload_to=b'favourite_imgs', blank=True)),
                ('latitude', models.FloatField()),
                ('longtitude', models.FloatField()),
                ('caregiver', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IDuser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('phone', models.IntegerField()),
                ('onJourney', models.BooleanField(default=False)),
                ('currentLat', models.FloatField(null=True, blank=True)),
                ('currentLng', models.FloatField(null=True, blank=True)),
                ('currentHR', models.IntegerField(null=True, blank=True)),
                ('carer', models.ForeignKey(to='wayfinder.Carer')),
                ('onJourneyTo', models.ForeignKey(to='wayfinder.Favourites')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
