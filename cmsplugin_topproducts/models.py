from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin

from shop.models.productmodel import Product

class TopSellingProductsSettings(CMSPlugin):
    count = models.PositiveIntegerField(_("Number of Products"),
                help_text=_('How many top selling products to show.'))
