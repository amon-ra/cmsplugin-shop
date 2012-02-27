from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import title
from django.db.models import Count

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from shop.models import (
  Product,
  OrderItem
)

from cmsplugin_topproducts.models import TopSellingProductsSettings


class TopProductsPlugin(CMSPluginBase):
    model = TopSellingProductsSettings
    admin_preview = False
    name = title(_('DjangoShop: Top Selling Products'))
    render_template = "cmsplugin_topproducts/top_products.html"


    def render(self, context, instance, placeholder):
        """This is the main rendering function. We "simply" query the
        database to get the top N products (as defined in the plugin
        instance), and pass them to the context"""

        top_products_data = OrderItem.objects.values(
        'product_reference').annotate(
                product_count=Count('product_reference')
            ).distinct('product_reference') \
            .order_by('product_count')

        # For Future Quick Reference :
        # The top_products_data result should be in the form:
        # [
        #   {
        #    'product_reference': '<product_id>',
        #    'product_count': <count>
        #   },
        #   ...
        # ]

        top_products_list = []
        for values in top_products_data:
            if len(top_products_list) >= instance.count:
                break
            id_references = values.get('product_reference')
            total = values.get('product_count')
            try:
                product = Product.objects.get(id=id_references)

                top_products_list.append({
                  'object': product,
                  'count' : total
                })
            except Product.DoesNotExist:
                pass

        # TODO: Cache top_products_list, invalidate on new order (or just
        # periodically maybe, it's not critical). Should be cached per
        # instance.number_of_products, obviously.


        # all cmsplugin templates have access to (overly simplified ):
        #
        #    plugin.instance
        #
        # where `instance` is the settings model of this cmsplugin
        # which in this case is a row/object in :
        #
        #    cmsplugin_topproducts.models.TopSellingProductsSettings

        context.update({
            'Products': top_products_list,
        })
        return context
plugin_pool.register_plugin(TopProductsPlugin)
