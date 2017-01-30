from django.conf.urls import url
from django.conf.urls import include
from wayfinder import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    url(r'^login/$', views.login.as_view()),
    url(r'^register/$', views.register.as_view()),
    url(r'^get-favourites/$', views.favouritesList.as_view()),
    url(r'^new-favourite/$', views.newFavourite.as_view()),
    url(r'^journey-info/$', views.journeyInfo.as_view()),
    url(r'^fave-test/(?P<pk>[0-9]+)/$', views.favouritesTest.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)