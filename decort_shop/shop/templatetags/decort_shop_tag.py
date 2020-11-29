from django import template
from shop.models import CatalogCategory, Content, Brand, Offer

register = template.Library()


@register.simple_tag()
def get_catalogcategories():
    return CatalogCategory.objects.all()


@register.inclusion_tag('decort_shop/tags/last_news.html')
def get_last_news(count=5):
    news = Content.objects.filter(category_id=2).order_by("id")[:count]
    return {'last_news': news}
