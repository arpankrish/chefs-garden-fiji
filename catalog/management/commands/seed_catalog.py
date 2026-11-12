import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from catalog.models import Category, Microgreen, WholesaleInquiry


class Command(BaseCommand):
    help = "Seeds initial admin account, categories, microgreen varieties, and sample inquiries for Chefs Garden Fiji."

    def handle(self, *args, **options):
        User = get_user_model()
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@chefsgardenfiji.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'chefsfiji2026')

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{admin_username}'"))
        else:
            self.stdout.write(f"Superuser '{admin_username}' already exists.")

        categories_data = [
            {
                'name': 'Vibrant Showstoppers & Earthy',
                'slug': 'vibrant-showstoppers',
                'description': 'High-contrast magenta, ruby, and deep crimson microgreens prized for visual drama and earthy mineral sweetness.',
                'badge_color': 'crimson',
                'display_order': 1,
            },
            {
                'name': 'Brassicas & Spicy Heat',
                'slug': 'brassicas-spicy',
                'description': 'Crisp, peppery, and horseradish-forward brassica microgreens that cut through rich coconut cream and seared proteins.',
                'badge_color': 'violet',
                'display_order': 2,
            },
            {
                'name': 'Delicate Shoots & Tendrils',
                'slug': 'shoots-tendrils',
                'description': 'Architectural curly tendrils and succulent shoots offering structural height, sweet crunch, and lush emerald volume.',
                'badge_color': 'emerald',
                'display_order': 3,
            },
            {
                'name': 'Aromatic Culinary Herbs',
                'slug': 'aromatic-herbs',
                'description': 'Concentrated essential-oil micro-herbs bursting with citrus, anise, and tropical botanical aromatics.',
                'badge_color': 'gold',
                'display_order': 4,
            },
        ]

        category_map = {}
        for cat_info in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=cat_info['slug'],
                defaults=cat_info
            )
            category_map[cat_info['slug']] = cat

        if Microgreen.objects.count() == 0:
            varieties_data = [
                {
                    'name': 'Red Garnet Amaranth',
                    'scientific_name': 'Amaranthus tricolor',
                    'slug': 'red-garnet-amaranth',
                    'category': category_map['vibrant-showstoppers'],
                    'tagline': 'Electric neon-magenta stems and delicate ruby leaves with a clean, sweet beetroot finish.',
                    'description': (
                        'Grown under filtered tropical highland light in our Nadi climate-controlled grow rooms, Red Garnet Amaranth '
                        'is the ultimate visual garnish for fine-dining plates across Fiji. Its translucent magenta stems catch the light '
                        'effortlessly, adding instant colour contrast against white coconut emulsions, seared scallops, and cured reef fish.'
                    ),
                    'primary_image': 'products/red-garnet-amaranth.jpg',
                    'flavor_profile': 'Earthy Beetroot, Sweet Mineral, Delicate Velvet Finish',
                    'intensity_level': Microgreen.Intensity.DELICATE,
                    'texture_notes': 'Feather-light cotyledons with tender, delicate crimson stems',
                    'culinary_pairings': 'Fijian Kokoda (Ceviche), Seared Yellowfin Tuna, Goat Cheese & Beet Tart, Coconut Panna Cotta',
                    'chef_serving_tip': 'Plate dry with precision tweezers at the pass; avoid submerging in hot jus to preserve electric magenta pigment.',
                    'availability_status': Microgreen.Availability.AVAILABLE,
                    'grow_cycle_days': 12,
                    'lead_time_notice': 'Dawn harvest daily; chilled delivery to Denarau, Nadi & Mamanuca ferries by 9:30 AM.',
                    'price_punnet_fjd': 14.50,
                    'punnet_weight_grams': '35g Chef Clam-Shell Punnet',
                    'price_tray_fjd': 54.00,
                    'tray_size_label': 'Live 10x20" Chef Tray (~180g yield)',
                    'nutritional_highlights': 'Exceptionally rich in betalain antioxidants, Vitamin K, Vitamin C, plant iron, and folate.',
                    'storage_instructions': 'Store unwashed in sealed punnet at 3°C–5°C with moisture pad. Avoid excess condensation.',
                    'shelf_life_days': 8,
                    'is_featured': True,
                    'is_active': True,
                    'display_order': 1,
                },
                {
                    'name': 'Rambo Purple Radish',
                    'scientific_name': 'Raphanus sativus',
                    'slug': 'rambo-purple-radish',
                    'category': category_map['brassicas-spicy'],
                    'tagline': 'Deep royal-violet leaves with a bold, clean peppery radish bite and crisp structural crunch.',
                    'description': (
                        'A staple in resort degustation kitchens, our Rambo Purple Radish delivers an immediate burst of fresh daikon-radish '
                        'spice followed by a clean, nutty finish. Its sturdy royal-purple cotyledons hold up admirably under warm proteins '
                        'and citrus vinaigrettes without wilting.'
                    ),
                    'primary_image': 'products/rambo-purple-radish.jpg',
                    'flavor_profile': 'Zesty Peppery Radish, Crisp Brassica Bite, Nutty Undertone',
                    'intensity_level': Microgreen.Intensity.BOLD,
                    'texture_notes': 'Succulent, snappy stems with firm violet heart-shaped leaves',
                    'culinary_pairings': 'Wagyu Beef Carpaccio, Coral Trout Crudo, Smoked Duck Breast, Avocado & Lime Tostadas',
                    'chef_serving_tip': 'Excellent structural garnish that withstands citrus dressings for up to 25 minutes on plated dishes.',
                    'availability_status': Microgreen.Availability.AVAILABLE,
                    'grow_cycle_days': 8,
                    'lead_time_notice': 'Harvested daily at 5:30 AM; available for same-day Nadi/Denarau dispatch.',
                    'price_punnet_fjd': 12.00,
                    'punnet_weight_grams': '45g Chef Clam-Shell Punnet',
                    'price_tray_fjd': 46.00,
                    'tray_size_label': 'Live 10x20" Chef Tray (~240g yield)',
                    'nutritional_highlights': 'Packed with glucosinolates, sulforaphane, Vitamin C, Vitamin B6, and potassium.',
                    'storage_instructions': 'Keep refrigerated at 2°C–4°C in original ventilated punnet. Rinse gently in ice water only if needed before service.',
                    'shelf_life_days': 10,
                    'is_featured': True,
                    'is_active': True,
                    'display_order': 2,
                },
                {
                    'name': 'Speckled Pea Tendrils',
                    'scientific_name': 'Pisum sativum',
                    'slug': 'speckled-pea-tendrils',
                    'category': category_map['shoots-tendrils'],
                    'tagline': 'Graceful curling tendrils and emerald leaves with the sweet taste of fresh spring garden peas.',
                    'description': (
                        'Harvested strictly at the tender top-node stage, our Speckled Pea Tendrils bring architectural height and sculptural '
                        'movement to any plate. Chefs prize their unmistakable sweet snow-pea aroma and crisp, juicy snap.'
                    ),
                    'primary_image': 'products/speckled-pea-tendrils.jpg',
                    'flavor_profile': 'Sweet Fresh Garden Pea, Lush Chlorophyll, Clean Crisp Finish',
                    'intensity_level': Microgreen.Intensity.MILD,
                    'texture_notes': 'Coiled springy tendrils with crisp, juicy stems and soft leaves',
                    'culinary_pairings': 'Pan-Seared Mahi-Mahi, Yasawa Lobster Risotto, Burrata & Tropical Citrus Salad, Lamb Rack',
                    'chef_serving_tip': 'Toss lightly in cold-pressed virgin coconut or olive oil with sea salt flakes to crown warm seafood.',
                    'availability_status': Microgreen.Availability.AVAILABLE,
                    'grow_cycle_days': 11,
                    'lead_time_notice': 'Daily morning harvest; high-volume standing resort allocations available.',
                    'price_punnet_fjd': 12.50,
                    'punnet_weight_grams': '50g Chef Clam-Shell Punnet',
                    'price_tray_fjd': 48.00,
                    'tray_size_label': 'Live 10x20" Chef Tray (~260g yield)',
                    'nutritional_highlights': 'High in plant protein, Vitamin A, Vitamin C, folate, and dietary fiber.',
                    'storage_instructions': 'Store at 2°C–4°C. Very resilient; stays crisp for over a week in cold storage.',
                    'shelf_life_days': 11,
                    'is_featured': True,
                    'is_active': True,
                    'display_order': 3,
                },
                {
                    'name': 'Black Oil Sunflower Shoots',
                    'scientific_name': 'Helianthus annuus',
                    'slug': 'black-oil-sunflower',
                    'category': category_map['shoots-tendrils'],
                    'tagline': 'Thick, jade-green succulent shoots with a rich, toasted sunflower-nut crunch.',
                    'description': (
                        'Our Black Oil Sunflower Shoots are carefully de-hulled by hand prior to harvest, yielding meaty, jade-green cotyledons '
                        'with a substantial crunch and savoury nutty sweetness. Ideal both as a structural garnish and as the base of a luxury micro-salad.'
                    ),
                    'primary_image': 'products/black-oil-sunflower.jpg',
                    'flavor_profile': 'Toasted Sunflower Seed, Savoury Nutty, Juicy Green Crunch',
                    'intensity_level': Microgreen.Intensity.BALANCED,
                    'texture_notes': 'Substantial, meaty cotyledons with crisp, hydrating stems',
                    'culinary_pairings': 'Chargrilled Eye Fillet, Roasted Pumpkin & Feta Tart, Reef Fish Ika Vakalolo, Micro-Green Caesar',
                    'chef_serving_tip': 'Sturdy enough to be dressed 10 minutes before service as a dedicated micro-salad component.',
                    'availability_status': Microgreen.Availability.AVAILABLE,
                    'grow_cycle_days': 10,
                    'lead_time_notice': 'Available daily in punnets or uncut live trays for resort kitchens.',
                    'price_punnet_fjd': 13.00,
                    'punnet_weight_grams': '60g Chef Clam-Shell Punnet',
                    'price_tray_fjd': 50.00,
                    'tray_size_label': 'Live 10x20" Chef Tray (~300g yield)',
                    'nutritional_highlights': 'Complete amino acid profile, Vitamin E, zinc, magnesium, iron, and healthy phytosterols.',
                    'storage_instructions': 'Store at 2°C–4°C in sealed clam-shell. Keep dry until plating.',
                    'shelf_life_days': 10,
                    'is_featured': False,
                    'is_active': True,
                    'display_order': 4,
                },
                {
                    'name': 'Fijian Citrus Micro Coriander',
                    'scientific_name': 'Coriandrum sativum',
                    'slug': 'fijian-citrus-coriander',
                    'category': category_map['aromatic-herbs'],
                    'tagline': 'Finely serrated lacy leaves bursting with 3x the essential citrus-coriander oil of mature cilantro.',
                    'description': (
                        'Slow-grown from split Leisure coriander seed, our Fijian Citrus Micro Coriander delivers an explosive aroma of crushed '
                        'coriander seed, kaffir lime zest, and fresh garden herb. A single pinch transforms coastal Fijian seafood and Pacific Rim curries.'
                    ),
                    'primary_image': 'products/fijian-citrus-coriander.jpg',
                    'flavor_profile': 'Bright Citrus Zest, Crushed Coriander Seed, Intense Herbal Finish',
                    'intensity_level': Microgreen.Intensity.BOLD,
                    'texture_notes': 'Delicate fern-like serrated true leaves with slender aromatic stems',
                    'culinary_pairings': 'Traditional Fijian Kokoda, Chili Mud Crab, Yellowfin Tuna Tataki, Lolo Coconut Broth',
                    'chef_serving_tip': 'Leave whole stems intact when plating to release citrus volatiles as the guest takes their first bite.',
                    'availability_status': Microgreen.Availability.GROW_TO_ORDER,
                    'grow_cycle_days': 16,
                    'lead_time_notice': 'Limited daily punnets; 14-day custom grow reservation recommended for standing resort orders.',
                    'price_punnet_fjd': 15.00,
                    'punnet_weight_grams': '35g Chef Clam-Shell Punnet',
                    'price_tray_fjd': 58.00,
                    'tray_size_label': 'Live 10x20" Chef Tray (~190g yield)',
                    'nutritional_highlights': 'Rich in linalool essential oils, Vitamin A, Vitamin K, lutein, and detoxifying phytonutrients.',
                    'storage_instructions': 'Store at 3°C–5°C. Ordering live uncut trays gives island kitchens up to 14 days of peak harvest.',
                    'shelf_life_days': 9,
                    'is_featured': True,
                    'is_active': True,
                    'display_order': 5,
                },
                {
                    'name': 'Wasabi Mustard Microgreens',
                    'scientific_name': 'Brassica juncea',
                    'slug': 'wasabi-mustard-greens',
                    'category': category_map['brassicas-spicy'],
                    'tagline': 'Ruffled lime-emerald leaves delivering an authentic sinus-clearing Japanese wasabi kick.',
                    'description': (
                        'Prized by sushi masters and modern Pacific Rim chefs, Wasabi Mustard Microgreens start with a sweet green crunch before '
                        'building into a clean, unmistakable horseradish-wasabi heat that vanishes cleanly without lingering bitterness.'
                    ),
                    'primary_image': 'products/wasabi-mustard-greens.jpg',
                    'flavor_profile': 'Authentic Wasabi Heat, Horseradish Zest, Sweet Brassica Finish',
                    'intensity_level': Microgreen.Intensity.SPICY,
                    'texture_notes': 'Frilly, ruffled bright green cotyledons with crisp stems',
                    'culinary_pairings': 'Sashimi & Nigiri Flights, Seared Wagyu Tataki, Oysters on the Half Shell, Smoked Marlin',
                    'chef_serving_tip': 'Use 3–4 micro-stems per piece of sashimi or oyster to replace grated paste with fresh botanical heat.',
                    'availability_status': Microgreen.Availability.LIMITED,
                    'grow_cycle_days': 9,
                    'lead_time_notice': 'Harvested Tuesday & Friday mornings; reserve 7 days ahead for guaranteed weekly allocation.',
                    'price_punnet_fjd': 14.00,
                    'punnet_weight_grams': '40g Chef Clam-Shell Punnet',
                    'price_tray_fjd': 52.00,
                    'tray_size_label': 'Live 10x20" Chef Tray (~210g yield)',
                    'nutritional_highlights': 'Extremely high in allyl isothiocyanate, Vitamin C, Vitamin K, and antioxidant glucosinolates.',
                    'storage_instructions': 'Keep sealed at 2°C–4°C; cold temperature locks in the volatile mustard oils.',
                    'shelf_life_days': 8,
                    'is_featured': False,
                    'is_active': True,
                    'display_order': 6,
                },
            ]

            for item in varieties_data:
                Microgreen.objects.create(**item)

            self.stdout.write(self.style.SUCCESS(f"Seeded {len(varieties_data)} flagship microgreen varieties."))
        else:
            self.stdout.write("Microgreen varieties already seeded.")

        if WholesaleInquiry.objects.count() == 0:
            WholesaleInquiry.objects.create(
                chef_name="Chef Epeli Nailatikau",
                role_title="Executive Chef",
                establishment_name="Vomo Island Resort Fiji",
                email="executivechef@vomofiji.example.com",
                phone_whatsapp="+679 992 4810",
                region=WholesaleInquiry.Region.MAMANUCA_YASAWA,
                inquiry_type=WholesaleInquiry.InquiryType.STANDING_ORDER,
                selected_varieties_summary="• Red Garnet Amaranth (6x 35g Punnets)\n• Fijian Citrus Micro Coriander (4x Live Trays)\n• Wasabi Mustard Microgreens (4x 40g Punnets)",
                estimated_weekly_volume="18 punnets + 4 live trays weekly via Port Denarau transfer",
                preferred_delivery_days="Tuesday & Friday 7:30 AM Port Denarau Marina",
                culinary_notes="Looking for consistent year-round live trays for our beachfront degustation menu.",
                status=WholesaleInquiry.Status.ACTIVE_PARTNER,
            )
            WholesaleInquiry.objects.create(
                chef_name="Chef Elena Rostova",
                role_title="Head Yacht Chef",
                establishment_name="M/Y Southern Cross (Port Denarau Marina)",
                email="galley@mysoutherncross.example.com",
                phone_whatsapp="+679 778 1920",
                region=WholesaleInquiry.Region.MARINA_YACHT,
                inquiry_type=WholesaleInquiry.InquiryType.SAMPLE_BOX,
                selected_varieties_summary="• Speckled Pea Tendrils\n• Rambo Purple Radish\n• Red Garnet Amaranth",
                estimated_weekly_volume="12 punnets + 2 live trays for 10-day Lau Group charter",
                preferred_delivery_days="Thursday morning before 8:00 AM dockside",
                culinary_notes="Requesting a tasting box tomorrow morning prior to owner provisioning.",
                status=WholesaleInquiry.Status.NEW,
            )
            self.stdout.write(self.style.SUCCESS("Seeded sample Chef Wholesale Inquiries."))
