from ..models import *


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


class Cross(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cross_product", null=True, blank=True)
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="cross_brand", null=True, blank=True)
    article_nr = models.CharField(max_length=500, null=True, blank=True)
    search_nr = models.CharField(max_length=500, null=True, blank=True)
    product = models.CharField(max_length=500, null=True, blank=True)
    brand = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.article_nr

    class Meta:
        verbose_name = "Cross"
        verbose_name_plural = "Crosses"


class ProductApplicability(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="applicability_product", null=True, blank=True)
    vehicle = models.CharField(max_length=250, null=True, blank=True)
    modification = models.CharField(max_length=250, null=True, blank=True)
    engine = models.CharField(max_length=250, null=True, blank=True)
    year = models.CharField(max_length=250, null=True, blank=True)
    product = models.CharField(max_length=500, null=True, blank=True)

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
    product = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "ProductDescription"
        verbose_name_plural = "ProductDescriptions"


class Price(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="price_product", null=True, blank=True)
    price_type_id = models.ForeignKey(
        PriceType, on_delete=models.CASCADE, related_name="price_price_type", null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="price_currency", null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=0)
    product = models.CharField(max_length=300, null=True, blank=True)
    price_type = models.CharField(max_length=300, null=True, blank=True)
    currency = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.price

    class Meta:
        verbose_name = "Price"
        verbose_name_plural = "Prices"


class Stock(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stock_product", null=True, blank=True)
    stock_name = models.CharField(max_length=300, default='Stock')
    amount_total = models.IntegerField(default=0, null=True)
    amount_account = models.IntegerField(default=0, null=True)
    product = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.amount_account

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"


class DeficitReserve(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="deficit_product", null=True, blank=True)
    sale_policy = models.CharField(max_length=250, null=True, blank=True)
    amount = models.IntegerField(default=0, null=True)
    product = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.amount

    class Meta:
        verbose_name = "DeficitReserve"
        verbose_name_plural = "DeficitReserves"


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

