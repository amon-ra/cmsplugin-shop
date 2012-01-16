# -*- coding: utf-8 -*-
from django import template
from django.conf import settings


from classytags.core import Tag, Options
from classytags.arguments import Argument

register = template.Library()

def format_currency(value, symbol=None, thousand_sep=None, decimal_sep=None):

    if not symbol:
        symbol = getattr(settings, 'CURRENCY_SYMBOL', '$')

    if not thousand_sep:
        thousand_sep = getattr(settings, 'THOUSAND_SEPARATOR', ',')

    if not decimal_sep:
        decimal_sep = getattr(settings, 'DECIMAL_SEPARATOR', '.')

    intstr = str(int(value))
    f = lambda x, n, acc=[]: f(x[:-n], n, [(x[-n:])]+acc) if x else acc
    intpart = thousand_sep.join(f(intstr, 3))
    return "%s%s%s%s" % (symbol, intpart, decimal_sep, ("%0.2f" % value)[-2:])


@register.filter()
def currency(value):
    return format_currency(value)

@register.tag()
class CurrencyBlockTag(Tag):
    name = 'currency'
    options = Options(
        Argument('symbol', resolve=True, required=False),
        Argument('thousand_sep', resolve=True, required=False),
        Argument('decimal_sep', resolve=True, required=False),
        blocks=[('endcurrency', 'nodelist')],
    )

    def render_tag(self, context, symbol=None,
                   thousand_sep=None,
                   decimal_sep=None,
                   nodelist=None):
        context.push()
        output = nodelist.render(context)
        context.pop()
        try:
            currency_amount = float(output)
            return format_currency(currency_amount)
#                                    symbol=None,
#                                    thousand_sep=None,
#                                    decimal_sep=None)

        except Exception,error:
            return "$"+output
