from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from store.models import Category, Product

class Command(BaseCommand):
    help = "Seed demo categories and products using the sample images in static/jof/images."

    def handle(self, *args, **options):
        fruits, _ = Category.objects.get_or_create(name="Fruits", defaults={'slug': 'fruits'})
        berries, _ = Category.objects.get_or_create(name="Berries", defaults={'slug': 'berries'})

        image_dir = Path(settings.BASE_DIR) / 'static' / 'jof' / 'images'
        candidates = sorted([p for p in image_dir.glob('*.JPG')])

        if not candidates:
            self.stdout.write(self.style.WARNING("No JPG images found in static/jof/images."))
            return

        demo = [
            ("Mango & Apricot Mix", fruits, "Fresh assorted fruit selection.", "3500.00"),
            ("Green Apples", fruits, "Crisp green apples.", "2800.00"),
            ("Fruit Combo Pack", fruits, "Apples, orange and kiwi combo.", "5200.00"),
            ("Bananas", fruits, "Sweet bananas.", "2200.00"),
            ("Lime", fruits, "Fresh lime (vitamin C).", "1800.00"),
            ("Pineapple Slices", fruits, "Juicy pineapple.", "3000.00"),
            ("Apple Basket", fruits, "Basket of apples.", "6500.00"),
            ("Berry Mix", berries, "Strawberry, cherry & blackberry.", "4200.00"),
            ("Black Grapes", fruits, "Sweet black grapes.", "3200.00"),
        ]

        # Create products and attach images in order
        for i, (name, cat, desc, price) in enumerate(demo):
            p, created = Product.objects.get_or_create(
                name=name,
                defaults={'category': cat, 'description': desc, 'price': price, 'is_active': True},
            )
            if created and i < len(candidates):
                # Copy image into media/products and set ImageField to relative path
                src = candidates[i]
                dest_dir = Path(settings.MEDIA_ROOT) / 'products'
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest = dest_dir / src.name
                dest.write_bytes(src.read_bytes())
                p.image = f"products/{src.name}"
                p.save()
                self.stdout.write(self.style.SUCCESS(f"Created: {p.name}"))
            else:
                self.stdout.write(f"Exists: {p.name}")

        self.stdout.write(self.style.SUCCESS("Done. Visit /admin to manage products."))
