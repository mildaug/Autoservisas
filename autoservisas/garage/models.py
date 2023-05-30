from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class CarModel(models.Model):
    brand = models.CharField(_('brand'), max_length=100)
    model = models.CharField(_('model'), max_length=100)
    year = models.IntegerField(_('year'), null=True)
    engine = models.CharField(_('engine'), max_length=100, null=100, blank=True)

    class Meta:
        ordering = ['brand', 'model']
        verbose_name = _("car model")
        verbose_name_plural = _("car models")

    def __str__(self):
        return f"{self.brand} {self.model}"
    
    def get_absolute_url(self):
        return reverse("carmodel_detail", kwargs={"pk": self.pk})
    
    
class Car(models.Model):
    license_plate = models.CharField(_('license_plate'), max_length=100, db_index=True)
    model = models.ForeignKey(CarModel, verbose_name=('model'), related_name='cars', on_delete=models.CASCADE)
    vin = models.CharField(_('vin'), max_length=100, db_index=True)
    customer = models.TextField(_('customer'), max_length=100, db_index=True)

    class Meta:
        ordering = ['license_plate']
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return f"{self.license_plate} {self.model} {self.vin} {self.customer}"
    
    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    date = models.DateField(_('date'), auto_now_add=True, null=True, db_index=True)
    car = models.ForeignKey(Car, verbose_name=('car'), related_name='orders', on_delete=models.CASCADE)
    price = models.DecimalField(_('price'), max_digits=18, decimal_places=2, null=True, db_index=True)

    class Meta:
        ordering = ['date', 'id']
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f"{self.date} {self.car} {self.price}"
    
    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})
    

class Service(models.Model):
    title = models.CharField(_('title'), max_length=100, db_index=True)
    price = models.DecimalField(_('price'), max_digits=18, decimal_places=2, null=True, db_index=True)

    class Meta:
        ordering = ['title']
        verbose_name = _('service')
        verbose_name_plural = _('services')

    def __str__(self):
        return f"{self.title} {self.price}"
    
    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"pk": self.pk})


class OrderEntry(models.Model):
    service = models.ForeignKey(Service, verbose_name=_('service'), related_name='order_entries', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), null=True, db_index=True)
    price = models.DecimalField(_('price'), max_digits=18, decimal_places=2, null=True, db_index=True)
    order = models.ForeignKey(Order, verbose_name=_('order'), related_name='order_entries', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('order entry')
        verbose_name_plural = _('order entries')

    def __str__(self):
        return f"{self.service.title} {self.quantity}"
    
    def get_absolute_url(self):
        return reverse("order entry_detail", kwargs={"pk": self.pk})