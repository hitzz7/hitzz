from django.urls import path
from . import views 
from .views import demo_view
app_name = 'work'
urlpatterns = [
    
    path('', demo_view, name='demo_view'), 
    
    path('work/', views.work, name='work'),
    
    path('project_list/<int:category_id>/', views.project_list, name='project_list'),
    path('project_detail/<int:project_id>/', views.project_detail, name='project_detail'),
     path('services/', views.services, name='services'),
       path('about/', views.about, name='about'),
         path('contact/', views.contact, name='contact'),
         path('start /', views.start, name='start'),
         path('contactc/', views.contactc, name='contactc'),
    path('success/', views.success, name='success'),
]
