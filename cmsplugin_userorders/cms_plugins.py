from django.db.models import Count
from django.template.defaultfilters import title
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from shop.models.productmodel import Product

from cmsplugin_userorders.models import (
    UserOrderPluginSettings,
)

class UserOrdersPlugin(CMSPluginBase):
    model = UserOrderPluginSettings
    admin_preview = False
    name = title(_('DjangoShop : Users Orders'))
    render_template = "cmsplugin_userorders/base.html"
    filter_horizontal = ('filter_states', )

    def render(self, context, instance, placeholder):
        return context

plugin_pool.register_plugin(UserOrdersPlugin)
