from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)


class Model(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.CASCADE)


class CommentType(models.Model):
    name = models.CharField(max_length=255)


class Comment(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    comment_type = models.ForeignKey("CommentType", on_delete=models.CASCADE)
    # TODO: Asset ID
    # TODO: User ID


class AssetType(models.Model):
    name = models.CharField(max_length=255)


class AssetTypeContainmentItem(models.Model):
    asset_type = models.ForeignKey("AssetType", on_delete=models.CASCADE)
    can_contain = models.ForeignKey("AssetType", on_delete=models.CASCADE, related_name="container")


class AssetTypeField(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    asset_type = models.ForeignKey("AssetType", on_delete=models.CASCADE)


class Asset(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    asset_type = models.ForeignKey("AssetType", on_delete=models.CASCADE)
    # TODO: Site Room
    # TODO: Site Rack
    height = models.IntegerField(null=True)
    bottom_rack_slot = models.IntegerField(null=True)
    contained_by = models.ForeignKey("Asset", null=True)


class AssetFieldValue(models.Model):
    value = models.CharField(max_length=255)
    asset_type_field = models.ForeignKey("AssetTypeField")
    asset = models.ForeignKey("Asset")
