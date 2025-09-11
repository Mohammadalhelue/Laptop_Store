from django.core.management.base import BaseCommand
from store.models import Accessory
from django.utils.text import slugify
SAMPLES = [
    {'name':'USB-C Charger 65W','category':'charger','description':'شاحن USB-C سريع 65 واط مناسب لأغلب اللابتوبات الحديثة','price':49.99,'stock':120},
    {'name':'Laptop Sleeve 13 inch','category':'bag','description':'حافظة لابتوب مبطنة 13 بوصة','price':19.99,'stock':50},
    {'name':'Wireless Mouse Pro','category':'mouse','description':'ماوس لاسلكي بدقة عالية وتصميم مريح','price':29.99,'stock':200},
    {'name':'Mechanical Keyboard Compact','category':'keyboard','description':'لوحة مفاتيح ميكانيكية مدمجة بإضاءة خلفية','price':79.99,'stock':80},
    {'name':'USB-C to HDMI Adapter','category':'adapter','description':'محول USB-C إلى HDMI بدقة 4K','price':24.99,'stock':150},
    {'name':'Laptop Cooling Stand','category':'stand','description':'حامل تبريد قابل للتعديل للابتوبات','price':34.50,'stock':75},
    {'name':'Multiport Docking Station','category':'adapter','description':'محطة وصل متعددة المنافذ للابتوب','price':129.99,'stock':30},
    {'name':'Portable SSD 1TB','category':'other','description':'قرص صلب SSD خارجي 1 تيرابايت','price':109.99,'stock':65},
]

class Command(BaseCommand):
    help = 'Seed sample accessories data'

    def handle(self, *args, **options):
        for s in SAMPLES:
            slug = slugify(s['name'])
            obj, created = Accessory.objects.get_or_create(slug=slug, defaults={
                'name': s['name'],
                'description': s['description'],
                'category': s['category'],
                'price': s['price'],
                'stock': s['stock'],
            })
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created {obj.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Exists {obj.name}'))
