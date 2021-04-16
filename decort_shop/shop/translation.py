from modeltranslation.translator import register, TranslationOptions
from .models import Product, CatalogCategory, Category, Content, Manager, RunString


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'comment')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'comment', 'keywords')


@register(CatalogCategory)
class CatalogCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'comment')


@register(Manager)
class ManagerMethodTranslationOptions(TranslationOptions):
    fields = ('name', 'comment')


@register(RunString)
class RunStringMethodTranslationOptions(TranslationOptions):
    fields = ('full_text', 'comment')


@register(Content)
class ContentTypeMethodTranslationOptions(TranslationOptions):
    fields = ('title', 'intro_text', 'full_text', 'meta_tag_title', 'meta_tag_description', 'meta_tag_keyword')

