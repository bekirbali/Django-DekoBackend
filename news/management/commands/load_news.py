import json
import os
from django.core.management.base import BaseCommand
from news.models import News
from django.conf import settings
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Load initial news from products.json into the database.'

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, '..', 'deko', 'public', 'products.json')
        json_path = os.path.abspath(json_path)

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'File not found: {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        news_items = data.get('news', [])

        for item in news_items:
            image_url = item.get('image', '')
            image_name = os.path.basename(image_url) if image_url else ''
            
            # Check if news item already exists
            obj, created = News.objects.get_or_create(
                title=item['title'],
                defaults={
                    'context': item.get('context', ''),
                }
            )

            if created:
                if image_name:
                    # This is a simplified way to handle images from a URL.
                    # In a real-world scenario, you might need to handle different URL schemes
                    # and have more robust error handling.
                    try:
                        # For local file paths in products.json, construct a full path
                        # The path in json is like '/assets/images/news/news1.jpg'
                        image_file_path = os.path.join(settings.BASE_DIR, '..', 'deko', 'public', image_url.lstrip('/'))
                        image_file_path = os.path.abspath(image_file_path)

                        if os.path.exists(image_file_path):
                            with open(image_file_path, 'rb') as img_f:
                                obj.image.save(image_name, ContentFile(img_f.read()), save=True)
                            self.stdout.write(self.style.SUCCESS(f'Created and saved image for: {obj.title}'))
                        else:
                            self.stdout.write(self.style.WARNING(f'Image file not found for {obj.title}: {image_file_path}'))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Could not save image for {obj.title}: {e}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Created: {obj.title} (no image)'))
            else:
                self.stdout.write(self.style.WARNING(f'Exists: {obj.title}'))
        
        self.stdout.write(self.style.SUCCESS('News loading complete.')) 