from django.contrib import admin
from . import models
from.models import OrderEntry

class OrderEntryInline(admin.TabularInline):
    model = OrderEntry
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'date', 'price', 'customer', 'due_back', 'status')
    inlines = [OrderEntryInline]


class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'model', 'vin', 'customer')
    list_filter = ('customer', 'model')
    search_fields = ('license_plate', 'vin')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')


class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewed_at', 'order', 'reviewer', 'content')


admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderEntry)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.OrderReview, OrderReviewAdmin)
