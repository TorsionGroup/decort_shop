from django.db import models
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from creditcards.models import CardNumberField


class Currency(models.Model):
    code = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    rate = models.DecimalField(max_digits=15, decimal_places=2)
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "PriceType"
        verbose_name_plural = "PriceTypes"


class Manager(models.Model):
    inner_name = models.CharField(max_length=250)
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    skype = models.CharField(max_length=250, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    source_id = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=0, blank=True, null=True)

    def __str__(self):
        return self.inner_name

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"


class Customer(models.Model):
    code = models.CharField(max_length=250, null=True)
    name = models.CharField(max_length=300)
    main_customer_id = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    manager_id = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, related_name="customer_manager", null=True, blank=True)
    sale_policy = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    region_id = models.CharField(max_length=300, null=True, blank=True)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    no_show_balance = models.BooleanField(default=0, null=True)
    deficit_available = models.BooleanField(default=0, null=True)
    online_reserve = models.BooleanField(default=0, null=True)
    main_customer = models.CharField(max_length=300, null=True, blank=True)
    manager = models.CharField(max_length=300, null=True, blank=True)

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
    phone = models.CharField(max_length=250, blank=True, null=True)
    date_of_birth = models.CharField(max_length=250, blank=True, null=True)
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
    enabled = models.BooleanField(default=1, null=True, blank=True)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    wait_list = models.BooleanField(default=0, null=True, blank=True)
    is_recommended = models.BooleanField(default=0, null=True, blank=True)
    sort_index = models.IntegerField(default=999, null=True, blank=True)
    source_type = models.CharField(max_length=250, default='1C', null=True)
    gallery_attribute = models.CharField(max_length=250, default='article', null=True, blank=True)
    gallery_name = models.CharField(max_length=250, null=True, blank=True)
    kind = models.CharField(max_length=250, default='secondary', null=True, blank=True)
    brand_image = models.ImageField(upload_to="content/brand_image/", blank=True, null=True)
    supplier_id = models.CharField(max_length=300, null=True, blank=True)

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
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    source_id = models.CharField(max_length=300, null=True, blank=True)
    enabled = models.BooleanField(default=0, null=True)
    sort_index = models.IntegerField(default=999, null=True, blank=True)
    content_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=500, null=True, default='Catalog')
    comment = models.CharField(max_length=500, null=True, blank=True)
    parent_source = models.CharField(max_length=500, null=True, blank=True)
    url = models.SlugField(max_length=150, unique=True)
    image = models.ImageField(upload_to="product/category_image/", null=True, blank=True)

    def __str__(self):
        return str(self.url)

    def get_absolute_url(self):
        return reverse('catalog_category_detail', kwargs={'slug': self.url})

    class Meta:
        verbose_name = "CatalogCategory"
        verbose_name_plural = "CatalogCategories"

    class MPTTMeta:
        order_insertion_by = ['name']


class Offer(models.Model):
    name = models.CharField(max_length=300, default='Offer')
    group_name = models.CharField(max_length=300, null=True, blank=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    is_recommended = models.BooleanField(default=0, null=True, blank=True)

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
        CatalogCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='category_id')
    source_id = models.CharField(max_length=300, null=True, blank=True)
    search_key = models.CharField(max_length=250, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True)
    is_active = models.BooleanField(default=1, null=True)
    weight = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    pack_qty = models.IntegerField(default=0, blank=True, null=True)
    abc = models.CharField(max_length=300, null=True, blank=True)
    is_exists = models.BooleanField(default=0, null=True)
    code = models.CharField(max_length=250, null=True, blank=True)
    source_type = models.CharField(max_length=250, default='1C', null=True)
    price_category_id = models.ForeignKey(PriceCategory, on_delete=models.SET_NULL, blank=True, null=True)
    product_type = models.IntegerField(null=True, blank=True)
    delete_flag = models.BooleanField(default=0, null=True)
    advanced_description = models.TextField("Advanced description", null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    comment = models.CharField(max_length=500, null=True, blank=True)
    keywords = models.CharField(max_length=500, null=True, blank=True)
    brand = models.CharField(max_length=300, null=True, blank=True)
    offer = models.CharField(max_length=300, null=True, blank=True)
    category = models.CharField(max_length=300, null=True, blank=True)
    price_category = models.CharField(max_length=300, null=True, blank=True)
    manufacturer_name = models.CharField(max_length=300, null=True, blank=True)
    model_name = models.CharField(max_length=300, null=True, blank=True)
    create_date = models.CharField(max_length=300, null=True, blank=True)
    income_date = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'int': self.id})

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


class Constant(models.Model):
    code = models.CharField(max_length=250)
    value = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Constant"
        verbose_name_plural = "Constant"


class Category(models.Model):
    name = models.CharField(max_length=300)
    comment = models.CharField(max_length=500, null=True, blank=True)
    url = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Content(models.Model):
    alias = models.SlugField(max_length=300, unique=True)
    created_date = models.DateTimeField(default=datetime.today, null=True)
    updated_date = models.DateTimeField(default=datetime.today, null=True)
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


class RunString(models.Model):
    created_date = models.DateTimeField(default=datetime.today, null=True)
    updated_date = models.DateTimeField(default=datetime.today, null=True)
    full_text = models.CharField(max_length=1000)
    comment = models.CharField(max_length=500, null=True, blank=True)
    published = models.BooleanField(default=0)

    def __str__(self):
        return self.full_text

    class Meta:
        verbose_name = "RunString"
        verbose_name_plural = "RunStrings"


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "RatingStar"
        verbose_name_plural = "RatingStars"
        ordering = ["-value"]


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

