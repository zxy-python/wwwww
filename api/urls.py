from django.conf.urls import url,include
from django.contrib import admin
from api import views
from rest_framework import routers

# router=routers.DefaultRouter()
# router.register(r'servers',views.ServerViewSet)
urlpatterns = [

    url(r'^asset.html$', views.asset),
    # url(r'^servers.html$', views.servers),
    # url(r'^servers/(\d+).html$', views.servers_detail),

    # url(r'^', include(router.urls)),
    url(r'^servers/$', views.ServerView.as_view()),
    url(r'^servers/(\d+)$', views.ServerDetail.as_view()),
]
