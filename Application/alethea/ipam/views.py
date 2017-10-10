from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SubnetForm


def index(request):
    return redirect(reverse("ipam:subnets_index"))


def subnets_index(request):
    return render(request, "subnets_index.html")


def subnets_add(request):
    error_message = None
    if request.method == "POST":
        form = SubnetForm(request.POST)

        if form.is_valid():
            # Do something!
            pass
        else:
            error_message = "Unable to add subnet, one or more fields below are invalid" + str(form.errors)
    else:
        form = SubnetForm()

    return render(request, "subnets_add.html", {"form": form, "error_message": error_message})
