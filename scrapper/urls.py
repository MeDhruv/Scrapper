"""noon_scraper URL Configuration

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

from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path("",home),
    path('admin/', admin.site.urls),
    path('register/',register),
    path("login/",login),
    path("logout/",logout),
    path("add_prod/",add_product),
    path("add_cat/",add_cat),
    path("products/",product),
    path("crawler/",crawler),
    path("product/detail/<int:id>/",detail),
    path("product/edit/<int:id>/",Edit),
    path("export/",Export),
    path("data/",scraped),
    path("del/<int:id>/",delete)
]
