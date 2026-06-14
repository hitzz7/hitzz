from django import forms
from django.forms import inlineformset_factory
from .models import StartaProject, Invoice, InvoiceItem


class ContactForm(forms.ModelForm):
    class Meta:
        model = StartaProject
        fields = ['name', 'email', 'mobile', 'description']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'client_name', 'client_email', 'client_address',
            'issue_date', 'due_date', 'tax_rate', 'notes', 'status',
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'client_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['item_type', 'description', 'quantity', 'unit_price']
        widgets = {
            'item_type': forms.Select(attrs={'class': 'item-type-select'}),
            'description': forms.TextInput(attrs={'placeholder': 'e.g. Website Design, Advance Paid, Remaining Due'}),
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'unit_price': forms.NumberInput(attrs={'step': '0.01', 'min': 0}),
        }


InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)

