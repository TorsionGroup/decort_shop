from django import template
from shop.models import *

register = template.Library()


@register.simple_tag()
def get_catalogcategories():
    return CatalogCategory.objects.filter(enabled=True)


@register.simple_tag()
def get_currency():
    return Currency.objects.filter(id=1)


@register.inclusion_tag('decort_shop/news/last_news.html')
def get_last_news(count=5):
    news = Content.objects.filter(category_id=2).order_by("id")[:count]
    return {'last_news': news}

