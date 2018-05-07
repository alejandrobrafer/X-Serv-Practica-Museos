"""practica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import *
from practica import settings
from django.contrib.auth.views import logout


urlpatterns = [
    # https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/views/
    url(r'^logout$', logout, {'next_page': '/'}),
    url(r'^login$', 'museos.views.login', name = "Función que proporciona el logeado"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'templates/style\.css', 'museos.views.define_style', name = "Función para definir el estilo CSS"),
 	url(r'^about$', 'museos.views.about', name = "Página para más informacion."),
	url(r'^museos/(\d+)$', 'museos.views.museum_page', name = "Página del museo."),
	url(r'^museos$', 'museos.views.museums', name = "Listado con todos los museos."),
	url(r'^$', 'museos.views.home', name = "Página principal"),
    url(r'^(.+)/xml$', 'museos.views.xml_user', name = "Canal XML del usuario."),
    url(r'templates/(?P<path>.*)$',  serve, {'document_root': settings.STATIC_URL}),
    url(r'^(.+)$', 'museos.views.user', name = "Página del usuario."),
]