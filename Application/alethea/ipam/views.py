from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from netaddr import IPNetwork

from ipam import models
from .forms import SubnetForm


def index(request):
    return redirect(reverse("ipam:subnets_index"))


def subnets_index(request):
    subnets = models.Subnet.objects.all()
    return render(request, "subnets_index.html", {"subnets": subnets})


def subnets_delete(request, subnet_id):
    subnet = get_object_or_404(models.Subnet, pk=subnet_id)
    if request.method == "POST":
        subnet.delete()
        messages.add_message(request, messages.SUCCESS, "Subnet has been deleted successfully")
        return redirect("ipam:subnets_index")
    return render(request, "delete_object.html", {
        "item_type": "subnet",
        "item_name": subnet.name,
        "cancel_url": reverse("ipam:subnets_index")
    })


def subnets_view(request, subnet_id):
    subnet_data = get_object_or_404(models.Subnet, pk=subnet_id)
    subnet_addresses = [str(x) for x in list(IPNetwork(f"{subnet_data.address}/{subnet_data.netmask}"))]

    print(subnet_addresses)

    pass


def subnets_add(request):
    error = None
    if request.method == "POST":
        form = SubnetForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            subnet = models.Subnet(name=data["name"], address=data["address"], netmask=data["mask_bits"])
            subnet.save()
            messages.add_message(request, messages.SUCCESS, "Subnet has been added successfully")
            return redirect("ipam:subnets_index")
        else:
            field_errors = []
            for field in form:
                for error in field.errors:
                    field_errors.append({"field": field.label, "error": str(error)})
            error = render_to_string("form_error.html", {
                "message": "Unable to add subnet, the following errors were found",
                "field_errors": field_errors
            })
            messages.add_message(request, messages.ERROR, error)
    else:
        form = SubnetForm()

    return render(request, "subnets_add.html", {"form": form})
