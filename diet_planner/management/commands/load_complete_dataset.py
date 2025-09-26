from django.core.management.base import BaseCommand
from django.db import transaction
from diet_planner.models import Food, DietPlanTemplate
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load comprehensive Ayurvedic diet plans and foods from verified dataset'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write("Clearing existing data...")
            Food.objects.all().delete()
            DietPlanTemplate.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Data cleared successfully"))

        with transaction.atomic():
            self.load_foods()
            self.load_diet_plan_templates()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded {Food.objects.count()} foods and '
                f'{DietPlanTemplate.objects.count()} diet plan templates'
            )
        )

    def load_foods(self):
        """Load all 36 foods from the verified Ayurvedic dataset"""
        foods_data = [
            # GRAINS & CEREALS
            {
                'name': 'Basmati Rice (White)',
                'food_category': 'Grain',
                'calories': Decimal('345'),
                'protein': Decimal('6.8'),
                'carbs': Decimal('78.2'),
                'fat': Decimal('0.6'),
                'virya': 'Cooling',
                'rasa': 'Sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Increases',
                'digestibility': 'Easy to digest',
                'used_in_plans': 'All basic dosha plans, dual constitution plans',
            },
            {
                'name': 'Barley (Jau)',
                'food_category': 'Grain',
                'calories': Decimal('354'),
                'protein': Decimal('12.5'),
                'carbs': Decimal('73.5'),
                'fat': Decimal('2.3'),
                'virya': 'Cooling',
                'rasa': 'Sweet, astringent',
                'vipaka': 'Sweet',
                'vata_effect': 'Increases',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Balances',
                'digestibility': 'Hard to digest',
                'used_in_plans': 'Pitta balance, Kapha reduction, diabetes, weight loss',
            },
            {
                'name': 'Oats',
                'food_category': 'Grain',
                'calories': Decimal('389'),
                'protein': Decimal('16.9'),
                'carbs': Decimal('66.3'),
                'fat': Decimal('6.9'),
                'virya': 'Heating',
                'rasa': 'Sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Neutral',
                'digestibility': 'Easy to moderate',
                'used_in_plans': 'Vata balance, dual constitutions, anxiety plan',
            },
            {
                'name': 'Quinoa',
                'food_category': 'Grain',
                'calories': Decimal('368'),
                'protein': Decimal('14.1'),
                'carbs': Decimal('64.2'),
                'fat': Decimal('6.1'),
                'virya': 'Heating',
                'rasa': 'Sweet, astringent',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Balances',
                'digestibility': 'Easy to moderate',
                'used_in_plans': 'Dual constitutions, diabetes management',
            },
            {
                'name': 'Millet (Bajra)',
                'food_category': 'Grain',
                'calories': Decimal('361'),
                'protein': Decimal('11.6'),
                'carbs': Decimal('67.5'),
                'fat': Decimal('5.0'),
                'virya': 'Heating',
                'rasa': 'Sweet, astringent',
                'vipaka': 'Sweet',
                'vata_effect': 'Increases',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Balances',
                'digestibility': 'Hard to digest',
                'used_in_plans': 'Kapha reduction, weight loss, diabetes',
            },
            
            # LEGUMES & PULSES
            {
                'name': 'Mung Dal (Split Yellow Lentils)',
                'food_category': 'Pulse',
                'calories': Decimal('347'),
                'protein': Decimal('24.5'),
                'carbs': Decimal('59.9'),
                'fat': Decimal('1.2'),
                'virya': 'Cooling',
                'rasa': 'Sweet, astringent',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Balances',
                'digestibility': 'Easy (best among all dals)',
                'used_in_plans': 'All plans, especially digestive weakness, detox',
            },
            {
                'name': 'Horse Gram (Kulthi)',
                'food_category': 'Pulse',
                'calories': Decimal('321'),
                'protein': Decimal('22.0'),
                'carbs': Decimal('57.2'),
                'fat': Decimal('0.6'),
                'virya': 'Heating',
                'rasa': 'Astringent, sweet',
                'vipaka': 'Pungent',
                'vata_effect': 'Increases',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Balances',
                'digestibility': 'Very hard to digest',
                'used_in_plans': 'Weight loss, Kapha reduction, respiratory issues',
            },
            {
                'name': 'Legumes (General)',
                'food_category': 'Pulse',
                'calories': Decimal('355'),
                'protein': Decimal('22.5'),
                'carbs': Decimal('60.0'),
                'fat': Decimal('2.0'),
                'virya': 'Heating',
                'rasa': 'Sweet, astringent',
                'vipaka': 'Sweet',
                'vata_effect': 'Increases',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Balances',
                'digestibility': 'Moderate to hard',
                'used_in_plans': 'Kapha reduction, weight loss, diabetes',
            },
            
            # VEGETABLES
            {
                'name': 'Leafy Greens (Spinach, etc.)',
                'food_category': 'Leafy Vegetable',
                'calories': Decimal('25'),
                'protein': Decimal('2.5'),
                'carbs': Decimal('3.8'),
                'fat': Decimal('0.5'),
                'virya': 'Cooling',
                'rasa': 'Sweet, astringent, bitter',
                'vipaka': 'Sweet',
                'vata_effect': 'Neutral',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Balances',
                'digestibility': 'Moderate',
                'used_in_plans': 'Pitta balance, skin disorders, menstrual health, diabetes',
            },
            {
                'name': 'Cucumber (Kheera)',
                'food_category': 'Fruit Vegetable',
                'calories': Decimal('13'),
                'protein': Decimal('0.7'),
                'carbs': Decimal('2.5'),
                'fat': Decimal('0.1'),
                'virya': 'Cooling',
                'rasa': 'Sweet, astringent',
                'vipaka': 'Sweet',
                'vata_effect': 'Increases',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Increases',
                'digestibility': 'Easy',
                'used_in_plans': 'Pitta balance, high blood pressure, skin disorders',
            },
            {
                'name': 'Bottle Gourd (Lauki)',
                'food_category': 'Fruit Vegetable',
                'calories': Decimal('15'),
                'protein': Decimal('0.6'),
                'carbs': Decimal('3.4'),
                'fat': Decimal('0.1'),
                'virya': 'Cooling',
                'rasa': 'Sweet, astringent',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Balances',
                'digestibility': 'Very easy',
                'used_in_plans': 'Pitta balance, high blood pressure, digestive weakness',
            },
            {
                'name': 'Bitter Gourd (Karela)',
                'food_category': 'Fruit Vegetable',
                'calories': Decimal('19'),
                'protein': Decimal('0.9'),
                'carbs': Decimal('4.2'),
                'fat': Decimal('0.2'),
                'virya': 'Cooling',
                'rasa': 'Bitter, pungent',
                'vipaka': 'Pungent',
                'vata_effect': 'Increases',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Balances',
                'digestibility': 'Hard to digest',
                'used_in_plans': 'Diabetes, weight loss, Kapha reduction, skin disorders',
            },
            {
                'name': 'Garlic (Lahsun)',
                'food_category': 'Bulb Vegetable',
                'calories': Decimal('149'),
                'protein': Decimal('6.4'),
                'carbs': Decimal('33.1'),
                'fat': Decimal('0.5'),
                'virya': 'Heating',
                'rasa': 'All except sour (mainly pungent)',
                'vipaka': 'Pungent',
                'vata_effect': 'Balances',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Balances',
                'digestibility': 'Hard to digest (raw), easier when cooked',
                'used_in_plans': 'Respiratory issues, Vata balance, Kapha reduction',
            },
            {
                'name': 'Onion (Pyaz)',
                'food_category': 'Bulb Vegetable',
                'calories': Decimal('50'),
                'protein': Decimal('1.2'),
                'carbs': Decimal('11.1'),
                'fat': Decimal('0.1'),
                'virya': 'Heating',
                'rasa': 'Sweet, pungent',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Balances',
                'digestibility': 'Moderate',
                'used_in_plans': 'Respiratory issues, Kapha reduction',
            },
            {
                'name': 'Root Vegetables (Carrots, Beets, Sweet Potato)',
                'food_category': 'Root Vegetable',
                'calories': Decimal('61'),
                'protein': Decimal('1.5'),
                'carbs': Decimal('14.1'),
                'fat': Decimal('0.2'),
                'virya': 'Cooling to neutral',
                'rasa': 'Sweet, astringent',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Increases',
                'digestibility': 'Easy to moderate',
                'used_in_plans': 'Vata balance, dual constitutions',
            },
            {
                'name': 'Steamed Vegetables (General)',
                'food_category': 'Mixed Vegetables',
                'calories': Decimal('35'),
                'protein': Decimal('2.0'),
                'carbs': Decimal('8.0'),
                'fat': Decimal('0.3'),
                'virya': 'Depends on vegetables used',
                'rasa': 'Mixed (sweet, bitter, astringent)',
                'vipaka': 'Generally sweet',
                'vata_effect': 'Depends on combination',
                'pitta_effect': 'Depends on combination',
                'kapha_effect': 'Depends on combination',
                'digestibility': 'Easy to moderate',
                'used_in_plans': 'All plans, especially digestive issues',
            },
            
            # FRUITS
            {
                'name': 'Fresh Fruits (Sweet varieties)',
                'food_category': 'Fruit',
                'calories': Decimal('65'),
                'protein': Decimal('0.9'),
                'carbs': Decimal('15.5'),
                'fat': Decimal('0.3'),
                'virya': 'Generally cooling',
                'rasa': 'Sweet (ripe fruits)',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Increases',
                'digestibility': 'Easy',
                'used_in_plans': 'Vata balance, Pitta balance, dual constitutions',
            },
            {
                'name': 'Cooked Fruits',
                'food_category': 'Processed Fruit',
                'calories': Decimal('58'),
                'protein': Decimal('0.6'),
                'carbs': Decimal('14.0'),
                'fat': Decimal('0.2'),
                'virya': 'Heating (due to cooking)',
                'rasa': 'Sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Neutral to slightly increasing',
                'kapha_effect': 'Increases',
                'digestibility': 'Very easy',
                'used_in_plans': 'Vata balance, digestive weakness',
            },
            {
                'name': 'Dates (Khajur)',
                'food_category': 'Dried Fruit',
                'calories': Decimal('277'),
                'protein': Decimal('1.8'),
                'carbs': Decimal('75.0'),
                'fat': Decimal('0.2'),
                'virya': 'Heating',
                'rasa': 'Sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Neutral',
                'kapha_effect': 'Increases',
                'digestibility': 'Easy',
                'used_in_plans': 'Vata balance, anxiety, menstrual disorders, nervous system support',
            },
            {
                'name': 'Figs (Anjeer)',
                'food_category': 'Fruit/Dried Fruit',
                'calories': Decimal('161'),
                'protein': Decimal('2.1'),
                'carbs': Decimal('41.6'),
                'fat': Decimal('0.6'),
                'virya': 'Cooling',
                'rasa': 'Sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Increases',
                'digestibility': 'Easy',
                'used_in_plans': 'Menstrual disorders, hormonal balance',
            },
            
            # DAIRY & ALTERNATIVES
            {
                'name': 'Milk (Cow\'s)',
                'food_category': 'Dairy',
                'calories': Decimal('64'),
                'protein': Decimal('3.3'),
                'carbs': Decimal('4.9'),
                'fat': Decimal('3.6'),
                'virya': 'Cooling',
                'rasa': 'Sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Increases',
                'digestibility': 'Moderate (better warm)',
                'used_in_plans': 'Vata balance, anxiety, nervous system support',
            },
            {
                'name': 'Buttermilk',
                'food_category': 'Fermented Dairy',
                'calories': Decimal('45'),
                'protein': Decimal('3.1'),
                'carbs': Decimal('4.8'),
                'fat': Decimal('0.9'),
                'virya': 'Heating',
                'rasa': 'Sour, astringent',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Balances',
                'digestibility': 'Easy',
                'used_in_plans': 'Digestive weakness, Vata balance',
            },
            {
                'name': 'Lassi (Sweet)',
                'food_category': 'Fermented Dairy Drink',
                'calories': Decimal('70'),
                'protein': Decimal('2.8'),
                'carbs': Decimal('7.0'),
                'fat': Decimal('3.0'),
                'virya': 'Cooling',
                'rasa': 'Sweet, sour',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Increases',
                'digestibility': 'Easy',
                'used_in_plans': 'Pitta balance, dual constitutions',
            },
            {
                'name': 'Ghee',
                'food_category': 'Clarified Butter',
                'calories': Decimal('900'),
                'protein': Decimal('0.3'),
                'carbs': Decimal('0.0'),
                'fat': Decimal('99.8'),
                'virya': 'Cooling',
                'rasa': 'Sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Increases',
                'digestibility': 'Easy (enhances digestion when used in small amounts)',
                'used_in_plans': 'Most plans (essential for Vata balance, digestive health)',
            },
            
            # NUTS, SEEDS & OILS
            {
                'name': 'Almonds (Badam)',
                'food_category': 'Nuts',
                'calories': Decimal('579'),
                'protein': Decimal('21.2'),
                'carbs': Decimal('21.6'),
                'fat': Decimal('49.9'),
                'virya': 'Heating',
                'rasa': 'Sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Increases',
                'digestibility': 'Moderate (better when soaked)',
                'used_in_plans': 'Vata balance, anxiety, nervous system support',
            },
            {
                'name': 'Sesame Seeds (Til)',
                'food_category': 'Seeds',
                'calories': Decimal('573'),
                'protein': Decimal('17.7'),
                'carbs': Decimal('23.4'),
                'fat': Decimal('49.7'),
                'virya': 'Heating',
                'rasa': 'Sweet, bitter',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Increases',
                'digestibility': 'Moderate',
                'used_in_plans': 'Menstrual disorders, hormonal balance',
            },
            {
                'name': 'Coconut',
                'food_category': 'Fruit/Fat',
                'calories': Decimal('354'),
                'protein': Decimal('3.3'),
                'carbs': Decimal('15.2'),
                'fat': Decimal('33.5'),
                'virya': 'Cooling',
                'rasa': 'Sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Increases',
                'digestibility': 'Easy to moderate',
                'used_in_plans': 'Pitta balance, skin disorders',
            },
            {
                'name': 'Coconut Water',
                'food_category': 'Natural Drink',
                'calories': Decimal('19'),
                'protein': Decimal('0.7'),
                'carbs': Decimal('3.7'),
                'fat': Decimal('0.2'),
                'virya': 'Cooling',
                'rasa': 'Sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Neutral',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Increases',
                'digestibility': 'Very easy',
                'used_in_plans': 'Pitta balance, high blood pressure, skin disorders',
            },
            
            # SPICES & HERBS
            {
                'name': 'Ginger (Fresh - Adrak)',
                'food_category': 'Spice/Root',
                'calories': Decimal('80'),
                'protein': Decimal('1.8'),
                'carbs': Decimal('17.8'),
                'fat': Decimal('0.8'),
                'virya': 'Heating',
                'rasa': 'Pungent, sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Balances',
                'digestibility': 'Enhances digestion',
                'used_in_plans': 'All plans for digestive support, especially Vata and Kapha conditions',
            },
            {
                'name': 'Turmeric (Haldi)',
                'food_category': 'Spice',
                'calories': Decimal('354'),
                'protein': Decimal('7.8'),
                'carbs': Decimal('64.9'),
                'fat': Decimal('9.9'),
                'virya': 'Heating',
                'rasa': 'Bitter, pungent',
                'vipaka': 'Pungent',
                'vata_effect': 'Neutral to balancing',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Balances',
                'digestibility': 'Enhances digestion, purifying',
                'used_in_plans': 'Skin disorders, diabetes, respiratory issues, detox',
            },
            {
                'name': 'Cumin (Jeera)',
                'food_category': 'Spice',
                'calories': Decimal('375'),
                'protein': Decimal('17.8'),
                'carbs': Decimal('44.2'),
                'fat': Decimal('22.3'),
                'virya': 'Heating',
                'rasa': 'Pungent, bitter',
                'vipaka': 'Pungent',
                'vata_effect': 'Balances',
                'pitta_effect': 'Neutral',
                'kapha_effect': 'Balances',
                'digestibility': 'Excellent digestive aid',
                'used_in_plans': 'Digestive weakness, detox, most cooking preparations',
            },
            {
                'name': 'Coriander (Dhania)',
                'food_category': 'Spice/Herb',
                'calories': Decimal('298'),
                'protein': Decimal('12.4'),
                'carbs': Decimal('55.0'),
                'fat': Decimal('17.8'),
                'virya': 'Cooling',
                'rasa': 'Pungent, sweet',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Neutral',
                'digestibility': 'Good digestive support',
                'used_in_plans': 'Pitta balance, skin disorders, high blood pressure',
            },
            {
                'name': 'Fennel (Saunf)',
                'food_category': 'Spice',
                'calories': Decimal('345'),
                'protein': Decimal('15.8'),
                'carbs': Decimal('52.3'),
                'fat': Decimal('14.9'),
                'virya': 'Cooling',
                'rasa': 'Sweet, pungent',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Balances',
                'kapha_effect': 'Neutral to balancing',
                'digestibility': 'Excellent digestive aid',
                'used_in_plans': 'Pitta balance, menstrual disorders, digestive support',
            },
            {
                'name': 'Cardamom (Elaichi)',
                'food_category': 'Spice',
                'calories': Decimal('311'),
                'protein': Decimal('10.8'),
                'carbs': Decimal('68.5'),
                'fat': Decimal('6.7'),
                'virya': 'Heating',
                'rasa': 'Sweet, pungent',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Neutral',
                'kapha_effect': 'Balances',
                'digestibility': 'Digestive and carminative',
                'used_in_plans': 'Anxiety, nervous system support, respiratory issues',
            },
            {
                'name': 'Cinnamon (Dalchini)',
                'food_category': 'Spice',
                'calories': Decimal('247'),
                'protein': Decimal('4.0'),
                'carbs': Decimal('50.6'),
                'fat': Decimal('1.2'),
                'virya': 'Heating',
                'rasa': 'Sweet, pungent, astringent',
                'vipaka': 'Sweet',
                'vata_effect': 'Balances',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Balances',
                'digestibility': 'Digestive stimulant',
                'used_in_plans': 'Diabetes, weight loss, Kapha reduction, respiratory',
            },
            {
                'name': 'Black Pepper (Kali Mirch)',
                'food_category': 'Spice',
                'calories': Decimal('251'),
                'protein': Decimal('10.4'),
                'carbs': Decimal('63.9'),
                'fat': Decimal('3.3'),
                'virya': 'Heating',
                'rasa': 'Pungent',
                'vipaka': 'Pungent',
                'vata_effect': 'Balances',
                'pitta_effect': 'Increases',
                'kapha_effect': 'Balances',
                'digestibility': 'Enhances digestion',
                'used_in_plans': 'Weight loss, respiratory issues, digestive weakness',
            },
        ]

        for food_data in foods_data:
            food, created = Food.objects.get_or_create(
                name=food_data['name'],
                defaults=food_data
            )
            if created:
                self.stdout.write(f"Created food: {food.name}")
            else:
                self.stdout.write(f"Food already exists: {food.name}")

    def load_diet_plan_templates(self):
        """Load all 15 verified Ayurvedic diet plan templates"""
        diet_plans_data = [
            # 1. VATA IMBALANCE DIET PLAN
            {
                'name': 'Vata Imbalance Diet Plan',
                'plan_type': 'dosha_balance',
                'target_dosha': 'Vata',
                'conditions_treated': 'Anxiety, constipation, dry skin, insomnia, irregular digestion',
                'principle': 'Vatas should favour warm, cooked foods and avoid cold, raw, dry, or crunchy foods',
                'daily_schedule': {
                    'early_morning': '6-7 AM: Warm water with ginger and honey, Soaked almonds (5-6 pieces)',
                    'breakfast': '7-8 AM: Oatmeal, cooked fruits, root vegetables, and warming spices. Options: Khichdi with ghee, warm milk with dates, cooked oats with cinnamon',
                    'mid_morning': '10 AM: Herbal tea (ginger-cardamom or fennel)',
                    'lunch': '12-1 PM: Basmati rice with mung dal, Steamed vegetables (carrots, beets, sweet potato), Ghee (1-2 tsp), Buttermilk with cumin',
                    'evening': '4 PM: Warm almond milk or herbal tea, 2-3 dates',
                    'dinner': '6-7 PM: Light khichdi or vegetable soup, Cooked vegetables with mild spices, Small portion of rice or chapati with ghee'
                },
                'meal_guidelines': {
                    'temperature': 'Warm, cooked foods preferred',
                    'texture': 'Soft, moist, oily',
                    'timing': 'Regular meal times, eat when hungry'
                },
                'foods_to_favor': 'Warm, oily, heavy foods; sweet, sour, salty tastes; cooked grains, root vegetables, dairy, nuts, oils',
                'foods_to_avoid': 'Cold, dry, light foods; bitter, pungent, astringent tastes; raw vegetables, beans, caffeine',
                'difficulty_level': 'beginner'
            },
            
            # 2. PITTA IMBALANCE DIET PLAN
            {
                'name': 'Pitta Imbalance Diet Plan',
                'plan_type': 'dosha_balance',
                'target_dosha': 'Pitta',
                'conditions_treated': 'Acidity, inflammation, anger, skin rashes, excessive heat',
                'principle': 'To balance pitta, foods that are internally cooling, astringent, and mild are recommended',
                'daily_schedule': {
                    'early_morning': '6-7 AM: Cool water with lime juice, Fresh coconut water',
                    'breakfast': '7-8 AM: Cool porridge with milk, Fresh fruits (sweet apples, pears, grapes), Rose water or fennel tea',
                    'mid_morning': '10 AM: Cooling herbal tea (mint, coriander, fennel)',
                    'lunch': '11 AM-1 PM: Basmati rice or barley, Mung dal with cooling spices, Cucumber salad or coriander chutney, Sweet vegetables (zucchini, cucumber, leafy greens), Cooling lassi',
                    'evening': '4 PM: Fresh fruit juice or coconut water, Sweet fruits',
                    'dinner': '6-7 PM: Light meal with cooling foods, Vegetable soup or light khichdi, Steamed vegetables, Milk with cardamom'
                },
                'meal_guidelines': {
                    'temperature': 'Cool to room temperature foods',
                    'texture': 'Light, cooling, moist',
                    'timing': '11am-1pm: hearty, healthy lunch'
                },
                'foods_to_favor': 'Cool, heavy, oily foods; sweet, bitter, astringent tastes; milk, ghee, coconut, cucumber, leafy greens',
                'foods_to_avoid': 'Pungent and spicy foods; hot, sharp, acidic foods; tomatoes, garlic, chili, alcohol',
                'difficulty_level': 'beginner'
            },
            
            # 3. KAPHA IMBALANCE DIET PLAN
            {
                'name': 'Kapha Imbalance Diet Plan',
                'plan_type': 'dosha_balance',
                'target_dosha': 'Kapha',
                'conditions_treated': 'Weight gain, lethargy, congestion, slow digestion, depression',
                'principle': 'Balancing excess Kapha would involve having foods that are light, dry, rough',
                'daily_schedule': {
                    'early_morning': '6-7 AM: Warm water with honey and lemon, Ginger tea',
                    'breakfast': '7-8 AM: Light, warm foods, Barley porridge with warming spices, Herbal teas (ginger, cinnamon)',
                    'mid_morning': '10 AM: Spiced tea (no milk, minimal sweetener)',
                    'lunch': '12-1 PM: Light grains (barley, millet, quinoa), Pungent and bitter foods such as garlic, ginger, peaches, and pears, Bitter vegetables (bitter gourd, leafy greens), Minimal oil, maximum spices',
                    'evening': '4 PM: Herbal tea with warming spices, Avoid snacking if possible',
                    'dinner': '6-7 PM: Very light meal, Vegetable soup with heating spices, Steamed vegetables'
                },
                'meal_guidelines': {
                    'temperature': 'Warm, heating foods',
                    'texture': 'Light, dry, rough',
                    'timing': '6-8am: Light but fulfilling breakfast, 6-7pm: small to medium-size dinner'
                },
                'foods_to_favor': 'Light, dry, warm foods; pungent, bitter, astringent tastes; variety of spices; legumes, leafy greens',
                'foods_to_avoid': 'Heavy, oily, sweet foods; dairy, nuts, sweet fruits, cold foods',
                'difficulty_level': 'intermediate'
            },
            
            # 4. VATA-PITTA DUAL CONSTITUTION PLAN
            {
                'name': 'Vata-Pitta Dual Constitution Plan',
                'plan_type': 'dual_constitution',
                'target_dosha': 'Vata-Pitta',
                'conditions_treated': 'Mixed characteristics of both doshas',
                'principle': 'Balance both air/space and fire/water elements',
                'daily_schedule': {
                    'early_morning': '6-7 AM: Room temperature water with fresh lime, Soaked almonds',
                    'breakfast': '7-8 AM: Moderately warm, not too hot foods, Oats with mild spices and milk, Sweet fruits (ripe mangoes, sweet apples)',
                    'lunch': '12-1 PM: Basmati rice with sweet vegetables, Mung dal with moderate spices, Cooling vegetables prepared warmly, Lassi (not too cold)',
                    'dinner': '6-7 PM: Warm but not heated foods, Light khichdi with ghee, Cooked vegetables with mild seasoning'
                },
                'meal_guidelines': {
                    'temperature': 'Moderately warm',
                    'texture': 'Neither too dry nor too oily',
                    'timing': 'Regular meal schedules'
                },
                'foods_to_favor': 'Moderately warm foods, sweet taste, balanced moisture',
                'foods_to_avoid': 'Extremely hot or cold foods, excessive spices',
                'seasonal_adjustments': 'Summer: Follow more Pitta guidelines (cooling foods), Winter: Follow more Vata guidelines (warming foods)',
                'difficulty_level': 'intermediate'
            },
            
            # 5. VATA-KAPHA DUAL CONSTITUTION PLAN
            {
                'name': 'Vata-Kapha Dual Constitution Plan',
                'plan_type': 'dual_constitution',
                'target_dosha': 'Vata-Kapha',
                'conditions_treated': 'Mixed air/space and earth/water elements',
                'principle': 'Keep breakfast and dinner light and lunch the heaviest meal of the day',
                'daily_schedule': {
                    'early_morning': '6-7 AM: Warm water with ginger and honey',
                    'breakfast': '7-8 AM: Light but nourishing, Warm porridge with warming spices, Avoid heavy, cold foods',
                    'lunch': '12-1 PM: Warming, moderately heavy foods, Rice with well-spiced dal, Cooked vegetables with heating spices, Moderate amounts of ghee',
                    'dinner': '6-7 PM: Light and warm, Vegetable soup or light khichdi, Herbal tea'
                },
                'meal_guidelines': {
                    'temperature': 'Warm foods',
                    'texture': 'Light breakfast and dinner, substantial lunch',
                    'timing': 'Main meal at lunch'
                },
                'foods_to_favor': 'Warming, light to moderate foods, digestive spices',
                'foods_to_avoid': 'Heavy, cold foods especially at breakfast and dinner',
                'key_points': 'Eat only when you are hungry or better still when the previous meal has been digested',
                'difficulty_level': 'intermediate'
            },
            
            # 6. PITTA-KAPHA DUAL CONSTITUTION PLAN
            {
                'name': 'Pitta-Kapha Dual Constitution Plan',
                'plan_type': 'dual_constitution',
                'target_dosha': 'Pitta-Kapha',
                'conditions_treated': 'Mixed fire/water and earth/water elements',
                'principle': 'Balance heat and heaviness',
                'daily_schedule': {
                    'early_morning': '6-7 AM: Room temperature water with lemon, Light start to the day',
                    'breakfast': '7-8 AM: Moderate portions of cooling foods, Fresh fruits, light grains, Herbal teas',
                    'lunch': '11 AM-1 PM: Cooling but light foods, Barley or quinoa with cooling spices, Bitter and astringent vegetables, Minimal oil',
                    'dinner': '6-7 PM: Very light meal, Vegetable broth or light soup, Steamed vegetables'
                },
                'meal_guidelines': {
                    'temperature': 'Cool to room temperature',
                    'texture': 'Light, not oily',
                    'timing': 'Light meals throughout'
                },
                'foods_to_favor': 'Cooling, light, bitter and astringent foods',
                'foods_to_avoid': 'Heavy, oily, very hot foods',
                'seasonal_adjustments': 'Spring/Early Summer: More Kapha-reducing (light, dry, warm), Late Summer: More Pitta-reducing (cool, sweet)',
                'difficulty_level': 'advanced'
            },
            
            # 7. DIGESTIVE WEAKNESS (WEAK AGNI) PLAN
            {
                'name': 'Digestive Weakness (Weak Agni) Plan',
                'plan_type': 'therapeutic',
                'target_dosha': 'All doshas',
                'conditions_treated': 'Poor appetite, bloating, undigested food, fatigue after meals',
                'principle': 'Strengthen digestive fire with easy to digest foods and digestive spices',
                'daily_schedule': {
                    'early_morning': '6-7 AM: Warm water with fresh ginger juice and honey, Digestive tea (ginger, cumin, coriander)',
                    'breakfast': '8-9 AM: Easy to digest foods, Khichdi with minimal spices and ghee, Cooked fruits',
                    'lunch': '12-1 PM: Small portions, well-cooked, Mung dal soup, Steamed vegetables, Buttermilk with digestive spices',
                    'dinner': '6 PM - early: Very light, liquid foods, Vegetable broth, Herbal teas'
                },
                'meal_guidelines': {
                    'portion_size': 'Small, frequent meals',
                    'preparation': 'Well-cooked, easy to digest',
                    'timing': 'Eat only when hungry'
                },
                'foods_to_favor': 'Digestive spices: ginger, cumin, fennel; Well-cooked, warm foods',
                'foods_to_avoid': 'Raw, cold, heavy foods; Large portions',
                'key_points': 'Eat only when hungry, Small, frequent meals, Avoid raw, cold, heavy foods, Include digestive spices: ginger, cumin, fennel',
                'difficulty_level': 'intermediate'
            },
            
            # 8. HIGH BLOOD PRESSURE (PITTA-VATA) PLAN
            {
                'name': 'High Blood Pressure (Pitta-Vata) Plan',
                'plan_type': 'therapeutic',
                'target_dosha': 'Pitta-Vata',
                'conditions_treated': 'Hypertension, stress, anxiety with heat symptoms',
                'principle': 'Cool and calm both Pitta and Vata with cooling, grounding foods',
                'daily_schedule': {
                    'early_morning': '6-7 AM: Room temperature water, Fresh coconut water',
                    'breakfast': '7-8 AM: Cooling, calming foods, Oats with milk and cardamom, Sweet, ripe fruits',
                    'lunch': '12-1 PM: Cooling vegetables (cucumber, bottle gourd), Basmati rice, Mung dal with minimal salt, Cooling herbs: coriander, mint',
                    'dinner': '6-7 PM: Very light, cooling meal, Vegetable soup (low salt), Steamed vegetables, Herbal teas (hibiscus, fennel)'
                },
                'meal_guidelines': {
                    'salt': 'Minimal salt intake',
                    'temperature': 'Cool to room temperature',
                    'herbs': 'Cooling herbs like coriander, mint'
                },
                'foods_to_favor': 'Potassium-rich foods, cooling herbs, stress-reducing practices',
                'foods_to_avoid': 'Excessive salt, spicy foods, caffeine, alcohol',
                'therapeutic_foods': 'Cucumber, bottle gourd, coconut water, hibiscus tea',
                'difficulty_level': 'intermediate'
            },
            
            # 9. DIABETES MANAGEMENT (KAPHA-PITTA) PLAN
            {
                'name': 'Diabetes Management (Kapha-Pitta) Plan',
                'plan_type': 'therapeutic',
                'target_dosha': 'Kapha-Pitta',
                'conditions_treated': 'Blood sugar regulation, weight management',
                'principle': 'Use bitter, astringent tastes to balance blood sugar and reduce Kapha',
                'daily_schedule': {
                    'early_morning': '6-7 AM: Warm water with bitter herbs (neem, fenugreek), Herbal tea without sugar',
                    'breakfast': '8 AM: High fiber, low glycemic foods, Barley porridge with cinnamon, Bitter vegetables',
                    'lunch': '12-1 PM: Complex carbs in moderation, Quinoa or millet, Plenty of bitter and astringent vegetables, Legumes for protein',
                    'dinner': '6 PM: Very light, early dinner, Vegetable soup, Minimal grains'
                },
                'meal_guidelines': {
                    'carbohydrates': 'Complex carbs in moderation',
                    'fiber': 'High fiber foods',
                    'glycemic_index': 'Low glycemic foods preferred'
                },
                'foods_to_favor': 'Bitter gourd, fenugreek, turmeric, cinnamon, leafy greens',
                'foods_to_avoid': 'Sweet, oily, heavy foods; refined carbs; fruits high in sugar',
                'therapeutic_foods': 'Bitter gourd, fenugreek, turmeric, cinnamon',
                'difficulty_level': 'intermediate'
            },
            
            # 10. WEIGHT LOSS (KAPHA REDUCTION) PLAN
            {
                'name': 'Weight Loss (Kapha Reduction) Plan',
                'plan_type': 'therapeutic',
                'target_dosha': 'Kapha',
                'conditions_treated': 'Obesity, slow metabolism, water retention',
                'principle': 'Reduce Kapha with heating, light, dry foods and spices',
                'daily_schedule': {
                    'early_morning': '6 AM: Hot water with honey and lemon, Ginger tea',
                    'breakfast': '8 AM: Light, warming foods, Spiced barley porridge (minimal ghee), Herbal teas',
                    'lunch': '12-1 PM: Heating spices with light grains, Millet or quinoa, Bitter vegetables (bitter gourd, leafy greens), Legumes (mung dal, horse gram)',
                    'dinner': '6 PM: Minimal, early dinner, Clear vegetable broth, Steamed vegetables with spices'
                },
                'meal_guidelines': {
                    'portion_size': 'Small portions',
                    'timing': 'Early dinner',
                    'spices': 'Heating spices essential'
                },
                'foods_to_favor': 'Bitter, pungent, astringent tastes; Heating spices: ginger, black pepper, turmeric',
                'foods_to_avoid': 'Sweet, sour, salty; heavy, oily foods',
                'key_points': 'Favor bitter, pungent, astringent tastes, Heating spices: ginger, black pepper, turmeric, Avoid sweet, sour, salty; heavy, oily foods, Regular exercise essential',
                'difficulty_level': 'advanced'
            },
            
            # 11. RESPIRATORY ISSUES (KAPHA IN LUNGS) PLAN
            {
                'name': 'Respiratory Issues (Kapha in Lungs) Plan',
                'plan_type': 'therapeutic',
                'target_dosha': 'Kapha',
                'conditions_treated': 'Congestion, cough, asthma, bronchitis',
                'principle': 'Clear Kapha from lungs with heating, expectorant foods',
                'daily_schedule': {
                    'early_morning': '6 AM: Hot water with ginger and honey, Steam inhalation with eucalyptus',
                    'breakfast': '8 AM: Warm, light foods, Ginger tea with tulsi, Avoid dairy and cold foods',
                    'lunch': '12-1 PM: Heating, drying foods, Light grains with expectorant spices, Garlic, onion, ginger in cooking, Avoid mucus-forming foods',
                    'dinner': '6 PM: Light, warm meal, Spiced vegetable soup, Herbal teas (ginger, tulsi, licorice)'
                },
                'meal_guidelines': {
                    'temperature': 'Warm, heating foods',
                    'spices': 'Expectorant spices like ginger, garlic',
                    'dairy': 'Avoid dairy completely'
                },
                'foods_to_favor': 'Garlic, ginger, turmeric, black pepper, honey',
                'foods_to_avoid': 'Dairy, cold foods, sweet fruits, refined sugar',
                'therapeutic_foods': 'Garlic, ginger, turmeric, black pepper, honey',
                'difficulty_level': 'intermediate'
            },
            
            # 12. SKIN DISORDERS (PITTA IN BLOOD) PLAN  
            {
                'name': 'Skin Disorders (Pitta in Blood) Plan',
                'plan_type': 'therapeutic',
                'target_dosha': 'Pitta',
                'conditions_treated': 'Acne, eczema, psoriasis, inflammatory skin conditions',
                'principle': 'Cool and purify the blood with cooling, bitter foods',
                'daily_schedule': {
                    'early_morning': '6 AM: Cool water with aloe vera juice, Neem tea (bitter but purifying)',
                    'breakfast': '8 AM: Cooling, blood-purifying foods, Fresh fruits (not citrus), Coconut water',
                    'lunch': '12-1 PM: Cooling vegetables, Leafy greens, cucumber, bottle gourd, Coconut-based preparations, Avoid heating spices',
                    'dinner': '6 PM: Light, cooling meal, Steamed vegetables, Herbal teas (neem, manjistha)'
                },
                'meal_guidelines': {
                    'temperature': 'Cool foods',
                    'preparation': 'Minimal heating spices',
                    'focus': 'Blood purifying foods'
                },
                'foods_to_favor': 'Neem, turmeric, aloe vera, cilantro, coconut',
                'foods_to_avoid': 'Spicy, sour, fermented, fried foods; excessive salt',
                'therapeutic_foods': 'Neem, turmeric, aloe vera, cilantro, coconut',
                'difficulty_level': 'intermediate'
            },
            
            # 13. ANXIETY & INSOMNIA (VATA NERVOUS SYSTEM) PLAN
            {
                'name': 'Anxiety & Insomnia (Vata Nervous System) Plan',
                'plan_type': 'therapeutic',
                'target_dosha': 'Vata',
                'conditions_treated': 'Mental restlessness, sleep disorders, nervous system imbalance',
                'principle': 'Ground and nourish the nervous system with heavy, oily, sweet foods',
                'daily_schedule': {
                    'early_morning': '6 AM: Warm milk with nutmeg and cardamom, Calming herbal tea',
                    'breakfast': '8 AM: Nourishing, grounding foods, Warm oats with ghee and dates, Soaked almonds',
                    'lunch': '12-1 PM: Heavy, oily, sweet foods in moderation, Rice with well-cooked vegetables, Ghee and warming spices, Avoid stimulating foods',
                    'dinner': '7 PM: Early, warm, light dinner, Warm milk with ashwagandha, Avoid caffeine completely'
                },
                'meal_guidelines': {
                    'texture': 'Heavy, oily, nourishing',
                    'timing': 'Regular, early dinner',
                    'stimulants': 'Avoid all caffeine'
                },
                'foods_to_favor': 'Almonds, dates, ghee, warm milk, ashwagandha, brahmi',
                'foods_to_avoid': 'Caffeine, alcohol, raw foods, excessive stimulation',
                'therapeutic_foods': 'Almonds, dates, ghee, warm milk, ashwagandha, brahmi',
                'difficulty_level': 'beginner'
            },
            
            # 14. MENSTRUAL DISORDERS (HORMONAL BALANCE) PLAN
            {
                'name': 'Menstrual Disorders (Hormonal Balance) Plan',
                'plan_type': 'therapeutic',
                'target_dosha': 'Vata-Pitta',
                'conditions_treated': 'Irregular cycles, PMS, hormonal imbalances',
                'principle': 'Nourish reproductive tissues with hormone-supporting foods',
                'daily_schedule': {
                    'early_morning': '6 AM: Warm water with fennel seeds, Herbal tea (shatavari, rose)',
                    'breakfast': '8 AM: Hormone-supporting foods, Warm porridge with sesame seeds, Fresh dates and figs',
                    'lunch': '12-1 PM: Iron and calcium-rich foods, Sesame-based preparations, Dark leafy greens, Moderate amounts of ghee',
                    'dinner': '6 PM: Nourishing but light, Warm milk with saffron, Avoid cold, raw foods'
                },
                'meal_guidelines': {
                    'nutrients': 'Iron and calcium rich',
                    'temperature': 'Warm, nourishing',
                    'timing': 'Regular meal schedules'
                },
                'foods_to_favor': 'Sesame seeds, shatavari, rose, fennel, dates, ghee',
                'foods_to_avoid': 'Cold, raw foods during menstruation',
                'therapeutic_foods': 'Sesame seeds, shatavari, rose, fennel, dates, ghee',
                'key_points': 'Menstrual Phase: Extra iron from leafy greens, warm, nourishing foods',
                'difficulty_level': 'intermediate'
            },
            
            # 15. GENERAL DETOX & REJUVENATION PLAN
            {
                'name': 'General Detox & Rejuvenation Plan',
                'plan_type': 'detox',
                'target_dosha': 'All doshas',
                'conditions_treated': 'Seasonal cleansing, overall health maintenance',
                'principle': 'Systematic cleansing and rebuilding with simple, pure foods',
                'daily_schedule': {
                    'days_1_3': 'Preparation: Eliminate heavy, processed foods, Light, easily digestible meals, Increase water intake with lemon',
                    'days_4_5': 'Active Detox: Khichdi mono-diet (mung dal and rice), Herbal teas (ginger, cumin, coriander), Triphala before bed',
                    'days_6_7': 'Rebuilding: Gradually introduce normal foods, Focus on fresh, cooked vegetables, Digestive spices and probiotics'
                },
                'meal_guidelines': {
                    'phase_1': 'Preparation - light foods',
                    'phase_2': 'Active detox - khichdi mono-diet',
                    'phase_3': 'Rebuilding - gradual food introduction'
                },
                'foods_to_favor': 'Mung dal, basmati rice, fresh vegetables, herbal teas, triphala, fresh ginger',
                'foods_to_avoid': 'Processed foods, caffeine, alcohol during detox period',
                'key_points': 'Oil massage (abhyanga), Yoga and meditation, Early sleep and wake times, Avoid processed foods, caffeine, alcohol',
                'therapeutic_foods': 'Mung dal, basmati rice, fresh vegetables, herbal teas, triphala, fresh ginger',
                'difficulty_level': 'advanced'
            }
        ]

        for plan_data in diet_plans_data:
            plan, created = DietPlanTemplate.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(f"Created diet plan template: {plan.name}")
            else:
                self.stdout.write(f"Diet plan template already exists: {plan.name}")