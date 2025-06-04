from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as AuthUser, Group as AuthGroup
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, App, OSCategory, ScreenType, AppCategory, UIElement, AppImage, AppVideo
from django.contrib.admin.sites import NotRegistered

for model in (AuthUser, AuthGroup):
    try:
        admin.site.unregister(model)
    except NotRegistered:
        pass

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    search_fields = ("email", "first_name", "last_name")
    list_display  = ("email", "first_name", "is_staff", "is_subscribed", "subscription_end")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"),  {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Subscription"), {"fields": ("is_subscribed", "subscription_start", "subscription_end", "payment_profile")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2"),
        }),
    )
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions",)


class AppImageInline(admin.TabularInline):
    model = AppImage
    extra = 1
    fields = ['image']
    readonly_fields = []

class AppVideoInline(admin.TabularInline):
    model = AppVideo
    extra = 1
    fields = ['video']
    readonly_fields = []

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'os_category', 'app_category']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [AppImageInline, AppVideoInline]

admin.site.register(ScreenType)
admin.site.register(AppCategory)
admin.site.register(UIElement)
admin.site.register(OSCategory)