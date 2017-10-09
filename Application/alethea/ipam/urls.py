from django.conf.urls import url

from . import views

app_name = "ipam"
urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^subnets/$", views.subnets_index, name="subnets_index"),
    url(r"^subnets/add/$", views.subnets_add, name="subnets_add"),
]