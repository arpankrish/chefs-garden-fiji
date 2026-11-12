from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.TextField(
        blank=True,
        help_text="Brief culinary description of this microgreen category."
    )
    badge_color = models.CharField(
        max_length=30,
        default="emerald",
        help_text="Accent style (emerald, crimson, gold, violet, citrus)"
    )
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Botanical Category"
        verbose_name_plural = "Botanical Categories"
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Microgreen(models.Model):
    class Availability(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Ready for Daily Harvest'
        GROW_TO_ORDER = 'GROW_TO_ORDER', 'Grow-to-Order (Custom Harvest)'
        LIMITED = 'LIMITED', 'Limited Weekly Batch'
        SEASONAL = 'SEASONAL', 'Seasonal / Chef Inquiry Only'

    class Intensity(models.IntegerChoices):
        DELICATE = 1, '1 — Delicate & Subtle'
        MILD = 2, '2 — Mild & Fresh'
        BALANCED = 3, '3 — Balanced & Aromatic'
        BOLD = 4, '4 — Bold & Earthy'
        SPICY = 5, '5 — Spicy & Pungent'

    # Core Identification & Imagery
    name = models.CharField(
        max_length=140,
        help_text="Commercial culinary name (e.g., Red Garnet Amaranth)"
    )
    scientific_name = models.CharField(
        max_length=140,
        blank=True,
        help_text="Botanical Latin name (e.g., Amaranthus tricolor)"
    )
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='microgreens'
    )
    tagline = models.CharField(
        max_length=220,
        help_text="One-line visual & flavor hook shown on catalog cards."
    )
    description = models.TextField(
        help_text="Detailed culinary description, visual appeal on the plate, and origin story."
    )
    primary_image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        help_text="Upload high-resolution macro product photo."
    )

    # 1. Flavor Profile & Culinary Pairing Notes
    flavor_profile = models.CharField(
        max_length=200,
        help_text="Key tasting notes separated by commas (e.g., Peppy Mustard, Horseradish Heat, Clean Crisp Finish)"
    )
    intensity_level = models.IntegerField(
        choices=Intensity.choices,
        default=Intensity.BALANCED,
        help_text="Flavor intensity from 1 (Delicate) to 5 (Spicy/Pungent)"
    )
    texture_notes = models.CharField(
        max_length=180,
        default="Crisp succulent stems with tender cotyledons",
        help_text="Mouthfeel and structural texture on the plate."
    )
    culinary_pairings = models.TextField(
        help_text="Recommended dishes & ingredients (comma-separated or prose, e.g., Fijian Kokoda, Seared Yellowfin Tuna, Duck Breast)"
    )
    chef_serving_tip = models.CharField(
        max_length=255,
        blank=True,
        help_text="Pro plating advice for executive chefs."
    )

    # 2. Harvest-to-Order / Grow Time & Availability Status
    availability_status = models.CharField(
        max_length=25,
        choices=Availability.choices,
        default=Availability.AVAILABLE
    )
    grow_cycle_days = models.PositiveIntegerField(
        default=10,
        help_text="Number of days from seeding to peak harvest."
    )
    lead_time_notice = models.CharField(
        max_length=200,
        default="Harvested at dawn; same-day chilled delivery for Nadi, Denarau & Coral Coast.",
        help_text="Delivery or custom grow lead time details."
    )

    # 3. Packaging Sizes & Pricing (in FJD)
    price_punnet_fjd = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=12.50,
        verbose_name="Punnet Price (FJD $)",
        help_text="Wholesale price per chef punnet in Fijian Dollars (FJD)."
    )
    punnet_weight_grams = models.CharField(
        max_length=80,
        default="40g Chef Clam-Shell Punnet",
        help_text="Standard punnet size/weight specification."
    )
    price_tray_fjd = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=48.00,
        blank=True,
        null=True,
        verbose_name="Live Chef Tray Price (FJD $)",
        help_text="Wholesale price for a full live 10x20\" tray in FJD."
    )
    tray_size_label = models.CharField(
        max_length=100,
        default="Live 10x20\" Shallow Chef Tray (~220g yield)",
        blank=True,
        help_text="Live tray specification."
    )

    # 4. Nutritional Benefits & Storage Instructions
    nutritional_highlights = models.TextField(
        default="High concentration of Vitamins C, E, K, beta-carotene, and polyphenols (up to 40x mature greens).",
        help_text="Key vitamins, antioxidants, and nutritional benefits."
    )
    storage_instructions = models.TextField(
        default="Keep unwashed in sealed chef punnet at 2°C–4°C with bottom moisture pad. Rinse gently only immediately prior to service.",
        help_text="Best cold-chain storage instructions for commercial kitchens."
    )
    shelf_life_days = models.PositiveIntegerField(
        default=8,
        help_text="Expected refrigerated shelf life in days after harvest."
    )

    # Display Flags
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this microgreen in the Chef's Spotlight section."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Show this variety on the public website catalog."
    )
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Microgreen Variety"
        verbose_name_plural = "Microgreen Varieties"
        ordering = ['display_order', '-is_featured', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Microgreen.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def flavor_tags(self):
        return [tag.strip() for tag in self.flavor_profile.split(',') if tag.strip()]

    @property
    def pairing_tags(self):
        return [tag.strip() for tag in self.culinary_pairings.split(',') if tag.strip()]

    @property
    def intensity_range(self):
        return range(1, 6)

    def __str__(self):
        return f"{self.name} (${self.price_punnet_fjd} FJD)"


class ProductGalleryImage(models.Model):
    microgreen = models.ForeignKey(
        Microgreen,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(upload_to='products/gallery/')
    caption = models.CharField(
        max_length=160,
        blank=True,
        help_text="Optional caption (e.g., Plated on Kokoda ceviche, Live tray view)"
    )
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Additional Gallery Photos"
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.microgreen.name} - Photo #{self.id}"


class WholesaleInquiry(models.Model):
    class InquiryType(models.TextChoices):
        SAMPLE_BOX = 'SAMPLE_BOX', "Complimentary Chef's Tasting Box"
        STANDING_ORDER = 'STANDING_ORDER', 'Weekly Standing Resort / Restaurant Supply'
        CUSTOM_GROW = 'CUSTOM_GROW', 'Custom Grow-to-Order Crop Program'
        EVENT_CHARTER = 'EVENT_CHARTER', 'One-Off Event / Superyacht Charter Order'

    class Region(models.TextChoices):
        DENARAU_NADI = 'DENARAU_NADI', 'Denarau Island, Nadi & Martintar'
        MAMANUCA_YASAWA = 'MAMANUCA_YASAWA', 'Mamanuca & Yasawa Island Resorts'
        CORAL_COAST = 'CORAL_COAST', 'Coral Coast & Natadola'
        SUVA_PACIFIC = 'SUVA_PACIFIC', 'Suva, Pacific Harbour & Beqa'
        NORTH_OUTER = 'NORTH_OUTER', 'Savusavu, Taveuni & Outer Islands (Air Freight)'
        MARINA_YACHT = 'MARINA_YACHT', 'Port Denarau / Vuda Superyacht Provisioning'

    class Status(models.TextChoices):
        NEW = 'NEW', 'New Inquiry'
        CONTACTED = 'CONTACTED', 'Chef Contacted'
        SAMPLE_SENT = 'SAMPLE_SENT', 'Tasting Box Dispatched'
        ACTIVE_PARTNER = 'ACTIVE_PARTNER', 'Active Standing Account'
        ARCHIVED = 'ARCHIVED', 'Archived'

    chef_name = models.CharField(max_length=120, verbose_name="Chef / Contact Name")
    role_title = models.CharField(
        max_length=100,
        default="Executive Chef",
        verbose_name="Culinary Role / Title"
    )
    establishment_name = models.CharField(
        max_length=160,
        verbose_name="Resort, Restaurant, or Yacht Name"
    )
    email = models.EmailField(verbose_name="Email Address")
    phone_whatsapp = models.CharField(
        max_length=60,
        verbose_name="Phone / WhatsApp (+679)"
    )
    region = models.CharField(
        max_length=30,
        choices=Region.choices,
        default=Region.DENARAU_NADI,
        verbose_name="Fiji Delivery Region"
    )
    inquiry_type = models.CharField(
        max_length=30,
        choices=InquiryType.choices,
        default=InquiryType.SAMPLE_BOX,
        verbose_name="Program Interest"
    )
    selected_varieties_summary = models.TextField(
        blank=True,
        verbose_name="Requested Microgreen Varieties & Formats",
        help_text="Varieties added by the chef from the interactive catalog."
    )
    estimated_weekly_volume = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Estimated Weekly Volume (Punnets / Live Trays)"
    )
    preferred_delivery_days = models.CharField(
        max_length=120,
        blank=True,
        default="Tuesday & Friday Morning Harvest",
        verbose_name="Preferred Harvest / Delivery Days"
    )
    culinary_notes = models.TextField(
        blank=True,
        verbose_name="Menu Notes / Special Requests"
    )
    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chef Wholesale Inquiry"
        verbose_name_plural = "Chef Wholesale Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.establishment_name} ({self.chef_name}) — {self.get_inquiry_type_display()}"
