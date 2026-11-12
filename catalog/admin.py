from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Microgreen, ProductGalleryImage, WholesaleInquiry


class ProductGalleryImageInline(admin.TabularInline):
    model = ProductGalleryImage
    extra = 1
    readonly_fields = ('gallery_preview',)
    fields = ('image', 'gallery_preview', 'caption', 'display_order')

    def gallery_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 64px; width: 64px; object-fit: cover; border-radius: 8px; border: 1px solid #d4a359;" />',
                obj.image.url
            )
        return "No photo uploaded"
    gallery_preview.short_description = "Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'badge_color', 'display_order', 'variety_count')
    list_editable = ('badge_color', 'display_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def variety_count(self, obj):
        return obj.microgreens.count()
    variety_count.short_description = "Varieties"


@admin.register(Microgreen)
class MicrogreenAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail_preview',
        'name',
        'category',
        'availability_status',
        'grow_cycle_days',
        'price_punnet_fjd',
        'price_tray_fjd',
        'is_featured',
        'is_active',
    )
    list_display_links = ('thumbnail_preview', 'name')
    list_editable = (
        'availability_status',
        'price_punnet_fjd',
        'price_tray_fjd',
        'is_featured',
        'is_active',
    )
    list_filter = ('category', 'availability_status', 'intensity_level', 'is_featured', 'is_active')
    search_fields = ('name', 'scientific_name', 'tagline', 'description', 'flavor_profile', 'culinary_pairings')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('large_image_preview', 'created_at', 'updated_at')
    inlines = [ProductGalleryImageInline]

    fieldsets = (
        ('1. Variety Identity, Photo Upload & Description', {
            'description': 'Upload your microgreen photo and write the description chefs will read in the catalog.',
            'fields': (
                ('name', 'scientific_name'),
                ('slug', 'category'),
                ('primary_image', 'large_image_preview'),
                'tagline',
                'description',
            )
        }),
        ('2. Flavor Profile & Culinary Pairing Notes', {
            'description': 'Specify tasting notes, heat/intensity level, and recommended dish pairings for chefs.',
            'fields': (
                ('flavor_profile', 'intensity_level'),
                'texture_notes',
                'culinary_pairings',
                'chef_serving_tip',
            )
        }),
        ('3. Harvest-to-Order, Grow Cycle & Availability', {
            'description': 'Manage current stock status, grow time in days, and harvest delivery notice.',
            'fields': (
                ('availability_status', 'grow_cycle_days'),
                'lead_time_notice',
            )
        }),
        ('4. Packaging Formats & Wholesale Pricing (FJD $)', {
            'description': 'Set Fijian Dollar (FJD) pricing for chef clam-shell punnets and live 10x20" trays.',
            'fields': (
                ('price_punnet_fjd', 'punnet_weight_grams'),
                ('price_tray_fjd', 'tray_size_label'),
            )
        }),
        ('5. Nutritional Benefits & Kitchen Storage', {
            'description': 'Provide cold-chain care instructions, shelf life, and nutritional highlights.',
            'fields': (
                'shelf_life_days',
                'storage_instructions',
                'nutritional_highlights',
            )
        }),
        ('6. Catalog Visibility & Display Order', {
            'fields': (
                ('is_featured', 'is_active', 'display_order'),
                ('created_at', 'updated_at'),
            )
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.primary_image:
            return format_html(
                '<img src="{}" style="width: 56px; height: 56px; object-fit: cover; border-radius: 10px; border: 2px solid #2e6f40; box-shadow: 0 2px 6px rgba(0,0,0,0.2);" />',
                obj.primary_image.url
            )
        return format_html(
            '<div style="width:56px;height:56px;border-radius:10px;background:#132a1f;color:#d4a359;display:flex;align-items:center;justify-content:center;font-size:11px;text-align:center;">No Photo</div>'
        )
    thumbnail_preview.short_description = "Photo"

    def large_image_preview(self, obj):
        if obj.primary_image:
            return format_html(
                '<img src="{}" style="max-height: 220px; border-radius: 12px; border: 2px solid #d4a359; box-shadow: 0 6px 18px rgba(0,0,0,0.25);" />',
                obj.primary_image.url
            )
        return "Upload an image and click Save to preview."
    large_image_preview.short_description = "Current Uploaded Photo"


@admin.register(WholesaleInquiry)
class WholesaleInquiryAdmin(admin.ModelAdmin):
    list_display = (
        'establishment_name',
        'chef_name',
        'role_title',
        'inquiry_type',
        'region',
        'phone_whatsapp',
        'status',
        'created_at',
    )
    list_editable = ('status',)
    list_filter = ('status', 'inquiry_type', 'region', 'created_at')
    search_fields = ('establishment_name', 'chef_name', 'email', 'phone_whatsapp', 'selected_varieties_summary', 'culinary_notes')
    readonly_fields = ('created_at',)
