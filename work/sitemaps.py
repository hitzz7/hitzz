from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project

class ProjectSitemap(Sitemap):
    changefreq = "weekly"  # How often the page content changes
    priority = 0.8  # Importance (1.0 is the highest)
    
    def items(self):
        return Project.objects.all()  # Retrieve all projects
    
    def lastmod(self, obj):
        return obj.date_created
    
    def location(self, obj):
        return obj.get_absolute_url() # Last modified date

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ['home', 'about', 'contact']  # List of static pages

    def location(self, item):
        return reverse(item)
