# -*- coding: utf-8 -*-
import os

from django import template
from django.conf import settings

from classytags.helpers import InclusionTag
from classytags.core import Options, Tag
from classytags.arguments import Argument

from shop.util.cart import get_or_create_cart

from shop.models.productmodel import Product
from shop.models.ordermodel import Order

register = template.Library()

class UsersOrder(Tag):
    """
    Inclusion tag for displaying order.
    """
    name = 'user_orders'
    template = os.sep.join(('shop','templatetags','_order.html'))
    options = Options(
        Argument('user', resolve=True, required=False),
        Argument('status', resolve=True, required=False),
        'as',
        Argument('varname', resolve=False),
        blocks=[('enduser_orders', 'nodelist')],
    )
    def render_tag(self, context, user=None, status=None, varname=None, nodelist=None):
        context.push()
        orders = Order.objects.filter(user = user)
        context[varname] = orders
        output = nodelist.render(context)
        context.pop()
        return output

register.tag(UsersOrder)
