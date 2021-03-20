from django import template
from shop.models import *

register = template.Library()


def list_categories(request):
    return {'menu_categories': CatalogCategory.objects.all()}


@register.simple_tag()
def get_catalogcategories():
    return CatalogCategory.objects.filter(parent_id=None)


@register.inclusion_tag('decort_shop/news/last_news.html')
def get_last_news(count=5):
    news = Content.objects.filter(category_id=2).order_by("id")[:count]
    return {'last_news': news}
