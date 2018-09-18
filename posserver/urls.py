"""posserver URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from chart.views import websockTest
from chart.views import index, indexTest
import os

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^web/', websockTest),     # 处理 websocket
    url(r'^$', index),
    url(r'^test/', indexTest)
]

media_root = os.path.join(settings.BASE_DIR+'/posserver/','templates')
urlpatterns += static('/templates/', document_root=media_root)

# C:\Users\10104841C\posserver\posserver\templates\index.html