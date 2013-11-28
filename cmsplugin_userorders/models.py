import os
from os.path import join, getsize

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict

from cms.models.pluginmodel import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField

from shop.models import (
  Product,
  Order
)

from appconf import AppConf

from .fields import MultiSelectField
from .lib.choices import (
  DynamicTemplateChoices,
  DynamicChoice,
  )

class ApplicationSettings(AppConf):
    USERORDER_LIST_TEMPLATES = "cmsplugin_userorders/container"
    USERORDER_ITEM_TEMPLATES = "cmsplugin_userorders/item"

ORDER_STATE_CHOICES = Order.STATUS_CODES
ORDER_FIELD_CHOICES = [
  ('Current Status',     'status'),
  ('Creation Date',      'created'),
  ('Last Modified Date', 'modified'),
  ('Shipping Address',   'shipping_address_text')
]


class UserOrderPluginSettings(CMSPlugin):

    title = models.CharField(max_length=100, default=_("Your Order History"))

    container_template = models.CharField(
        max_length=256, blank=True, null=True,
        choices=DynamicTemplateChoices(
            path=ApplicationSettings.USERORDER_LIST_TEMPLATES, include='.html'),
        default = os.path.join(ApplicationSettings.USERORDER_LIST_TEMPLATES, "default.html"),
        help_text="Select a template to render this list. Templates are stored in : {0}"\
            .format(ApplicationSettings.USERORDER_LIST_TEMPLATES))

    empty_text = HTMLField(default=_("You haven't placed any orders yet."))

    item_template = models.CharField(
        max_length=256, blank=True, null=True,
        choices=DynamicTemplateChoices(
            path=ApplicationSettings.USERORDER_ITEM_TEMPLATES, include='.html'),
        default = os.path.join(ApplicationSettings.USERORDER_ITEM_TEMPLATES, "default.html"),
        help_text="Select a template to render the items in the list. Templates are stored in : {0}"\
            .format(ApplicationSettings.USERORDER_ITEM_TEMPLATES))

    sort_by = models.CharField(max_length=32, choices=ORDER_FIELD_CHOICES)
    filter_states = MultiSelectField(max_length=32, choices=ORDER_STATE_CHOICES, blank=True, null=False)
