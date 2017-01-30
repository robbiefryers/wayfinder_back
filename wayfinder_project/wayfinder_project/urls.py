from django.conf.urls import include, url
from django.contrib import admin
from wayfinder import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('wayfinder.urls')),
]

