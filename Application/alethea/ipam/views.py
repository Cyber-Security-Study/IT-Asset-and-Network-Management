from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse("ipam:subnets_index"))


def subnets_index(request):
    return render(request, "subnets_index.html")


def subnets_add(request):
    return render(request, "subnets_add.html")
