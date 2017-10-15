from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from netaddr import IPNetwork, IPAddress, IPRange

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
    subnet = IPNetwork(f"{subnet_data.address}/{subnet_data.netmask}")

    used_addresses = dict([(x["address"], x) for x in models.IpAddress.objects.filter(subnet_id=subnet_id).values()])
    ordered_addresses = sorted([IPAddress(x) for x in used_addresses.keys()])

    # TODO: Handle if there are no used addresses!

    rows = []

    if ordered_addresses:
        unused_start = IPRange(subnet[0], ordered_addresses[0])
        if unused_start.size - 1:
            rows.append({
                "type": "unused",
                "unused_count": unused_start.size - 1,
                "unused_start": unused_start[0],
                "unused_end": unused_start[-2]
            })

        last_used_address = ordered_addresses[0]
        for address in ordered_addresses:
            unused_between = IPRange(last_used_address, address)  # IPs on each end are in use!
            if (unused_between.size - 2) > 0:
                rows.append({
                    "type": "unused",
                    "unused_count": unused_between.size - 2,
                    "unused_start": unused_between[1],
                    "unused_end": unused_between[-2]
                })

            rows.append({
                "type": "address",
                "address": used_addresses[str(address)]
            })

            last_used_address = address

        unused_after = IPRange(ordered_addresses[-1], subnet[-1])
        if (unused_after.size - 1) > 0:
            rows.append({
                "type": "unused",
                "unused_count": unused_after.size - 1,
                "unused_start": unused_after[1],
                "unused_end": unused_after[-1]
            })
    else:
        rows.append({
            "type": "unused",
            "unused_count": subnet.size,
            "unused_start": subnet[0],
            "unused_end": subnet[-1]
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
