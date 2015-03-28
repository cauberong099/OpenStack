from django.conf.urls import patterns, include, url
from registration import views
urlpatterns = patterns('',
    url(r'register', views.registration, name='register'),
    url(r'^confirm/(?P<uid>\w{0,50})/$', views.confirm, name='confirm'),
    	)
