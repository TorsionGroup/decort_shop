from django.db import models
from datetime import datetime
from django.core.mail import send_mail
from creditcards.models import CardNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager()


class Manager(models.Model):
    inner_name = models.CharField(max_length=250)
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    skype = models.CharField(max_length=250, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    source_id = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.inner_name

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"


class Customer(models.Model):
    code = models.CharField(max_length=250, null=True)
    name = models.CharField(max_length=300)
    main_customer_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    manager_id = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, related_name="customer_manager", null=True, blank=True)
    sale_policy = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    region_id = models.IntegerField(null=True, blank=True)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    no_show_balance = models.BooleanField(default=0)
    deficit_available = models.BooleanField(default=0)
    online_reserve = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, phone, password, **extra_fields):
        values = [email, username, phone]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_username, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_username))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, phone, password, **extra_fields)

    def create_superuser(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, phone, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=250)
    phone = PhoneNumberField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    picture = models.ImageField(upload_to="content/account_image/", blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username.split()[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=300)
    enabled = models.BooleanField(default=1)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    wait_list = models.BooleanField(default=0)
    is_recommended = models.BooleanField(default=0)
    sort_index = models.IntegerField(default=999)
    source_type = models.CharField(max_length=250, default='1C')
    gallery_attribute = models.CharField(max_length=250, default='article')
    gallery_name = models.CharField(max_length=250, null=True, blank=True)
    kind = models.CharField(max_length=250, default='secondary')
    brand_image = models.ImageField(upload_to="content/brand_image/", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class PriceCategory(models.Model):
    inner_name = models.CharField(max_length=250, default='PriceCategory')
    source_id = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.inner_name

    class Meta:
        verbose_name = "PriceCategory"
        verbose_name_plural = "PriceCategories"


class CatalogCategory(MPTTModel):
    parent_id = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    source_id = models.CharField(max_length=300, null=True, blank=True)
    enabled = models.BooleanField(default=1)
    sort_index = models.IntegerField(default=999)
    content_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=500)
    comment = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CatalogCategory"
        verbose_name_plural = "CatalogCategories"

    class MPTTMeta:
        order_insertion_by = ['name']


class Offer(models.Model):
    name = models.CharField(max_length=300, default='Offer')
    group = models.CharField(max_length=300, null=True, blank=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    source_id = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"


class Product(models.Model):
    specification = models.CharField(max_length=250, null=True)
    article = models.CharField(max_length=250, null=True)
    brand_id = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    offer_id = models.ForeignKey(
        Offer, on_delete=models.SET_NULL, blank=True, null=True)
    category_id = models.ForeignKey(
        CatalogCategory, on_delete=models.SET_NULL, blank=True, null=True)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    search_key = models.CharField(max_length=250, null=True, blank=True)
    sort_price = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    is_active = models.BooleanField(default=1)
    weight = models.DecimalField(max_digits=15, decimal_places=3, default=0, blank=True)
    pack_qty = models.IntegerField(default=0, blank=True)
    ABC = models.CharField(max_length=1, null=True, blank=True)
    is_exists = models.BooleanField(default=0)
    code = models.CharField(max_length=250, null=True, blank=True)
    source_type = models.CharField(max_length=250, default='1C', null=True, blank=True)
    price_category = models.ForeignKey(PriceCategory, on_delete=models.SET_NULL, blank=True, null=True)
    product_type = models.IntegerField(null=True, blank=True)
    delete_flag = models.BooleanField(default=0)
    advanced_description = models.TextField("Advanced description", null=True, blank=True)
    name = models.CharField(max_length=500, default='Product')
    comment = models.CharField(max_length=500, null=True, blank=True)
    keywords = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'int': self.id})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(models.Model):
    name = models.CharField(max_length=250, default='ProductImage')
    description = models.TextField(null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="product/product_image/", null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"


class CartProduct(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, verbose_name='cartproduct_account')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='cartproduct_cart',
                             related_name='related_cartproduct_cart')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='cartproduct_finalprice')

    def __str__(self):
        return "Product: {} (for cart)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "CartProduct"
        verbose_name_plural = "CartProducts"


class Cart(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, verbose_name='cart_account')
    product = models.ManyToManyField(CartProduct, blank=True, verbose_name='cart_cartproduct',
                                     related_name='related_cart_product')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='cart_finalprice')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class Currency(models.Model):
    code = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    rate = models.DecimalField(max_digits=15, decimal_places=5)
    mult = models.IntegerField()
    name_eng = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


