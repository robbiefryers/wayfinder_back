from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions

from django.contrib.auth.models import User
from serializers import NewUserSerializer, LoginSerializer, JourneyInfoSerializer, FavouriteSerializer
from models import IDuser, Carer, Favourites
import time
from base64 import b64decode
from django.core.files.base import ContentFile


# Register View
class register(APIView):

	def post(self, request, format=None):
		data = request.data
		print data
		serializer = NewUserSerializer(data=data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class login(APIView):

	def post(self, request, *args, **kwargs):
		time.sleep(1)
		data = request.data
		serializer = LoginSerializer(data=data)

		if serializer.is_valid():
			print 'all good'
			return Response(serializer.data, status=status.HTTP_200_OK)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# IDusers journey info
class journeyInfo(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	
	#Get method for retrieving location info
	def get(self, request):
		carer = request.user
		print carer
		user = IDuser.objects.get(carer = carer)
		print user
		serializer = JourneyInfoSerializer(user)
		return Response(serializer.data, status=status.HTTP_200_OK)

	#post method called from ID user to start the journey
	def post(self, request, format=None):
		carer = request.user
		idUser = IDuser.objects.get(carer=carer)

		data = request.data
		saveDest = False

		#check if destination is in post (determines whether journe is being started or stopped)
		if 'destination' in data.keys():
			saveDest = True
			destination = Favourites.objects.get(caregiver=carer, name=data['destination'])
			print destination
			del data['destination']
		
		else:
			destination = None

		serializer = JourneyInfoSerializer(idUser, partial=True, data=request.data)

		if serializer.is_valid():
			serializer.save()
			if saveDest == True:
				idUser.onJourneyTo = destination
				idUser.save()
			return Response(serializer.data, status=status.HTTP_200_OK)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	#put method called from ID user to update location info
	def put(self, request, format=None):
		carer = request.user
		idUser = IDuser.objects.get(carer=carer)

		data = request.data

		serializer = JourneyInfoSerializer(idUser, partial=True, data=request.data)
		
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Favourites List View 
class favouritesList(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	
	def get(self, request):
		#Get the user who sent the request (django does this with token)
		#get a list of faves associated with that user
		usr = request.user
		print usr
		faves = Favourites.objects.filter(caregiver=usr)
		if faves:
			serializer = FavouriteSerializer(faves, many=True)
			print serializer.data
			return Response(serializer.data, status=status.HTTP_200_OK)

		else:
			print 'nating'
			return Response(status=status.HTTP_204_NO_CONTENT)


class newFavourite(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, format=None):
		data = request.data
		carer = request.user

		b64Picture = b64decode(request.data['picture'])

		
		del data['picture']

		serializer = FavouriteSerializer(data=data)

		if serializer.is_valid():
			newFave = serializer.save(caregiver=carer)
			print newFave
			newFave.picture = ContentFile(b64Picture,'png')
			newFave.save()
			return Response(serializer.data, status=status.HTTP_200_OK)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class favouritesTest(APIView):

	def get(self, request):

		faves = Favourites.objects.all()
		serializer = FavouriteSerializer(faves, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


	def post(self, request, format=None):

		data = request.data
		serializer = FavouriteSerializer(data = data)
		return Response(serializer.data, status=status.HTTP_200_OK)

'''
{
	"carerName": "Robbie",
	"idName": "Talita",
	"carerPhone": "0852324336",
	"idPhone": "0852324336",
	"username": "talita@gmail.com",
	"password": "test",
	"pwordAgain": "test"
}

'carerName', 'idName', 'carerPhone', 'idPhone', 'pwordAgain'

		carerName = data.get("carerName")
		idName = data.get("idName")
		carerPhone = data.get("carerPhone")
		idPhone = data.get("idPhone")
		username = data.get("email")
		pword = data.get("pword")
		pwordAgain = data.get("pwordAgain")


		if not (carerName or idName or carerPhone or idPhone or username):
			print 'Not all fields supplied'
			raise serializers.ValidationError("Not all fields supplied")

		if pword != pwordAgain:
			print 'passwords do not match'
			raise serializers.ValidationError("Passwords do not match")

'''
