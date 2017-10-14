from django.db import models


class Subnet(models.Model):
    address = models.CharField(max_length=255)
    netmask = models.IntegerField()
    name = models.CharField(max_length=255)


class DhcpRange(models.Model):
    start_address = models.CharField(max_length=255)
    end_address = models.CharField(max_length=255)
    subnet = models.ForeignKey(Subnet, on_delete=models.CASCADE)


class IpAddress(models.Model):
    address = models.CharField(max_length=255)
    description = models.TextField()
    is_failover = models.BooleanField()
    subnet = models.ForeignKey(Subnet, on_delete=models.CASCADE)

# TODO: Implement Address Assignments Table!