class PriceType(models.Model):
    name = models.CharField(max_length=300)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    enabled = models.BooleanField(default=1)
    sort_index = models.IntegerField(default=999, null=True)
    access_policy_data = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "PriceType"
        verbose_name_plural = "PriceTypes"


class CustomerAgreement(models.Model):
    code = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250)
    number = models.CharField(max_length=250, null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="agreement_customer", null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="agreement_currency", null=True, blank=True)
    price_type_id = models.ForeignKey(
        PriceType, on_delete=models.CASCADE, related_name="agreement_price_type", null=True, blank=True)
    is_status = models.BooleanField()
    discount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=1)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    api_available = models.BooleanField(default=0)
    api_token = models.CharField(max_length=250, null=True, blank=True)
    api_user_id = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CustomerAgreement"
        verbose_name_plural = "CustomerAgreements"


class CustomerCard(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="card_customer", null=True, blank=True)
    name = models.CharField(max_length=250)
    card = CardNumberField()

    def __str__(self):
        return self.card

    class Meta:
        verbose_name = "CustomerCard"
        verbose_name_plural = "CustomerCard"


class CustomerContact(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="contact_customer", null=True, blank=True)
    user_id = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=250)
    email = models.EmailField(null=True, blank=True)
    is_user = models.BooleanField(default=1)
    source_id = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CustomerContact"
        verbose_name_plural = "CustomerContacts"


class CustomerDiscount(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="discount_customer_customer", null=True, blank=True)
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.CASCADE, related_name="discount_customer_agreement", null=True, blank=True)
    criteria_id = models.IntegerField(null=True, blank=True)
    criteria_type = models.CharField(max_length=250, null=True, blank=True)
    discount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    price_type_id = models.ForeignKey(
        PriceType, on_delete=models.CASCADE, related_name="discount_customer_price_type", null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "CustomerDiscount"
        verbose_name_plural = "CustomerDiscounts"


class CustomerPoint(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="point_customer", null=True, blank=True)
    name = models.CharField(max_length=500)
    source_id = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CustomerPoint"
        verbose_name_plural = "CustomerPoints"


class Balance(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="balance_customer", null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="balance_currency", null=True, blank=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    past_due = models.DecimalField(max_digits=15, decimal_places=2)
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.CASCADE, related_name="balance_agreement", null=True, blank=True)

    def __str__(self):
        return self.balance

    class Meta:
        verbose_name = "Balance"
        verbose_name_plural = "Balances"


class Price(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="price_product", null=True, blank=True)
    price_type_id = models.ForeignKey(
        PriceType, on_delete=models.CASCADE, related_name="price_price_type", null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="price_currency", null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.price

    class Meta:
        verbose_name = "Price"
        verbose_name_plural = "Prices"


class PriceBuffer(models.Model):
    code = models.CharField(max_length=250)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="price_buffer_brand", null=True, blank=True)
    category = models.CharField(max_length=250, null=True, blank=True)
    price_category = models.ForeignKey(
        PriceCategory, on_delete=models.CASCADE, related_name="price_buffer_price_category", null=True, blank=True)
    specification = models.CharField(max_length=250, null=True, blank=True)
    article = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=250, null=True, blank=True)
    rest = models.IntegerField(null=True, blank=True)
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.CASCADE, related_name="price_buffer_agreement", null=True, blank=True)
    sort_index = models.CharField(max_length=300, null=True, blank=True)
    pack_qty = models.IntegerField(null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "PriceBuffer"
        verbose_name_plural = "PriceBuffers"


class Stock(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stock_product", null=True, blank=True)
    stock_name = models.CharField(max_length=300, default='Stock')
    amount_total = models.IntegerField(default=0)
    amount_account = models.IntegerField(default=0)

    def __str__(self):
        return self.amount_account

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"


class Category(models.Model):
    name = models.CharField(max_length=300)
    comment = models.CharField(max_length=500, null=True, blank=True)
    url = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Constant(models.Model):
    code = models.CharField(max_length=250)
    value = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Constant"
        verbose_name_plural = "Constant"


class Content(models.Model):
    alias = models.SlugField(max_length=300, unique=True)
    created_date = models.DateTimeField(default=datetime.today)
    updated_date = models.DateTimeField(default=datetime.today)
    published = models.BooleanField(default=0)
    main_image = models.ImageField(upload_to="content/main_image/", blank=True, null=True)
    category_id = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="content_category", null=True, blank=True)
    title = models.CharField(max_length=500, null=True)
    intro_text = models.CharField(max_length=1000, null=True)
    full_text = models.TextField(null=True)
    meta_tag_title = models.CharField(max_length=500, null=True, blank=True)
    meta_tag_description = models.CharField(max_length=500, null=True, blank=True)
    meta_tag_keyword = models.CharField(max_length=500, null=True, blank=True)
    geo = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.alias

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={"slug": self.alias})

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Contents"


