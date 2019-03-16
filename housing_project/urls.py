"""housing_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from housing_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    #path('', include('social_django.urls', namespace='social')),
    url(r'^logged-out/', views.logout, name='logout'),
    url(r'^$', views.home, name='home'),
    url(r'^apartments/$', views.apartments, name='apartments'),
    url(r'^apartments/(\d+)/', views.apartment_detail, name='apartment_detail'),
    url(r'^login/', views.login, name='login'),
    url(r'^favorites/', views.favorites, name='favorites'),
    url(r'^login-success/', views.loginsuccess, name='login-success'),
    url(r'^save_favorite/(\d+)/', views.save_favorite, name='save_favorite'),
    url(r'^delete_favorite/(\d+)/', views.delete_favorite, name='delete_favorite'),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile, name='profile'),
    url(r'^compare/', views.compare, name='compare'),
]

urlpatterns += staticfiles_urlpatterns()
