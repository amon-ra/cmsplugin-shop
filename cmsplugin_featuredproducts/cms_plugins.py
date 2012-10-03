from django.db.models import Count
from django.template.defaultfilters import title
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from shop.models.productmodel import Product

from cmsplugin_featuredproducts.models import (
    FeaturedProductSettings,
)

class FeaturedProductsPlugin(CMSPluginBase):
    model = FeaturedProductSettings
    admin_preview = False
    name = title(_('DjangoShop : Featured Products'))
    render_template = "cmsplugin_featuredproducts/base.html"
    filter_horizontal = ('products', )

    def render(self, context, instance, placeholder):
        """
        This is the main rendering function. We "simply" query the database
        to get the top N products (as defined in the plugin instance), and pass
        them to the context
        """

        return context

plugin_pool.register_plugin(FeaturedProductsPlugin)
