"""BookRecommend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
# urls.py

from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.hello, name='hello'),
    path('mainpage/', views.mainpage, name='mainpage'),
    path('zhuce/', views.zhuce, name='zhuce'),
    path('loginview/', views.loginview, name='loginview'),
    path('logout/', views.logout_view, name='logout'),
    path('library/', views.library, name='library'),
    path('search/', views.search, name='search'),
    path('record_and_show_book/<int:bid>/<str:isbn>/', views.record_and_show_book, name='record_and_show_book'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
]

