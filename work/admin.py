# admin.py
from django.contrib import admin
from .models import Category, Project, StartaProject, BrandLogo, HeroVideo, Invoice, InvoiceItem


@admin.register(BrandLogo)
class BrandLogoAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'scale', 'is_active')
    list_editable = ('order', 'scale', 'is_active')
    list_filter = ('is_active',)


@admin.register(HeroVideo)
class HeroVideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client_name', 'issue_date', 'due_date', 'status', 'total_display')
    list_filter = ('status', 'issue_date')
    search_fields = ('invoice_number', 'client_name', 'client_email')
    inlines = [InvoiceItemInline]
    readonly_fields = ('invoice_number', 'created_at')

    def total_display(self, obj):
        return obj.total
    total_display.short_description = 'Total'


admin.site.register(Category)
admin.site.register(Project)
admin.site.register(StartaProject)
