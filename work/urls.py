from django.urls import path
from . import views 
from .views import demo_view
app_name = 'work'
urlpatterns = [
    
    path('', demo_view, name='demo_view'), 
    
    path('web-design-projects/', views.work, name='work'),
    
    path('project_list/<int:category_id>/', views.project_list, name='project_list'),
    path('project_detail/<int:project_id>/', views.project_detail, name='project_detail'),
     path('web-design-services/', views.services, name='services'),
       path('web-design-about/', views.about, name='about'),
         path('web-design-contact/', views.contact, name='contact'),
         path('web-design-startaproject /', views.start, name='start'),
         path('contactc/', views.contactc, name='contactc'),
    path('success/', views.success, name='success'),
]
