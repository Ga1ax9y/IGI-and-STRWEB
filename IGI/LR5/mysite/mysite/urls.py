"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from hello import views



profile_patterns = [
    path("", views.profile,kwargs={"name":"Alexander","age":18}),
    path("new", views.new),
    path("old", views.old),
]

urlpatterns = [
    path('', views.index),
    path('about',views.about,kwargs={"name":"Alexander","age":18}),
    path('contact',views.contact),
    path('profile/',include(profile_patterns)),
    path('stats',views.stats),
    path('home',views.home),
    path('json',views.json),
    path('get',views.get),
    path('set',views.set),
    path('user',views.about),
    path('user/<str:name>',views.about),
    path('user/<str:name>/<int:age>',views.about), #через /alex/12

]
