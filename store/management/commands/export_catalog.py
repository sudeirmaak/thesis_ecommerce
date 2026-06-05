import csv
from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Exports the product catalog to a CSV for Scikit-Learn TF-IDF processing.'

    def handle(self, *args, **kwargs):
        filename = 'dataset.csv'

        # safely close even if an error occurs
        with open(filename, mode='w', newline='', encoding='utf-8') as file: #prevent blank rows
            writer = csv.writer(file)
            
            # csv headers 
            writer.writerow([
                'product_id', 
                'name', 
                'category', 
                'description', 
                'tags', 
                'origin', 
                'roast_level', 
                'tasting_notes'
            ])

            # important! to prevent the n+1 quesy problem
            # fetch all catogory names in a single db hit
            products = Product.objects.exclude(category__slug='brewing-equipment').select_related('category')
            count = 0

            #itrate through the queryset and write data row by row
            for product in products:
                writer.writerow([
                    product.id,
                    product.name,
                    product.category.name if product.category else '',
                    product.description,
                    product.tags,
                    product.origin or '',
                    product.roast_level or '',
                    product.tasting_notes or ''
                ])
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully exported {count} products to {filename}'))