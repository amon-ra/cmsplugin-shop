import os
from os.path import join, getsize

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from shop.models.productmodel import Product

from appconf import AppConf

from .lib.choices import (
  DynamicTemplateChoices,
  DynamicChoice,
  )

class ApplicationSettings(AppConf):
    FEATUREDITEMS_LIST_TEMPLATES = "cmsplugin_featuredproducts/container"
    FEATUREDITEMS_ITEM_TEMPLATES = "cmsplugin_featuredproducts/item"

class FeaturedProductSettings(CMSPlugin):
    products = models.ManyToManyField("shop.Product",
      help_text=_('Which Products to promote'))

    container_template = models.CharField(choices=DynamicTemplateChoices(
                                  path=ApplicationSettings.FEATUREDITEMS_LIST_TEMPLATES,
                                  include='.html'),
        max_length=256, blank=True, null=True,
        default = ('default', os.path.join(ApplicationSettings.FEATUREDITEMS_LIST_TEMPLATES, "default.html")),
        help_text="""Select a template to render this
            list. Templates are stored in : {0}""".format(
              ApplicationSettings.FEATUREDITEMS_LIST_TEMPLATES))

    item_template = models.CharField(choices=DynamicTemplateChoices(
                                  path=ApplicationSettings.FEATUREDITEMS_ITEM_TEMPLATES,
                                  include='.html'),
        max_length=256, blank=True, null=True,
        default = os.path.join(ApplicationSettings.FEATUREDITEMS_ITEM_TEMPLATES,
      "default.html"),
          help_text="""Select a template to render the items in the list.
            Templates are stored in : {0}""".format(
              ApplicationSettings.FEATUREDITEMS_ITEM_TEMPLATES))
