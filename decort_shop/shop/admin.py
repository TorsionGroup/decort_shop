from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from modeltranslation.admin import TranslationAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import *
from .forms import UserCreationForm, UserChangeForm


admin.site.site_title = 'Torsion Group B2B'
admin.site.site_header = 'Torsion Group B2B'


class ContentAdminForm(forms.ModelForm):
    full_text_ru = forms.CharField(widget=CKEditorUploadingWidget())
    full_text_uk = forms.CharField(widget=CKEditorUploadingWidget())
    full_text_en = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Content
        fields = '__all__'


admin.site.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'comment', 'url')
    list_display_links = ('name',)


admin.site.register(Content)
class ContentAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'alias', 'main_image', 'published')
    list_filter = ('category_id',)
    list_display_links = ('title',)
    readonly_fields = ('get_main_image',)
    save_on_top = True
    form = ContentAdminForm

    def get_main_image(self, obj):
        return mark_safe(f'<img src={obj.main_image.url} widht="50" height="60"')

    get_main_image.short_description = 'image'


admin.site.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sort_index', 'enabled', 'wait_list', 'is_recommended', 'kind', 'enabled')
    list_filter = ('sort_index',)
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'article', 'specification', 'is_active')
    list_display_links = ('name', 'article',)
    search_fields = ('name', 'article',)


admin.site.register(PriceCategory)
class PriceCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'inner_name', 'source_id')
    list_display_links = ('inner_name',)


class ReviewInLine(admin.StackedInline):
    model = ReviewContent, ReviewProduct


admin.site.register(ReviewContent)
class ReviewContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'email', 'content')
    list_display_links = ('name',)
    search_fields = ('name', 'content',)


admin.site.register(ReviewProduct)
class ReviewProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'email', 'product')
    list_display_links = ('name',)
    search_fields = ('name', 'product',)


admin.site.register(RatingStar)


admin.site.register(Account)
class AccountAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'customer_id', 'phone', 'date_of_birth', 'is_staff',  'is_superuser',
                    'is_active')
    list_filter = ('is_superuser',)
    save_on_top = True

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'is_active', 'password')}),
        ('Personal info', {'fields': ('username', 'phone', 'date_of_birth', 'picture')}),
        ('Customers', {'fields': ('customer_id',)}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'is_active', 'password1', 'password2')}),
        ('Personal info', {'fields': ('username', 'phone', 'date_of_birth', 'picture')}),
        ('Customers', {'fields': ('customer_id',)}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email', 'username', 'customer_id', 'phone')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CatalogCategory)
class CatalogCategoryAdmin(TranslationAdmin):
    list_display = ('id', 'parent_id', 'name', 'comment', 'enabled', 'sort_index', 'content_id')
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group', 'title', 'source_id')
    list_display_links = ('name',)


admin.site.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'inner_name')
    list_display_links = ('inner_name',)
    search_fields = ('inner_name',)


admin.site.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'main_customer_id', 'manager_id', 'sale_policy', 'city')
    list_display_links = ('name',)
    search_fields = ('name', 'manager_id',)


admin.site.register(PriceType)
class PriceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(CustomerAgreement)
class CustomerAgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'customer_id', 'code', 'number', 'currency_id')
    list_display_links = ('name', 'customer_id',)
    search_fields = ('name', 'customer_id',)


admin.site.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'agreement_id', 'delivery_method', 'point_id', 'order_number')
    list_display_links = ('id', 'user_id', 'agreement_id', 'delivery_method', 'order_number',)
    search_fields = ('user_id', 'delivery_method', 'order_number',)


admin.site.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'product_id', 'qty', 'price')
    list_display_links = ('order_id', 'product_id', 'qty', 'price',)
    search_fields = ('order_id',)