class ContentImage(models.Model):
    name = models.CharField(max_length=250, default='ContentImage')
    description = models.TextField(null=True, blank=True)
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="content/content_image/", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ContentImage"
        verbose_name_plural = "ContentImages"


class Cross(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cross_product", null=True, blank=True)
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="cross_brand", null=True, blank=True)
    article_nr = models.CharField(max_length=500, null=True, blank=True)
    search_nr = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.article_nr

    class Meta:
        verbose_name = "Cross"
        verbose_name_plural = "Crosses"


class CrossErrorStatistic(models.Model):
    user_id = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cross_error_product", null=True, blank=True)
    search_number = models.CharField(max_length=1000)
    comment = models.CharField(max_length=500, null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="cross_error_customer", null=True, blank=True)
    date = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.search_number

    class Meta:
        verbose_name = "CrossErrorStatistic"
        verbose_name_plural = "CrossErrorStatistics"


class ProductApplicability(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="applicability_product", null=True, blank=True)
    vehicle = models.CharField(max_length=250, null=True, blank=True)
    modification = models.CharField(max_length=250, null=True, blank=True)
    engine = models.CharField(max_length=250, null=True, blank=True)
    year = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "ProductApplicability"
        verbose_name_plural = "ProductApplicabilitys"


class ProductDescription(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="description_product", null=True, blank=True)
    property = models.CharField(max_length=500, null=True, blank=True)
    value = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "ProductDescription"
        verbose_name_plural = "ProductDescriptions"


class ProductErrorStatistic(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_error_product", null=True, blank=True)
    user_id = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    error_comment = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=250)
    created_date = models.DateTimeField(default=datetime.today)
    updated_date = models.DateTimeField(default=datetime.today)
    admin_comment = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "ProductErrorStatistic"
        verbose_name_plural = "ProductErrorStatistics"


class DeficitReserve(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="deficit_product", null=True, blank=True)
    sale_policy = models.CharField(max_length=250, null=True, blank=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.amount

    class Meta:
        verbose_name = "DeficitReserve"
        verbose_name_plural = "DeficitReserves"


class Region(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"


class DeliveryMethod(models.Model):
    code = models.CharField(max_length=250, null=True, blank=True)
    region_available = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=250)
    comment = models.TextField(null=True, blank=True)
    red = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DeliveryMethod"
        verbose_name_plural = "DeliveryMethods"


class DeliveryService(models.Model):
    name = models.CharField(max_length=250)
    has_to_door = models.BooleanField(default=0)
    parameters = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DeliveryService"
        verbose_name_plural = "DeliveryService"


class DeliveryCity(models.Model):
    service_id = models.ForeignKey(
        DeliveryService, on_delete=models.CASCADE, related_name="city_service", null=True, blank=True)
    region = models.CharField(max_length=250, null=True, blank=True)
    ref = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250)
    create_date = models.DateTimeField(default=datetime.today)
    update_date = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DeliveryCity"
        verbose_name_plural = "DeliveryCities"


class DeliveryPoint(models.Model):
    service_id = models.ForeignKey(
        DeliveryService, on_delete=models.CASCADE, related_name="point_service", null=True, blank=True)
    city_id = models.ForeignKey(
        DeliveryCity, on_delete=models.CASCADE, related_name="point_city", null=True, blank=True)
    street = models.CharField(max_length=250, null=True, blank=True)
    ref = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250)
    longitude = models.CharField(max_length=250, null=True, blank=True)
    latitude = models.CharField(max_length=250, null=True, blank=True)
    max_weight = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DeliveryPoint"
        verbose_name_plural = "DeliveryPoints"


class PartnerApi(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=250, null=True, blank=True)
    token = models.CharField(max_length=250, null=True, blank=True)
    margin = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    percent_prepayment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    show_branch = models.BooleanField(default=1)
    enabled = models.BooleanField(default=0)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "PartnerApi"
        verbose_name_plural = "PartnerApis"


