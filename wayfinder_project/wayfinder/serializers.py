from rest_framework import serializers
from models import Carer, Favourites, IDuser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from models import IDuser, Carer


#Serializer for creating a new account
class NewUserSerializer(serializers.ModelSerializer):
	username = serializers.CharField()
	carerName = serializers.CharField(allow_blank=False, write_only=True)
	idName = serializers.CharField(allow_blank=False, write_only=True)
	carerPhone = serializers.IntegerField(write_only=True)
	idPhone = serializers.IntegerField(write_only=True)
	pwordAgain = serializers.CharField(allow_blank=False, write_only=True)
	
	class Meta:
		model = User
		fields=('username', 'password', 'carerName', 'idName', 'carerPhone', 'idPhone', 'pwordAgain')

	def validate(self, data):
		carerName = data.get("carerName")
		idName = data.get("idName")
		carerPhone = data.get("carerPhone")
		idPhone = data.get("idPhone")
		username = data.get("username")
		password = data.get("password")
		pwordAgain = data.get("pwordAgain")
		usr_obj = None

		if password != pwordAgain:
			print 'passwords do not match'
			raise serializers.ValidationError("Passwords do not match")

		try:
			usr_obj = User.objects.get(username=username)

		except User.DoesNotExist:
			return data
		
		raise serializers.ValidationError("A user with that email already exists")


	def create(self, validated_data):

		print validated_data['username']
		print validated_data['carerName']

		#Create the new carer in the django user table
		newCarer = User(username=validated_data['username'], first_name=validated_data['carerName'])
		newCarer.set_password(validated_data['password'])
		newCarer.save()
		#Create the extension of carer with the extra phone field
		carer = Carer(carer=newCarer, phone=validated_data['carerPhone'])
		carer.save()
		#Create the new ID user and FK to carer
		newIDuser = IDuser(carer=newCarer, name=validated_data['idName'], phone=validated_data['idPhone'])
		newIDuser.save()

		return newCarer

class LoginSerializer(serializers.ModelSerializer):
	username = serializers.CharField()
	password = serializers.CharField()
	carerName = serializers.CharField(read_only=True)
	carerPhone = serializers.CharField(read_only=True)
	idName = serializers.CharField(read_only=True)
	idPhone = serializers.CharField(read_only=True)
	token = serializers.CharField(read_only=True)

	class Meta:
		model = User
		fields = ('username', 'password', 'token', 'carerName', 'idName', 'carerPhone', 'idPhone')
		extra_kwargs = {'password': {"write_only": True}}

	def validate(self, data):
		username = data.get("username")
		password = data.get("password")

		try:
			usr_obj = User.objects.get(username=username)

		except User.DoesNotExist:
			raise serializers.ValidationError("Incorrect username")

		if usr_obj:

			if not usr_obj.check_password(password):
				raise serializers.ValidationError("Incorrect password")

			#Retrieve names and phone numbers
			idUser = IDuser.objects.get(carer=usr_obj)
			data['carerName'] = usr_obj.first_name
			data['idName'] = idUser.name
			data['carerPhone'] = Carer.objects.get(carer=usr_obj).phone
			data['idPhone'] = idUser.phone


			try:
				data['token'] = Token.objects.get(user=usr_obj)
			except Token.DoesNotExist:
				print 'Invalid token'

		return data
	

#Serializer for basic place info
class FavouriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Favourites
		fields = ('name', 'picture', 'latitude', 'longitude')

	def create(self, validated_data):
		#The user object was sent as an extra argument in the save method in views
		usr = User.objects.get(username=validated_data['caregiver'].username)

		newFave = Favourites(
			name = validated_data['name'],
			latitude = validated_data['latitude'],
			longitude = validated_data['longitude'],
			caregiver = usr)
		newFave.save()
		return newFave

#Serializer for getting information about the place being navigated to
class JourneyInfoSerializer(serializers.ModelSerializer):
	destination = FavouriteSerializer(source='onJourneyTo', allow_null=True)
	timeStarted= serializers.DateTimeField(format="%m/%d/%Y %H:%M:%S", allow_null=True)
	class Meta:
		model = IDuser
		fields = ('currentLat', 'currentLng', 'currentHR', 'destination', 'timeStarted', 'onJourney', 'coords')




