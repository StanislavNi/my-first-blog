from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^string/$', views.print_string),
]