class CacheApi(models.Model):
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="cache_partner", null=True, blank=True)
    search_number = models.CharField(max_length=250)
    response_api = models.TextField(null=True, blank=True)
    response_date = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.search_number

    class Meta:
        verbose_name = "CacheApi"
        verbose_name_plural = "CacheApis"


class PartnerApiCache(models.Model):
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="apicache_partner", null=True, blank=True)
    search_number = models.CharField(max_length=250, null=True, blank=True)
    response_date = models.DateTimeField(default=datetime.today)
    product_json = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.search_number

    class Meta:
        verbose_name = "PartnerApiCache"
        verbose_name_plural = "PartnerApiCaches"


class PartnerCategory(models.Model):
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="category_partner", null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, default=0, null=True)
    response_date = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "PartnerCategory"
        verbose_name_plural = "PartnerCategories"


class CategoryMapping(models.Model):
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="mapping_partner", null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    category_id = models.ForeignKey(
        PartnerCategory, on_delete=models.CASCADE, related_name="mapping_category", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CategoryMapping"
        verbose_name_plural = "CategoryMappings"


class PartnerCategoryCache(models.Model):
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="category_cache_partner", null=True, blank=True)
    category_id = models.ForeignKey(
        PartnerCategory, on_delete=models.CASCADE, related_name="category_cache_category", null=True, blank=True)
    response_date = models.DateTimeField(default=datetime.today)
    product_json = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.response_date

    class Meta:
        verbose_name = "PartnerCategoryCache"
        verbose_name_plural = "PartnerCategoryCaches"


class PartnerStock(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_partner", null=True, blank=True)
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="stock_partner", null=True, blank=True)
    branch = models.CharField(max_length=250, null=True, blank=True)
    qty = models.IntegerField(default=0)
    supply_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.qty

    class Meta:
        verbose_name = "PartnerStock"
        verbose_name_plural = "PartnerStocks"


class ProductApiMap(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_api_map", null=True, blank=True)
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="partner_api_map", null=True, blank=True)
    api_key = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.partner_code

    class Meta:
        verbose_name = "ProductApiMap"
        verbose_name_plural = "ProductApiMaps"


class Order(models.Model):
    user_id = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.SET_NULL, related_name="order_agreement", null=True, blank=True)
    complete = models.BooleanField(default=0)
    delivery_method = models.ForeignKey(
        DeliveryMethod, on_delete=models.SET_NULL, related_name="order_delivery", null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.today)
    update_date = models.DateTimeField(default=datetime.today)
    comment = models.TextField(null=True, blank=True)
    point_id = models.ForeignKey(
        CustomerPoint, on_delete=models.SET_NULL, related_name="order_customer_point", null=True, blank=True)
    delivery_service_id = models.ForeignKey(
        DeliveryService, on_delete=models.SET_NULL, related_name="order_del_point", null=True, blank=True)
    delivery_city_id = models.ForeignKey(
        DeliveryCity, on_delete=models.SET_NULL, related_name="order_del_city", null=True, blank=True)
    delivery_point_id = models.ForeignKey(
        DeliveryPoint, on_delete=models.SET_NULL, related_name="order_del_point", null=True, blank=True)
    delivery_contact = models.CharField(max_length=250, null=True, blank=True)
    delivery_contact_phone = PhoneNumberField(blank=True)
    order_number = models.CharField(max_length=250, null=True, blank=True)
    waybill_number = models.CharField(max_length=250, null=True, blank=True)
    invoice_number = models.CharField(max_length=250, null=True, blank=True)
    source = models.CharField(max_length=250, default='site', null=True)
    is_pay_on_delivery = models.BooleanField(default=0)
    pay_on_delivery_sum = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    import_reason = models.TextField(null=True, blank=True)
    import_status = models.CharField(max_length=250, null=True, blank=True)
    partner_code = models.CharField(max_length=250, null=True, blank=True)
    declared_sum = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    declared_currency = models.BooleanField(default=1)
    source_type = models.CharField(max_length=250, default='B2B', null=True)
    delivery_contact_surname = models.CharField(max_length=250, null=True)
    declaration_number = models.CharField(max_length=250, null=True, blank=True)
    delivery_contact_middlename = models.CharField(max_length=250, null=True, blank=True)
    delivery_is_invoice_off = models.BooleanField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_item_order", null=True, blank=True)
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_item_product", null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="order_item_currency", null=True, blank=True)
    qty = models.IntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    source = models.CharField(max_length=250, null=True, blank=True)
    reserved = models.IntegerField(null=True, blank=True)
    executed = models.IntegerField(null=True, blank=True)
    old_qty = models.IntegerField(null=True, blank=True)
    old_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    update_date = models.DateTimeField(null=True, blank=True)
    purchase_qty = models.IntegerField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchase_currency_id = models.IntegerField(null=True, blank=True)
    purchase_order_id = models.IntegerField(null=True, blank=True)
    purchase_item_id = models.IntegerField(null=True, blank=True)
    partner_branch = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.product_id.sort_price * self.qty
        return total

    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"


