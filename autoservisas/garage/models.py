from django.contrib.auth import get_user_model
from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from tinymce.models import HTMLField

User = get_user_model()

class CarModel(models.Model):
    brand = models.CharField(_("brand"), max_length=100, db_index=True)
    model = models.CharField(_("model"), max_length=100, db_index=True)
    year = models.IntegerField(_("year"), null=True, blank=True)
    engine = models.CharField(_("engine"), max_length=100, null=True, blank=True )

    class Meta:
        ordering = ["brand", "model"]
        verbose_name = _("car model")
        verbose_name_plural = _("car models")

    def __str__(self):
        return f"{self.brand}, {self.model}"

    def get_absolute_url(self):
        return reverse("carmodel_detail", kwargs={"pk": self.pk})
    

class Car(models.Model):
    license_plate = models.CharField(_("license_plate"), max_length=20, db_index=True)
    model = models.ForeignKey(CarModel, verbose_name=_("model"), related_name="cars", on_delete=models.CASCADE)
    vin = models.CharField(_("VIN"), max_length=17, db_index=True)
    note = models.TextField(_("note"), max_length=1000, null=True, blank=True)
    issue = HTMLField(_("issue"), max_length=1000, null=True, blank=True)

    image = models.ImageField(
        _("image"), 
        upload_to="garage/car_images", 
        null=True, 
        blank=True,
    )

    customer = models.ForeignKey(
        User,
        verbose_name=('customer'),
        on_delete=models.CASCADE,
        related_name='cars',
        null=True,
        blank=True,
    )
    
    class Meta:
        ordering = ["license_plate"]
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return f'{self.license_plate} {self.customer}'

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})
    

class Order(models.Model):
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    car = models.ForeignKey(Car, verbose_name=_("car"), related_name="orders", on_delete=models.CASCADE)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, default=0, db_index=True)
    order_notes = HTMLField(_("order_notes"), max_length=1000, null=True, blank=True)
    
    class Meta:
        ordering = ["date", "id"]
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    STATUS = (
        ("new", "New"),
        ("processing", "Processing"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )
    status = models.CharField(_("status"), max_length=20, choices= STATUS, blank=True, default='new', help_text="Status")
    due_back = models.DateField(_('due back'), null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
    @property
    def customer(self):
        return self.car.customer

    def __str__(self):
        return f"Order {self.id}"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})


class Service(models.Model):
    title = models.CharField(_("title"), max_length=100, db_index=True )
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, null=True, db_index=True)
    
    class Meta:
        ordering = ["title"]
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"pk": self.pk})


class OrderEntry(models.Model):
    service = models.ForeignKey(Service, verbose_name=_("service"), related_name="order_entries", on_delete=models.CASCADE)
    quantity = models.IntegerField(_("quantity"), null=True, db_index=True)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, null=True, db_index=True)
    order = models.ForeignKey(Order, verbose_name=_("order"), related_name="order_entries", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("order entry")
        verbose_name_plural = _("order entries")

    def __str__(self):
        return f"Order entry #{self.pk}: {self.service.title}"

    def get_absolute_url(self):
        return reverse("orderentry_detail", kwargs={"pk": self.pk})
    

class OrderReview(models.Model):
    order = models.ForeignKey(
        Order, 
        verbose_name=_('order'), 
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    reviewer = models.ForeignKey(
        User, 
        verbose_name=_("reviewer"), 
        on_delete=models.SET_NULL,
        related_name='order_reviews',
        null=True, blank=True,
    )
    reviewed_at = models.DateTimeField(_("Reviewed"), auto_now_add=True)
    content = models.TextField(_("content"), max_length=4000)

    class Meta:
        ordering = ['-reviewed_at']
        verbose_name = _("order review")
        verbose_name_plural = _("order reviews")

    def __str__(self):
        return f"{self.reviewed_at}: {self.reviewer}"

    def get_absolute_url(self):
        return reverse("orderreview_detail", kwargs={"pk": self.pk})
