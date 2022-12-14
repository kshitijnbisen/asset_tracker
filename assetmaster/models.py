from django.db import models
import uuid
# Create your models here.

class AssetType(models.Model):
    asset_type = models.TextField()
    asset_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asset_type
#
class Item(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length=200)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, related_name='asset')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.item_id)
    def __str__(self):
        return self.item_name

class AssetImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.item_id.item_name