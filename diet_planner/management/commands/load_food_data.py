"""
Django Management Command to Load Ayurvedic Food Dataset
Loads comprehensive food data with Ayurvedic properties into the database
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from diet_planner.models import Food
from food_dataset import AYURVEDIC_FOOD_DATA, DATASET_INFO
import sys

class Command(BaseCommand):
    help = 'Load comprehensive Ayurvedic food dataset into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing food data before loading new data',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be loaded without actually loading data',
        )

    def handle(self, *args, **options):
        """Main command handler"""
        self.stdout.write(
            self.style.SUCCESS('🌿 AyurDiet Food Dataset Loader')
        )
        self.stdout.write(f"📊 Dataset contains: {DATASET_INFO['total_items']} food items")
        self.stdout.write(f"🏷️  Categories: {', '.join(DATASET_INFO['categories'])}")
        self.stdout.write("")

        # Check if this is a dry run
        if options['dry_run']:
            self.show_dry_run()
            return

        # Clear existing data if requested
        if options['clear']:
            self.clear_existing_data()

        # Check for existing data
        existing_count = Food.objects.count()
        if existing_count > 0 and not options['clear']:
            self.stdout.write(
                self.style.WARNING(f"⚠️  Found {existing_count} existing food items in database")
            )
            response = input("Do you want to continue? This may create duplicates. (y/N): ")
            if response.lower() != 'y':
                self.stdout.write(self.style.ERROR("❌ Loading cancelled by user"))
                return

        # Load the food data
        self.load_food_data()

    def show_dry_run(self):
        """Show what would be loaded without actually loading"""
        self.stdout.write(self.style.HTTP_INFO("🔍 DRY RUN - Preview of data to be loaded:"))
        self.stdout.write("")

        # Group by categories
        categories = {}
        for food_item in AYURVEDIC_FOOD_DATA:
            category = food_item['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(food_item['name'])

        for category, foods in categories.items():
            self.stdout.write(f"📁 {category} ({len(foods)} items):")
            for food in foods[:5]:  # Show first 5 items
                self.stdout.write(f"   • {food}")
            if len(foods) > 5:
                self.stdout.write(f"   ... and {len(foods) - 5} more items")
            self.stdout.write("")

        self.stdout.write(self.style.HTTP_INFO("👆 Run without --dry-run to actually load this data"))

    def clear_existing_data(self):
        """Clear existing food data from database"""
        existing_count = Food.objects.count()
        if existing_count > 0:
            self.stdout.write(f"🗑️  Clearing {existing_count} existing food items...")
            Food.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("✅ Existing data cleared"))
        else:
            self.stdout.write("ℹ️  No existing data to clear")

    def load_food_data(self):
        """Load food data into database with transaction safety"""
        self.stdout.write("📥 Loading food data...")
        
        success_count = 0
        error_count = 0
        skipped_count = 0

        try:
            with transaction.atomic():
                for food_data in AYURVEDIC_FOOD_DATA:
                    try:
                        # Check if food already exists
                        if Food.objects.filter(name=food_data['name']).exists():
                            self.stdout.write(
                                self.style.WARNING(f"⚠️  Skipping {food_data['name']} - already exists")
                            )
                            skipped_count += 1
                            continue

                        # Create food object
                        food = Food.objects.create(
                            name=food_data['name'],
                            calories=food_data.get('calories'),
                            protein=food_data.get('protein'),
                            rasa=food_data.get('rasa'),
                            guna=food_data.get('guna'),
                            virya=food_data.get('virya')
                        )
                        success_count += 1
                        
                        # Show progress every 50 items
                        if success_count % 50 == 0:
                            self.stdout.write(f"   📊 Loaded {success_count} items...")

                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(f"❌ Error loading {food_data['name']}: {str(e)}")
                        )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"💥 Critical error during data loading: {str(e)}")
            )
            raise CommandError(f"Failed to load food data: {str(e)}")

        # Show final results
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("🎉 Food data loading completed!"))
        self.stdout.write(f"✅ Successfully loaded: {success_count} items")
        if skipped_count > 0:
            self.stdout.write(f"⏭️  Skipped (already exist): {skipped_count} items")
        if error_count > 0:
            self.stdout.write(f"❌ Errors: {error_count} items")
        
        # Verify the data
        self.verify_loaded_data()

    def verify_loaded_data(self):
        """Verify that data was loaded correctly"""
        self.stdout.write("")
        self.stdout.write("🔍 Verifying loaded data...")
        
        total_foods = Food.objects.count()
        self.stdout.write(f"📊 Total foods in database: {total_foods}")
        
        # Check some sample data
        sample_foods = Food.objects.all()[:5]
        self.stdout.write("🔬 Sample data:")
        for food in sample_foods:
            self.stdout.write(f"   • {food.name} - {food.rasa} - {food.virya}")
        
        # Check categories (we don't have category field in model, but we can check variety)
        unique_rasas = Food.objects.values_list('rasa', flat=True).distinct()
        unique_viryas = Food.objects.values_list('virya', flat=True).distinct()
        
        self.stdout.write(f"🏷️  Unique Rasas: {len([r for r in unique_rasas if r])}")
        self.stdout.write(f"🌡️  Unique Viryas: {len([v for v in unique_viryas if v])}")
        
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✅ Data verification completed!"))
        self.stdout.write("")
        self.stdout.write("🚀 Next Steps:")
        self.stdout.write("   1. Test food search: python manage.py shell")
        self.stdout.write("      >>> from diet_planner.models import Food")
        self.stdout.write("      >>> Food.objects.filter(virya='Cooling').count()")
        self.stdout.write("   2. Start Django server: python manage.py runserver")
        self.stdout.write("   3. Visit admin panel: http://localhost:8000/admin/")
        self.stdout.write("   4. Test API endpoint: http://localhost:8000/api/foods/")