class OrderPayment(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_payment_order", null=True, blank=True)
    sum = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    date_payment = models.DateTimeField(default=datetime.today)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="order_payment_currency", null=True, blank=True)
    payment_sum = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    receiver_commission = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sender_commission = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.order_id

    class Meta:
        verbose_name = "OrderPayment"
        verbose_name_plural = "OrderPayments"


class OrderSourceStatistic(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_statistic_product", null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="order_statistic_customer", null=True, blank=True)
    source_type = models.CharField(max_length=250, null=True, blank=True)
    add_date = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "OrderSourceStatistic"
        verbose_name_plural = "OrderSourceStatistics"


class DropshippingWallet(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="d_wallet_order", null=True, blank=True)
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.CASCADE, related_name="d_wallet_agreement", null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="d_wallet_currency", null=True, blank=True)
    debit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    credit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.order_id

    class Meta:
        verbose_name = "DropshippingWallet"
        verbose_name_plural = "DropshippingWallets"


class DropshippingWalletTransfer(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="d_transfer_order", null=True, blank=True)
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.CASCADE, related_name="d_transfer_agreement", null=True, blank=True)
    sum = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="d_transfer_currency", null=True, blank=True)
    date = models.DateTimeField(default=datetime.today)
    card = CardNumberField(null=True, blank=True)

    def __str__(self):
        return self.order_id

    class Meta:
        verbose_name = "DropshippingWalletTransfer"
        verbose_name_plural = "DropshippingWalletTransfers"


class PromoSale(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="promo_sale_customer", null=True, blank=True)
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="promo_sale_product", null=True, blank=True)
    type = models.CharField(max_length=300, null=True, blank=True)
    is_visible = models.BooleanField(default=0)
    comment = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "PromoSale"
        verbose_name_plural = "PromoSales"


class RunString(models.Model):
    created_date = models.DateTimeField(default=datetime.today)
    updated_date = models.DateTimeField(default=datetime.today)
    full_text = models.CharField(max_length=1000)
    comment = models.CharField(max_length=500, null=True, blank=True)
    published = models.BooleanField(default=0)

    def __str__(self):
        return self.full_text

    class Meta:
        verbose_name = "RunString"
        verbose_name_plural = "RunStrings"


