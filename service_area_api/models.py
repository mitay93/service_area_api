from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.gis.db import models as gis_models


class Provider(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255
    )
    email = models.EmailField(
        verbose_name=_("email"),
        unique=True
    )
    phone_number = models.CharField(
        verbose_name=_("phone number"),
        max_length=15
    )
    language = models.CharField(
        verbose_name=_("language"),
        max_length=2,
        help_text=_("ISO 639-1 language code"),
    )
    currency = models.CharField(
        verbose_name=_("currency"),
        max_length=3,
        help_text=_("ISO 4217 currency code")
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = '-id',


class ServiceArea(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=100
    )
    price = models.DecimalField(
        verbose_name=_("price"),
        max_digits=10,
        decimal_places=2
    )
    polygon = gis_models.PolygonField(
        verbose_name=_("polygon"),
        spatial_index=True
    )
    provider = models.ForeignKey(
        verbose_name=_("provider"),
        to=Provider,
        related_name='service_areas',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = '-id',
