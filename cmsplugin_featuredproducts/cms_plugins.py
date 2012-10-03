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
        Return the list of products that has been picked,
        filtered by only products that are active.
        """

        products = instance.products.filter(active=True)

        context.update({'Products': products})
        return context

plugin_pool.register_plugin(FeaturedProductsPlugin)
