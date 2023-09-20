from django.contrib import admin

# Register your models here.
from .models import UploadedImage


class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ["image", "vehicle_number","uploaded_at"]

admin.site.register(UploadedImage, UploadedImageAdmin)
