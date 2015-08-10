"""desafio URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from market.views import MarketEndpoint, MarketProcessEndpoint

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^security/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),

    url(r'^$', MarketEndpoint.as_view()),
    url(r'^market/import/', MarketEndpoint.as_view()),
    url(r'^market/process/', MarketProcessEndpoint.as_view()),
]