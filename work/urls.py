from django.urls import path
from . import views 
from .views import demo_view
from django.contrib.sitemaps.views import sitemap

from .sitemaps import ProjectSitemap, StaticViewSitemap

sitemaps = {
    'projects': ProjectSitemap(),
    'static': StaticViewSitemap(),
}
app_name = 'work'
urlpatterns = [
    
    path('', demo_view, name='demo_view'), 
    
    path('web-design-projects/', views.work, name='work'),
    
    path('project_list/<int:category_id>/', views.project_list, name='project_list'),
    
     path('web-design-services/', views.services, name='services'),
       path('web-design-about/', views.about, name='about'),
         path('web-design-contact/', views.contact, name='contact'),
         path('web-design-startaproject/', views.start, name='start'),
         path('contactc/', views.contactc, name='contactc'),
    path('success/', views.success, name='success'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/<int:pk>/download.png', views.invoice_download_png, name='invoice_download_png'),
    path('invoices/<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
