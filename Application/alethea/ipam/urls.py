from django.conf.urls import url

from . import views

app_name = "ipam"
urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^subnets/$", views.subnets_index, name="subnets_index"),
    url(r"^subnets/add/$", views.subnets_add, name="subnets_add"),
    url(r"subnets/(?P<subnet_id>[0-9]+)/delete/$", views.subnets_delete, name="subnets_delete"),
    url(r"subnets/(?P<subnet_id>[0-9]+)/$", views.subnets_view, name="subnets_view"),
    url(r"addresses/(?P<address_id>[0-9]+)/delete/$", views.addresses_delete, name="addresses_delete"),
]