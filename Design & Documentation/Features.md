# Features
This document details various features that the application should support and
provides a brief description of each.  This document is very much subject to
change.  At this point it is more of a place for me to brain dump ideas and
therefore you are not expected to understand any of it!

## Assets
The system should allow tracking of various IT assets from servers to
workstations to network hardware such as switches and APs.  It should be
possible to create different types of assets with different sets of fields in
each (e.g. a switch could have a field for number of ports whereas a laptop may
  have a field for the CPU and RAM).  Manufacturers and models should be defined
  centrally and then assigned to assets.

Fields should be defined in one place and then added to each asset type.  This
will make filtering easier as it avoids having various custom fields that all
mean the same thing but are all defined in separate asset types.

There should be rapid searching available (e.g. "find a laptop with the
following serial number")

There should be a concept of one type of asset being able to contain another.
For example, VM hosts can contain VMs, blade enclosures can contain blade
servers.etc.

It should be possible to log various comments against an item.  The types of
types of these should be configurable however sensible defaults could include
"upgrade", "fault", "service call", "fault resolution", "repurpose."
This allows the full history of a device to be viewed.

## IP Addresses
The system should allow subnets to be defined and IP addresses within them to
be marked as in use and if applicable assigned to assets.  There should be
functionality to support floating/failover IPs (assigned to multiple assets)

On each subnet it should be possible to define DHCP ranges so to prevent IPs
from the DHCP pool being statically assigned to devices.

#### Potential - Still needs figured out
Some way to track VLANs and CARP VHIDs (and whatever the VRRP equivalent is).

## Sites
The system should allow sites to be created.  Sites are comprised of "rooms"
and rooms can contain zero or more racks.  Assets can then be assigned to racks
or directly to rooms as "non-racked devices."  If assigned to a rack, and the
asset has a size in rack units specified, the user can specify a slot within the
rack for it to be installed in.  If no size is specified then it will still be
marked as in the rack but will not have a placement (e.g. vertical PDUs or small
  devices on shelves.)

Racks can then be displayed to show the layout in a graphical form.

## Licences - Leave until later
The system should allow licences to be tracked.  There should be a way to store
licences including keys categorised by vendor and software product.  In the case
of keys it should be possible to mark a key as in use and, if applicable, assign
it to a device.

Could probably do with more research into different types of software licencing
beyond product keys and Microsoft Volume Licensing to get a better idea of other
features that could come in handy here.
