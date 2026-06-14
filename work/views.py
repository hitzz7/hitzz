from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.urls import reverse
from django.utils import timezone
from .models import Category, Project, BrandLogo, HeroVideo, Invoice
from .forms import ContactForm, InvoiceForm, InvoiceItemFormSet
from .invoice_png import generate_invoice_png


def _save_invoice_form(request, invoice=None):
    form = InvoiceForm(request.POST, instance=invoice)
    formset = InvoiceItemFormSet(request.POST, instance=invoice)

    if form.is_valid() and formset.is_valid():
        invoice = form.save()
        formset.instance = invoice
        formset.save()
        return invoice
    return None, form, formset


def demo_view(request):
    projects = Project.objects.filter(is_feature=True).select_related('category')
    brand_logos = BrandLogo.objects.filter(is_active=True)
    hero_videos = HeroVideo.objects.filter(is_active=True)
    return render(request, 'work/home.html', {
        'projects': projects,
        'brand_logos': brand_logos,
        'hero_videos': hero_videos,
    })


def work(request):
    categories = Category.objects.all()
    projects = Project.objects.select_related('category').all()
    return render(request, 'work/work.html', {
        'categories': categories,
        'projects': projects,
    })


def project_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    projects = category.projects.select_related('category').prefetch_related('images').all()
    return render(request, 'work/category_detail.html', {
        'category': category,
        'projects': projects,
    })


def services(request):
    return render(request, 'work/services.html')


def about(request):
    return render(request, 'work/about.html')


def contact(request):
    return render(request, 'work/contact.html')


def start(request):
    return render(request, 'work/start.html')


def contactc(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('work:success')
    else:
        form = ContactForm()

    return render(request, 'work/start.html', {'form': form})


def success(request):
    return render(request, 'work/success.html')


def invoice_list(request):
    invoices = Invoice.objects.prefetch_related('items').all()
    return render(request, 'work/invoice_list.html', {'invoices': invoices})


def invoice_create(request):
    if request.method == 'POST':
        result = _save_invoice_form(request)
        if result and not isinstance(result, tuple):
            return redirect(reverse('work:invoice_detail', kwargs={'pk': result.pk}) + '?saved=1')
        _, form, formset = result
    else:
        form = InvoiceForm(initial={'issue_date': timezone.now().date()})
        formset = InvoiceItemFormSet()

    return render(request, 'work/invoice_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Invoice',
    })


def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice.objects.prefetch_related('items'), pk=pk)
    return render(request, 'work/invoice_detail.html', {
        'invoice': invoice,
        'saved': request.GET.get('saved') == '1',
    })


def invoice_download_png(request, pk):
    invoice = get_object_or_404(Invoice.objects.prefetch_related('items'), pk=pk)
    png_buffer = generate_invoice_png(invoice)
    filename = f'{invoice.invoice_number}.png'
    return FileResponse(png_buffer, as_attachment=True, filename=filename, content_type='image/png')


def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        result = _save_invoice_form(request, invoice=invoice)
        if result and not isinstance(result, tuple):
            return redirect(reverse('work:invoice_detail', kwargs={'pk': result.pk}) + '?saved=1')
        _, form, formset = result
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)

    return render(request, 'work/invoice_form.html', {
        'form': form,
        'formset': formset,
        'title': f'Edit {invoice.invoice_number}',
        'invoice': invoice,
    })

