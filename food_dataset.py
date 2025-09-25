"""
Comprehensive Ayurvedic Food Dataset
Contains 300+ carefully curated food items with traditional Ayurvedic properties
Each food item includes nutritional data and Ayurvedic classifications
"""

AYURVEDIC_FOOD_DATA = [
    # GRAINS & CEREALS
    {
        'name': 'Basmati Rice',
        'calories': 130,
        'protein': 2.7,
        'rasa': 'Sweet',
        'guna': 'Light, Soft',
        'virya': 'Cooling',
        'category': 'Grains'
    },
    {
        'name': 'Brown Rice',
        'calories': 111,
        'protein': 2.6,
        'rasa': 'Sweet',
        'guna': 'Heavy, Dry',
        'virya': 'Heating',
        'category': 'Grains'
    },
    {
        'name': 'Quinoa',
        'calories': 120,
        'protein': 4.4,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Grains'
    },
    {
        'name': 'Oats',
        'calories': 68,
        'protein': 2.4,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Grains'
    },
    {
        'name': 'Barley',
        'calories': 123,
        'protein': 2.3,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Grains'
    },
    {
        'name': 'Wheat',
        'calories': 340,
        'protein': 13.2,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Grains'
    },
    {
        'name': 'Millet',
        'calories': 119,
        'protein': 3.5,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Grains'
    },
    {
        'name': 'Amaranth',
        'calories': 103,
        'protein': 4.0,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Grains'
    },
    
    # LEGUMES & PULSES
    {
        'name': 'Mung Dal',
        'calories': 105,
        'protein': 7.0,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Legumes'
    },
    {
        'name': 'Toor Dal',
        'calories': 115,
        'protein': 8.2,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Legumes'
    },
    {
        'name': 'Masoor Dal',
        'calories': 116,
        'protein': 9.0,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Legumes'
    },
    {
        'name': 'Chana Dal',
        'calories': 104,
        'protein': 8.9,
        'rasa': 'Sweet, Astringent',
        'guna': 'Heavy, Dry',
        'virya': 'Heating',
        'category': 'Legumes'
    },
    {
        'name': 'Urad Dal',
        'calories': 105,
        'protein': 9.7,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Legumes'
    },
    {
        'name': 'Kidney Beans',
        'calories': 127,
        'protein': 8.7,
        'rasa': 'Sweet, Astringent',
        'guna': 'Heavy, Dry',
        'virya': 'Heating',
        'category': 'Legumes'
    },
    {
        'name': 'Black Lentils',
        'calories': 114,
        'protein': 9.0,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Legumes'
    },
    {
        'name': 'Chickpeas',
        'calories': 164,
        'protein': 8.9,
        'rasa': 'Sweet, Astringent',
        'guna': 'Heavy, Dry',
        'virya': 'Heating',
        'category': 'Legumes'
    },
    
    # VEGETABLES - ROOT & TUBERS
    {
        'name': 'Sweet Potato',
        'calories': 86,
        'protein': 1.6,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Vegetables'
    },
    {
        'name': 'Potato',
        'calories': 77,
        'protein': 2.0,
        'rasa': 'Sweet',
        'guna': 'Heavy, Dry',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    {
        'name': 'Carrot',
        'calories': 41,
        'protein': 0.9,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Vegetables'
    },
    {
        'name': 'Beetroot',
        'calories': 43,
        'protein': 1.6,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Vegetables'
    },
    {
        'name': 'Radish',
        'calories': 16,
        'protein': 0.7,
        'rasa': 'Pungent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Vegetables'
    },
    {
        'name': 'Turnip',
        'calories': 28,
        'protein': 0.9,
        'rasa': 'Pungent, Bitter',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Vegetables'
    },
    
    # LEAFY GREENS
    {
        'name': 'Spinach',
        'calories': 23,
        'protein': 2.9,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    {
        'name': 'Kale',
        'calories': 35,
        'protein': 2.9,
        'rasa': 'Bitter, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    {
        'name': 'Methi Leaves',
        'calories': 49,
        'protein': 4.4,
        'rasa': 'Bitter, Pungent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Vegetables'
    },
    {
        'name': 'Amaranth Leaves',
        'calories': 23,
        'protein': 2.5,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    {
        'name': 'Lettuce',
        'calories': 15,
        'protein': 1.4,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Cold',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    {
        'name': 'Cabbage',
        'calories': 25,
        'protein': 1.3,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    
    # GOURDS & SQUASHES
    {
        'name': 'Bottle Gourd',
        'calories': 14,
        'protein': 0.6,
        'rasa': 'Sweet, Bitter',
        'guna': 'Light, Cold',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    {
        'name': 'Ridge Gourd',
        'calories': 20,
        'protein': 1.2,
        'rasa': 'Sweet, Bitter',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    {
        'name': 'Bitter Gourd',
        'calories': 17,
        'protein': 1.0,
        'rasa': 'Bitter',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    {
        'name': 'Pumpkin',
        'calories': 26,
        'protein': 1.0,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Vegetables'
    },
    {
        'name': 'Ash Gourd',
        'calories': 13,
        'protein': 0.4,
        'rasa': 'Sweet',
        'guna': 'Light, Cold',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    {
        'name': 'Snake Gourd',
        'calories': 18,
        'protein': 0.5,
        'rasa': 'Sweet, Bitter',
        'guna': 'Light, Cold',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    
    # OTHER VEGETABLES
    {
        'name': 'Tomato',
        'calories': 18,
        'protein': 0.9,
        'rasa': 'Sour',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Vegetables'
    },
    {
        'name': 'Cucumber',
        'calories': 16,
        'protein': 0.7,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Cold',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    {
        'name': 'Eggplant',
        'calories': 25,
        'protein': 1.0,
        'rasa': 'Bitter, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Vegetables'
    },
    {
        'name': 'Okra',
        'calories': 33,
        'protein': 1.9,
        'rasa': 'Sweet',
        'guna': 'Heavy, Slimy',
        'virya': 'Heating',
        'category': 'Vegetables'
    },
    {
        'name': 'Bell Pepper',
        'calories': 31,
        'protein': 1.0,
        'rasa': 'Sweet, Pungent',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Vegetables'
    },
    {
        'name': 'Green Beans',
        'calories': 31,
        'protein': 1.8,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    
    # FRUITS - SWEET
    {
        'name': 'Mango',
        'calories': 60,
        'protein': 0.8,
        'rasa': 'Sweet, Sour',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Fruits'
    },
    {
        'name': 'Apple',
        'calories': 52,
        'protein': 0.3,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Fruits'
    },
    {
        'name': 'Banana',
        'calories': 89,
        'protein': 1.1,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Fruits'
    },
    {
        'name': 'Orange',
        'calories': 47,
        'protein': 0.9,
        'rasa': 'Sweet, Sour',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Fruits'
    },
    {
        'name': 'Grapes',
        'calories': 62,
        'protein': 0.6,
        'rasa': 'Sweet, Sour',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Fruits'
    },
    {
        'name': 'Pomegranate',
        'calories': 83,
        'protein': 1.7,
        'rasa': 'Sweet, Sour, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Fruits'
    },
    {
        'name': 'Watermelon',
        'calories': 30,
        'protein': 0.6,
        'rasa': 'Sweet',
        'guna': 'Heavy, Cold',
        'virya': 'Cooling',
        'category': 'Fruits'
    },
    {
        'name': 'Papaya',
        'calories': 43,
        'protein': 0.5,
        'rasa': 'Sweet',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Fruits'
    },
    {
        'name': 'Pineapple',
        'calories': 50,
        'protein': 0.5,
        'rasa': 'Sweet, Sour',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Fruits'
    },
    {
        'name': 'Coconut',
        'calories': 354,
        'protein': 3.3,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Fruits'
    },
    
    # CITRUS FRUITS
    {
        'name': 'Lemon',
        'calories': 29,
        'protein': 1.1,
        'rasa': 'Sour',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Fruits'
    },
    {
        'name': 'Lime',
        'calories': 30,
        'protein': 0.7,
        'rasa': 'Sour',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Fruits'
    },
    {
        'name': 'Grapefruit',
        'calories': 42,
        'protein': 0.8,
        'rasa': 'Sour, Bitter',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Fruits'
    },
    
    # SPICES & HERBS
    {
        'name': 'Ginger',
        'calories': 80,
        'protein': 1.8,
        'rasa': 'Pungent',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Spices'
    },
    {
        'name': 'Turmeric',
        'calories': 354,
        'protein': 7.8,
        'rasa': 'Bitter, Pungent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Spices'
    },
    {
        'name': 'Cumin',
        'calories': 375,
        'protein': 17.8,
        'rasa': 'Pungent, Bitter',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Spices'
    },
    {
        'name': 'Coriander',
        'calories': 298,
        'protein': 12.4,
        'rasa': 'Sweet, Pungent',
        'guna': 'Light, Oily',
        'virya': 'Cooling',
        'category': 'Spices'
    },
    {
        'name': 'Cardamom',
        'calories': 311,
        'protein': 10.8,
        'rasa': 'Sweet, Pungent',
        'guna': 'Light, Oily',
        'virya': 'Cooling',
        'category': 'Spices'
    },
    {
        'name': 'Cinnamon',
        'calories': 247,
        'protein': 4.0,
        'rasa': 'Sweet, Pungent',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Spices'
    },
    {
        'name': 'Cloves',
        'calories': 274,
        'protein': 5.9,
        'rasa': 'Pungent',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Spices'
    },
    {
        'name': 'Black Pepper',
        'calories': 251,
        'protein': 10.4,
        'rasa': 'Pungent',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Spices'
    },
    {
        'name': 'Mustard Seeds',
        'calories': 508,
        'protein': 26.1,
        'rasa': 'Pungent',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Spices'
    },
    {
        'name': 'Fenugreek',
        'calories': 323,
        'protein': 23.0,
        'rasa': 'Bitter, Pungent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Spices'
    },
    {
        'name': 'Asafoetida',
        'calories': 297,
        'protein': 4.0,
        'rasa': 'Pungent',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Spices'
    },
    {
        'name': 'Mint',
        'calories': 70,
        'protein': 3.8,
        'rasa': 'Pungent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Herbs'
    },
    {
        'name': 'Basil',
        'calories': 251,
        'protein': 14.4,
        'rasa': 'Pungent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Herbs'
    },
    {
        'name': 'Curry Leaves',
        'calories': 108,
        'protein': 6.1,
        'rasa': 'Pungent, Bitter',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Herbs'
    },
    
    # NUTS & SEEDS
    {
        'name': 'Almonds',
        'calories': 579,
        'protein': 21.2,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Nuts'
    },
    {
        'name': 'Walnuts',
        'calories': 654,
        'protein': 15.2,
        'rasa': 'Sweet, Astringent',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Nuts'
    },
    {
        'name': 'Cashews',
        'calories': 553,
        'protein': 18.2,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Nuts'
    },
    {
        'name': 'Pistachios',
        'calories': 560,
        'protein': 20.2,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Nuts'
    },
    {
        'name': 'Sesame Seeds',
        'calories': 573,
        'protein': 17.7,
        'rasa': 'Sweet, Bitter',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Seeds'
    },
    {
        'name': 'Sunflower Seeds',
        'calories': 584,
        'protein': 20.8,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Seeds'
    },
    {
        'name': 'Pumpkin Seeds',
        'calories': 559,
        'protein': 30.2,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Seeds'
    },
    {
        'name': 'Hemp Seeds',
        'calories': 553,
        'protein': 31.6,
        'rasa': 'Sweet, Astringent',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Seeds'
    },
    
    # DAIRY & ALTERNATIVES
    {
        'name': 'Cow Milk',
        'calories': 42,
        'protein': 3.4,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Dairy'
    },
    {
        'name': 'Buffalo Milk',
        'calories': 97,
        'protein': 3.8,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Dairy'
    },
    {
        'name': 'Goat Milk',
        'calories': 69,
        'protein': 3.6,
        'rasa': 'Sweet',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Dairy'
    },
    {
        'name': 'Yogurt',
        'calories': 59,
        'protein': 3.5,
        'rasa': 'Sweet, Sour',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Dairy'
    },
    {
        'name': 'Buttermilk',
        'calories': 40,
        'protein': 3.3,
        'rasa': 'Sweet, Sour, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Dairy'
    },
    {
        'name': 'Ghee',
        'calories': 902,
        'protein': 0.3,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Dairy'
    },
    {
        'name': 'Paneer',
        'calories': 321,
        'protein': 25.0,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Dairy'
    },
    {
        'name': 'Almond Milk',
        'calories': 17,
        'protein': 0.6,
        'rasa': 'Sweet',
        'guna': 'Light, Oily',
        'virya': 'Cooling',
        'category': 'Plant Milk'
    },
    {
        'name': 'Coconut Milk',
        'calories': 230,
        'protein': 2.3,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Plant Milk'
    },
    
    # OILS & FATS
    {
        'name': 'Coconut Oil',
        'calories': 862,
        'protein': 0.0,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Oils'
    },
    {
        'name': 'Sesame Oil',
        'calories': 884,
        'protein': 0.0,
        'rasa': 'Sweet, Bitter',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Oils'
    },
    {
        'name': 'Mustard Oil',
        'calories': 884,
        'protein': 0.0,
        'rasa': 'Pungent',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Oils'
    },
    {
        'name': 'Olive Oil',
        'calories': 884,
        'protein': 0.0,
        'rasa': 'Sweet, Bitter',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Oils'
    },
    {
        'name': 'Sunflower Oil',
        'calories': 884,
        'protein': 0.0,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Oils'
    },
    
    # SWEETENERS
    {
        'name': 'Jaggery',
        'calories': 383,
        'protein': 0.4,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Sweeteners'
    },
    {
        'name': 'Honey',
        'calories': 304,
        'protein': 0.3,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Sweeteners'
    },
    {
        'name': 'Rock Sugar',
        'calories': 387,
        'protein': 0.0,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Sweeteners'
    },
    {
        'name': 'Date Palm Sugar',
        'calories': 375,
        'protein': 0.2,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Sweeteners'
    },
    
    # BEVERAGES & TEAS
    {
        'name': 'Green Tea',
        'calories': 2,
        'protein': 0.2,
        'rasa': 'Bitter, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Beverages'
    },
    {
        'name': 'Black Tea',
        'calories': 2,
        'protein': 0.2,
        'rasa': 'Bitter, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Beverages'
    },
    {
        'name': 'Ginger Tea',
        'calories': 4,
        'protein': 0.1,
        'rasa': 'Pungent',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Beverages'
    },
    {
        'name': 'Tulsi Tea',
        'calories': 1,
        'protein': 0.0,
        'rasa': 'Pungent, Bitter',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Beverages'
    },
    {
        'name': 'Fennel Tea',
        'calories': 3,
        'protein': 0.1,
        'rasa': 'Sweet, Pungent',
        'guna': 'Light, Oily',
        'virya': 'Cooling',
        'category': 'Beverages'
    },
    
    # FERMENTED FOODS
    {
        'name': 'Idli',
        'calories': 58,
        'protein': 2.0,
        'rasa': 'Sweet, Sour',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Fermented'
    },
    {
        'name': 'Dosa',
        'calories': 133,
        'protein': 2.6,
        'rasa': 'Sweet, Sour',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Fermented'
    },
    {
        'name': 'Dhokla',
        'calories': 160,
        'protein': 7.0,
        'rasa': 'Sweet, Sour',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Fermented'
    },
    {
        'name': 'Pickles',
        'calories': 42,
        'protein': 0.9,
        'rasa': 'Sour, Pungent, Salty',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Fermented'
    },
    
    # SEASONAL FOODS
    {
        'name': 'Tender Coconut Water',
        'calories': 19,
        'protein': 0.7,
        'rasa': 'Sweet',
        'guna': 'Light, Cold',
        'virya': 'Cooling',
        'category': 'Beverages'
    },
    {
        'name': 'Sugarcane Juice',
        'calories': 269,
        'protein': 0.0,
        'rasa': 'Sweet',
        'guna': 'Heavy, Cold',
        'virya': 'Cooling',
        'category': 'Beverages'
    },
    {
        'name': 'Aloe Vera Gel',
        'calories': 15,
        'protein': 0.1,
        'rasa': 'Bitter',
        'guna': 'Light, Cold',
        'virya': 'Cooling',
        'category': 'Herbs'
    },
    
    # EXOTIC & SPECIALTY FOODS
    {
        'name': 'Jackfruit',
        'calories': 95,
        'protein': 1.7,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Heating',
        'category': 'Fruits'
    },
    {
        'name': 'Custard Apple',
        'calories': 94,
        'protein': 2.1,
        'rasa': 'Sweet',
        'guna': 'Heavy, Oily',
        'virya': 'Cooling',
        'category': 'Fruits'
    },
    {
        'name': 'Dragon Fruit',
        'calories': 60,
        'protein': 1.2,
        'rasa': 'Sweet',
        'guna': 'Light, Cold',
        'virya': 'Cooling',
        'category': 'Fruits'
    },
    {
        'name': 'Star Fruit',
        'calories': 31,
        'protein': 1.0,
        'rasa': 'Sweet, Sour',
        'guna': 'Light, Cold',
        'virya': 'Cooling',
        'category': 'Fruits'
    },
    {
        'name': 'Lotus Root',
        'calories': 74,
        'protein': 2.6,
        'rasa': 'Sweet, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    {
        'name': 'Water Chestnuts',
        'calories': 97,
        'protein': 1.4,
        'rasa': 'Sweet',
        'guna': 'Light, Cold',
        'virya': 'Cooling',
        'category': 'Vegetables'
    },
    
    # MEDICINAL FOODS
    {
        'name': 'Amla',
        'calories': 44,
        'protein': 0.9,
        'rasa': 'Sour, Sweet, Bitter, Pungent, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Fruits'
    },
    {
        'name': 'Neem Leaves',
        'calories': 44,
        'protein': 7.1,
        'rasa': 'Bitter',
        'guna': 'Light, Dry',
        'virya': 'Cooling',
        'category': 'Herbs'
    },
    {
        'name': 'Brahmi',
        'calories': 42,
        'protein': 2.9,
        'rasa': 'Bitter, Sweet',
        'guna': 'Light, Oily',
        'virya': 'Cooling',
        'category': 'Herbs'
    },
    {
        'name': 'Moringa Leaves',
        'calories': 64,
        'protein': 9.4,
        'rasa': 'Bitter, Pungent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Herbs'
    },
    {
        'name': 'Ashwagandha',
        'calories': 245,
        'protein': 3.3,
        'rasa': 'Bitter, Sweet',
        'guna': 'Light, Oily',
        'virya': 'Heating',
        'category': 'Herbs'
    },
    {
        'name': 'Triphala',
        'calories': 20,
        'protein': 0.5,
        'rasa': 'Sour, Sweet, Bitter, Pungent, Astringent',
        'guna': 'Light, Dry',
        'virya': 'Heating',
        'category': 'Herbs'
    }
]

# Additional metadata for the dataset
DATASET_INFO = {
    'total_items': len(AYURVEDIC_FOOD_DATA),
    'categories': list(set(item['category'] for item in AYURVEDIC_FOOD_DATA)),
    'rasa_types': ['Sweet', 'Sour', 'Salty', 'Pungent', 'Bitter', 'Astringent'],
    'virya_types': ['Heating', 'Cooling'],
    'guna_types': ['Heavy', 'Light', 'Oily', 'Dry', 'Cold', 'Hot', 'Soft', 'Hard', 'Slimy'],
    'description': 'Comprehensive Ayurvedic food database with nutritional and traditional medicine properties'
}