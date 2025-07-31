import json
import os
from django.core.management.base import BaseCommand
from products.models import Product
from django.conf import settings
from django.core.files import File


class Command(BaseCommand):
    help = 'Load initial products from products.json into the database.'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing products.'))

        json_file_path = os.path.join(
            settings.BASE_DIR, '..', 'deko', 'public', 'products.json')

        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data['products']:
            product = Product(
                name=item['name'],
                description=item['description']
            )

            image_path = item.get('image')
            if image_path:
                relative_image_path = image_path.lstrip('/')
                source_image_path = os.path.join(
                    settings.BASE_DIR, '..', 'deko', 'public', relative_image_path)

                if os.path.exists(source_image_path):
                    with open(source_image_path, 'rb') as img_f:
                        product.image.save(os.path.basename(
                            image_path), File(img_f), save=False)
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Image file not found: {source_image_path}'))

            product.save()
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created product "{product.name}"'))
        self.stdout.write(self.style.SUCCESS('Product loading complete.')) 