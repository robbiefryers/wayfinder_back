from django.contrib import admin
from models import Carer, Favourites, IDuser

class CarerAdmin(admin.ModelAdmin):
	list_display = ('carer', 'phone')

class IDuserAdmin(admin.ModelAdmin):
	list_display = ('carer', 'name', 'phone', 'onJourney')

class FavouritesAdmin(admin.ModelAdmin):
	list_display = ('caregiver', 'name', 'picture', 'latitude', 'longitude')

admin.site.register(Carer, CarerAdmin)
admin.site.register(IDuser, IDuserAdmin)
admin.site.register(Favourites, FavouritesAdmin)
