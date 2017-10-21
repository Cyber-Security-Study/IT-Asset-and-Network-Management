from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse("asset_tracking:assets_index"))


def assets_index(request):
    return render(request, "assets_index.html")