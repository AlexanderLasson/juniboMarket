from django.contrib.sitemaps import Sitemap
from .models import Product


class ProductSitemap(Sitemap):
    changefreq = "weekly" 
    priority = 0.8 

    def items(self):
        return Product.objects.filter(current=True)

    def lastmod(self, obj):
        return obj.updated_on if hasattr(obj, 'updated_on') else None

    def location(self, obj):
        return f'/products/{obj.pk}/'  
