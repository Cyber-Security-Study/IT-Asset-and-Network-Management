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

    # TODO: The below doesn't like it when given IPv6 ranges (strangely enough!), need to refactor this to not expand
    # TODO: the entire subnet into a list and try to loop through it!  Loop through used_addresses then count the size
    # TODO: of the gaps perhaps?
    subnet_addresses = [str(x) for x in list(IPNetwork(f"{subnet_data.address}/{subnet_data.netmask}"))]

    # Get a dictionary containing each IpAddress as a dictionary, indexed by address
    used_addresses = dict([(x["address"], x) for x in models.IpAddress.objects.filter(subnet_id=subnet_id).values()])

    rows = []
    unused_count = 0
    unused_start = None
    unused_end = None
    for address in subnet_addresses:
        if address in used_addresses:
            if unused_count:
                rows.append({
                    "type": "unused",
                    "unused_count": unused_count,
                    "unused_start": unused_start,
                    "unused_end": unused_end
                })
                unused_count = 0

            rows.append({
                "type": "address",
                "address": used_addresses[address]
            })
        else:
            if unused_count == 0:
                unused_start = address
            unused_end = address
            unused_count += 1

    if unused_count:
        rows.append({
            "type": "unused",
            "unused_count": unused_count,
            "unused_start": unused_start,
            "unused_end": unused_end
        })

    return render(request, "subnets_subnet.html", {"subnet": subnet_data, "rows": rows})


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
