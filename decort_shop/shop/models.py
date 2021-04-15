from django.db import models
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from .customers.models import Customer


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