class Sale(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sale_product", null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="sale_customer", null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"


class SaleHistory(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sale_history_product", null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="sale_history_customer", null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "SaleHistory"
        verbose_name_plural = "SaleHistories"


class SaleProductRelated(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sale_related_product", null=True, blank=True)
    related_product_id = models.IntegerField(null=True, blank=True)
    qty_index = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    calculation_type = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "SaleProductRelated"
        verbose_name_plural = "SaleProductRelateds"


class SaleTask(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sale_task_product", null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="sale_task_customer", null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "SaleTask"
        verbose_name_plural = "SaleTasks"


class ScenarioPolicy(models.Model):
    sale_policy = models.CharField(max_length=250, null=True, blank=True)
    deficit_available = models.BooleanField(default=0, null=True)
    online_reserve = models.BooleanField(default=0, null=True)
    online_order = models.BooleanField(default=0, null=True)

    def __str__(self):
        return self.sale_policy

    class Meta:
        verbose_name = "ScenarioPolicy"
        verbose_name_plural = "ScenarioPolicies"


class SearchRequest(models.Model):
    user_id = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    search_keyword = models.CharField(max_length=250, null=True, blank=True)
    search_keyword_clean = models.CharField(max_length=250, null=True, blank=True)
    is_result = models.BooleanField(default=0, null=True)
    product_list = models.TextField(null=True, blank=True)
    is_added_in_cart = models.BooleanField(default=0, null=True)
    product_add_in_cart = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.search_keyword

    class Meta:
        verbose_name = "ScenarioPolicy"
        verbose_name_plural = "ScenarioPolicies"


class SearchRequestBufferIgnore(models.Model):
    search_keyword_clean = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.search_keyword_clean

    class Meta:
        verbose_name = "SearchRequestBufferIgnore"
        verbose_name_plural = "SearchRequestBufferIgnores"


class SendPriceBuffer(models.Model):
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.CASCADE, related_name="send_price_buffer_agreement", null=True, blank=True)
    price_email = models.CharField(max_length=250, null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="send_price_buffer_customer", null=True, blank=True)

    def __str__(self):
        return self.agreement_id

    class Meta:
        verbose_name = "SendPriceBuffer"
        verbose_name_plural = "SendPriceBuffers"


class Token(models.Model):
    user_id = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=datetime.today)
    type = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"


class UploadProduct(models.Model):
    upload_id = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(default=datetime.today)
    name = models.CharField(max_length=300, null=True, blank=True)
    article = models.CharField(max_length=300, null=True, blank=True)
    search_key = models.CharField(max_length=300, null=True, blank=True)
    category = models.CharField(max_length=300, null=True, blank=True)
    brand = models.CharField(max_length=300, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    branch = models.CharField(max_length=300, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    supply = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.upload_id

    class Meta:
        verbose_name = "UploadProduct"
        verbose_name_plural = "UploadProducts"


class UploadSetting(models.Model):
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="upload_setting_partner", null=True, blank=True)
    file_name = models.CharField(max_length=250, null=True, blank=True)
    first_row = models.IntegerField(null=True, blank=True)
    mapping = models.TextField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    rate = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    encoding = models.CharField(max_length=250, null=True, blank=True)
    compare_name = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.partner_code

    class Meta:
        verbose_name = "UploadSetting"
        verbose_name_plural = "UploadSettings"


class UserRequest(models.Model):
    user_id = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=250, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    request_type_id = models.IntegerField(null=True, blank=True)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    checked = models.BooleanField(default=0)
    date_request = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "UserRequest"
        verbose_name_plural = "UserRequests"


class UserRequestType(models.Model):
    manager_id = models.ForeignKey(
        Manager, on_delete=models.CASCADE, related_name="user_request_manager", null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    comment = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "UserRequestType"
        verbose_name_plural = "UserRequestTypes"


class WaitList(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wait_list_product", null=True, blank=True)
    user_id = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    date_add = models.DateTimeField(default=datetime.today)
    send_message = models.BooleanField(default=0)
    is_active = models.BooleanField(default=0)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "WaitList"
        verbose_name_plural = "WaitLists"


class Action(models.Model):
    content_id = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="action_content", null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    start_at = models.DateTimeField(default=datetime.today)
    finish_at = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.content_id

    class Meta:
        verbose_name = "Action"
        verbose_name_plural = "Actions"


class ActionCustomer(models.Model):
    action_id = models.ForeignKey(
        Action, on_delete=models.CASCADE, related_name="action_customer_action", null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="action_customer_customer", null=True, blank=True)
    win = models.BooleanField(default=0)
    close_action = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.action_id

    class Meta:
        verbose_name = "ActionCustomer"
        verbose_name_plural = "ActionCustomers"


class ActionProduct(models.Model):
    action_id = models.ForeignKey(
        Action, on_delete=models.CASCADE, related_name="action_product_action", null=True, blank=True)
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="action_product_product", null=True, blank=True)

    def __str__(self):
        return self.action_id

    class Meta:
        verbose_name = "ActionProduct"
        verbose_name_plural = "ActionProducts"


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "RatingStar"
        verbose_name_plural = "RatingStars"
        ordering = ["-value"]


class RatingProduct(models.Model):
    ip = models.CharField(max_length=50)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "RatingProduct"
        verbose_name_plural = "RatingProducts"


class ReviewProduct(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=250)
    text = models.TextField(max_length=5000)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name = "ReviewProduct"
        verbose_name_plural = "ReviewProducts"


class RatingContent(models.Model):
    ip = models.CharField(max_length=50)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.content}"

    class Meta:
        verbose_name = "RatingContent"
        verbose_name_plural = "RatingContents"


class ReviewContent(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=250)
    text = models.TextField(max_length=5000)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.content}"

    class Meta:
        verbose_name = "ReviewContent"
        verbose_name_plural = "ReviewContents"
