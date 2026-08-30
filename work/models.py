from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(max_length=500, blank=True)
    date_created = models.DateField(auto_now_add=True)
    is_feature = models.BooleanField(default=False)
    featured_image = models.ImageField(upload_to='projects/featured/', blank=True, null=True)
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})
    
    


class StartaProject(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=150)
    description = models.TextField(blank=False)

    def __str__(self):
        return self.name


class BrandLogo(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/')
    scale = models.FloatField(default=1.0)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class HeroVideo(models.Model):
    name = models.CharField(max_length=100)
    video = models.FileField(upload_to='hero_videos/')
    poster = models.ImageField(upload_to='hero_videos/posters/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField(blank=True)
    client_address = models.TextField(blank=True)
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issue_date', '-created_at']

    def __str__(self):
        return f'{self.invoice_number} - {self.client_name}'

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last = Invoice.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.invoice_number = f'INV-{next_id:04d}'
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return sum(
            (item.line_total for item in self.items.all() if item.item_type == InvoiceItem.TYPE_CHARGE),
            Decimal('0.00'),
        )

    @property
    def tax_amount(self):
        return (self.subtotal * self.tax_rate / Decimal('100')).quantize(Decimal('0.01'))

    @property
    def total(self):
        return self.subtotal + self.tax_amount

    @property
    def advance_paid(self):
        return sum(
            (item.line_total for item in self.items.all() if item.item_type == InvoiceItem.TYPE_ADVANCE),
            Decimal('0.00'),
        )

    @property
    def balance_due(self):
        remaining_items = [
            item for item in self.items.all()
            if item.item_type == InvoiceItem.TYPE_REMAINING
        ]
        if remaining_items:
            return sum((item.line_total for item in remaining_items), Decimal('0.00'))
        return self.total - self.advance_paid

    def get_absolute_url(self):
        return reverse('work:invoice_detail', kwargs={'pk': self.pk})


class InvoiceItem(models.Model):
    TYPE_CHARGE = 'charge'
    TYPE_ADVANCE = 'advance_paid'
    TYPE_REMAINING = 'remaining_due'

    ITEM_TYPE_CHOICES = [
        (TYPE_CHARGE, 'Charge / Service'),
        (TYPE_ADVANCE, 'Advance Paid'),
        (TYPE_REMAINING, 'Remaining Due'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default=TYPE_CHARGE)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.description

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def get_type_display_short(self):
        return dict(self.ITEM_TYPE_CHOICES).get(self.item_type, self.item_type)
