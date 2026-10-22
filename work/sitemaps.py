from django.contrib.sitemaps import Sitemap
from django.urls import reverse

 # Last modified date

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ['work:demo_view','work:services','work:start', 'work:about', 'work:contact']

    def location(self, item):
        return reverse(item)
