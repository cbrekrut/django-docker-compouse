from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет обычного пользователя с email и паролем.
        """
        if not email:
            raise ValueError("Email должен быть установлен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет суперпользователя.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email               = models.EmailField(_("email address"), unique=True)
    first_name          = models.CharField(_("first name"), max_length=150, blank=True)
    last_name           = models.CharField(_("last name"), max_length=150, blank=True)
    is_staff            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    date_joined        = models.DateTimeField(default=timezone.now)

    # Ваши поля подписки/платежей
    is_subscribed       = models.BooleanField(default=False)
    subscription_start  = models.DateTimeField(null=True, blank=True)
    subscription_end    = models.DateTimeField(null=True, blank=True)
    payment_profile     = models.CharField(
        max_length=255,
        blank=True,
        help_text="ID платёжного профиля (например, Stripe customer ID)"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class ScreenType(models.Model):
    name = models.CharField("Тип экрана", max_length=100)

    def __str__(self):
        return self.name

class AppCategory(models.Model):
    name = models.CharField("Категория приложения", max_length=100)

    def __str__(self):
        return self.name

class UIElement(models.Model):
    name = models.CharField("UI-элемент", max_length=100)

    def __str__(self):
        return self.name
    
class OSCategory(models.Model):
    name = models.CharField("ОС", max_length=20, unique=True)

    def __str__(self):
        return self.name

    
from django.db import models
from django.utils.safestring import mark_safe

from django.db import models
from django.utils.text import slugify
from django.utils.safestring import mark_safe

class App(models.Model):
    title = models.CharField("Название", max_length=255)
    slug = models.SlugField("URL-адрес", max_length=255, unique=True, blank=True)

    main_image = models.ImageField("Главная картинка", upload_to='apps/main/')
    icon = models.ImageField("Иконка", upload_to='apps/icons/')

    app_category = models.ForeignKey(AppCategory, verbose_name="Категория приложения", on_delete=models.SET_NULL, null=True, blank=True)
    os_category = models.ForeignKey(OSCategory, verbose_name="Категория OS", on_delete=models.SET_NULL, null=True, blank=True)
    screen_type = models.ForeignKey(ScreenType, verbose_name="Тип экрана", on_delete=models.SET_NULL, null=True, blank=True)
    ui_element = models.ForeignKey(UIElement, verbose_name="UI элемент", on_delete=models.SET_NULL, null=True, blank=True)

    screen = models.BooleanField("Экраны", default=False)
    animation = models.BooleanField("Анимации", default=False)

    def __str__(self):
        return self.title

    def main_image_preview(self):
        if self.main_image:
            return mark_safe(f'<img src="{self.main_image.url}" width="100" />')
        return "-"
    main_image_preview.short_description = "Превью фото"

    def icon_preview(self):
        if self.icon:
            return mark_safe(f'<img src="{self.icon.url}" width="50" />')
        return "-"
    icon_preview.short_description = "Превью иконки"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class AppImage(models.Model):
    app = models.ForeignKey('App', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField("Фото", upload_to='apps/photos/')

    def __str__(self):
        return f"Фото для {self.app.title}"

class AppVideo(models.Model):
    app = models.ForeignKey('App', on_delete=models.CASCADE, related_name='videos')
    video = models.FileField("Видео", upload_to='apps/videos/')

    def __str__(self):
        return f"Видео для {self.app.title}"