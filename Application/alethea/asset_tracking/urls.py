from django.conf.urls import url

from . import views

app_name = "asset_tracking"
urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^assets/$", views.assets_index, name="assets_index"),
]