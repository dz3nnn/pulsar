from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
from pathlib import Path
from PIL import Image

from .tasks import convert_to_webp

import os


def validate_image_formats(value):
    if value:
        img = Image.open(value)
        if img.format.lower() not in settings.VALIDE_IMAGES_FORMAT:
            raise ValidationError(
                f"{img.format} %s" % (_("некорректный формат изображения."))
            )
    else:
        raise ValidationError(_("Ошибка при валидации изображения."))


PRODUCT_STATUSES = [
    ("HAVE", _("В наличии")),
    ("ORDER", _("Под заказ")),
    ("WAIT", _("Ожидается поступление")),
    ("HAVENT", _("Нет в наличии")),
    ("NOTPROD", _("Не производится")),
]


class Product(models.Model):

    name = models.CharField(verbose_name=_("название"), max_length=255)
    sku = models.CharField(verbose_name=_("артикул"), max_length=255)
    price = models.CharField(verbose_name=_("цена"), max_length=255)  # Better Decimal
    status = models.CharField(
        verbose_name=_("статус"),
        max_length=10,
        choices=PRODUCT_STATUSES,
    )
    image = models.ImageField(
        verbose_name=_("изображение"),
        upload_to="images",
        validators=[validate_image_formats],
    )

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        convert_to_webp(Path(self.image.path))

    def image_dict(self):
        return {
            "path": os.path.splitext(self.image.url)[0],
            "formats": [
                os.path.splitext(self.image.url)[1][1::],
                "webp",
            ],
        }

    def to_dict(self):
        return {
            "name": self.name,
            "sku": self.sku,
            "price": self.price,
            "status": self.get_status_display(),
            "image": self.image_dict(),
        }

    class Meta:
        verbose_name = _("товар")
        verbose_name_plural = _("товары")

    def __str__(self):
        return self.name
