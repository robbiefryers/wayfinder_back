from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from datetime import datetime, timedelta
import uuid
import os
import json



# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def storeImagePath(self, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('favourite_imgs', filename)

# Model tables here

# Extension of user class to accomodate extra details about registerd accounts
class Carer(models.Model):
	carer = models.OneToOneField(User, related_name='own')
	phone = models.IntegerField(null=False)

	def __unicode__(self):
		return self.carer.username

class Favourites(models.Model):

	caregiver = models.ForeignKey('auth.User', null=False)
	name = models.CharField(max_length=128)
	picture = models.ImageField(upload_to=storeImagePath, blank=True)
	latitude = models.FloatField(null=False, blank=False)
	longitude = models.FloatField(null=False, blank=False)


	def __unicode__(self):
		return self.name

class IDuser(models.Model):
	carer = models.ForeignKey(User, null=False)
	name = models.CharField(max_length=32, null=False, blank=False)
	phone = models.IntegerField(null=False)
	onJourney = models.BooleanField(default=False)
	onJourneyTo = models.ForeignKey(Favourites, null=True, blank=True)
	currentLat = models.FloatField(null=True, blank=True)
	currentLng = models.FloatField(null=True, blank=True)
	currentHR = models.IntegerField(null=True, blank=True)
	timeStarted = models.DateTimeField(null=True, blank=True)
	coords = models.TextField(null=True, blank=True)

	class Meta:
		verbose_name_plural = "IDuser"

	def __unicode__(self):
		return ('idUser')




