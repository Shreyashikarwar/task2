"""
URL configuration for movie project.

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
from django.urls import path, include
from main_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movie', home, name='movie'),
    path('movie/list', movie_list, name='movie_list'),
    path('movie/add', add_movie, name='movie_add'),
    path('movie/update/<int:movie_id>', update_movie, name='movie_update'),
    path('movie/get', get_movie, name='movie_get'),
    path('movie/get/details/<int:movie_id>', get_movie_details, name='movie_get_details'),
    path('movie/delete/<int:movie_id>', delete_movie, name='delete_movie'),
    

]
