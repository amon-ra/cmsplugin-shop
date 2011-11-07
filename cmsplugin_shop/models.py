from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from shop.models.productmodel import Product


class TopProducts(CMSPlugin):
    number_of_products = models.IntegerField(help_text=_('How many products to show'))

