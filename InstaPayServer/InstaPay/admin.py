from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Bloger)
class BlogerAdmin(admin.ModelAdmin):

    fieldsets = (

        ("personal information", {"fields": ("name", "last_name", "national_code")}),
        ("identity", {"fields": ("bloger_email", "phone_number", "address")}),
        ("bank information", {"fields": ("bank_name", "bank_account_number", "shaba")}),
        ("Security information", {"fields": ("bloger_hashcode", "bloger_password_hashcode")}),

    )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    fieldsets = (

        ("product information", {"fields": ("name", "price", "description", "number", "category", "product_hashcode")}),
        ("off code", {"fields": ("off_code", "off_code_deadline")}),
        ("status", {"fields": ("purchase_state",)}),
        ("relation", {"fields": ("bloger",)})

    )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):

    fieldsets = (

        ("customer information", {"fields": ("name", "last_name", "phone_number", "address", "customer_email",
                                             "postal_code")}),

        ("relation", {"fields": ("bloger", "product")})

    )


@admin.register(models.Factor)
class FactorAdmin(admin.ModelAdmin):

    fieldsets = (

        ("factor information", {"fields": ("factor_id", "price", "number_of_product")}),
        ("customer factor", {"fields": ("customer_payment_year", "customer_payment_month", "customer_payment_day",
                                        "customer_payment_hours", "customer_payment_minutes")}),

        ("delivery factor", {"fields": ("factor_statement_ordering_factor", "delivery_year", "delivery_month",
                                        "delivery_day", "delivery_hours", "delivery_minutes")}),

        ("bloger factor", {"fields": ("factor_statement_payment_to_bloger", "bloger_payment_year",
                                      "bloger_payment_month", "bloger_payment_day", "bloger_payment_hours",
                                      "bloger_payment_minutes", "bloger_payment_bank", "bloger_payment_serial")}),

        ("relation", {"fields": ("bloger", "product", "customer", "off_code")})

    )


@admin.register(models.OffCode)
class OffCodeAdmin(admin.ModelAdmin):

    fieldsets = (

        ("off code information", {"fields": ("off_code_id", "off_number", "deadline", "generating_time", "using")}),
        ("relation", {"fields": ("bloger", "product", "customer")})

    )


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):

    fieldsets = (

        ("Image information", {"fields": ("name", "image",)}),
        ("relation", {"fields": ("product",)})

    )
