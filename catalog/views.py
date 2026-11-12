from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import MicrogreenStudioForm, WholesaleInquiryForm
from .models import Category, Microgreen, WholesaleInquiry


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


def home_view(request):
    categories = Category.objects.all()
    varieties = Microgreen.objects.filter(is_active=True).select_related('category').prefetch_related('gallery_images')

    # Optional server-side filtering if query params are passed
    selected_category = request.GET.get('category', '').strip()
    selected_availability = request.GET.get('availability', '').strip()
    search_query = request.GET.get('q', '').strip()

    if selected_category:
        varieties = varieties.filter(category__slug=selected_category)
    if selected_availability:
        varieties = varieties.filter(availability_status=selected_availability)
    if search_query:
        varieties = varieties.filter(
            Q(name__icontains=search_query) |
            Q(scientific_name__icontains=search_query) |
            Q(tagline__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(flavor_profile__icontains=search_query) |
            Q(culinary_pairings__icontains=search_query)
        )

    featured_varieties = Microgreen.objects.filter(is_active=True, is_featured=True).select_related('category')[:4]

    if request.method == 'POST':
        inquiry_form = WholesaleInquiryForm(request.POST)
        if inquiry_form.is_valid():
            inquiry = inquiry_form.save()
            messages.success(
                request,
                f"Vinaka vakalevu, {inquiry.chef_name}! Your wholesale inquiry for {inquiry.establishment_name} has been received. Our Head Grower will contact you on WhatsApp/Email within 4 hours."
            )
            return redirect('/#wholesale-inquiry')
        else:
            messages.error(
                request,
                "Please check the highlighted fields in your wholesale inquiry form below."
            )
    else:
        initial_variety = request.GET.get('variety', '')
        initial_data = {}
        if initial_variety:
            initial_data['selected_varieties_summary'] = f"• {initial_variety} (40g Punnet / Live Tray)"
        inquiry_form = WholesaleInquiryForm(initial=initial_data)

    context = {
        'categories': categories,
        'varieties': varieties,
        'featured_varieties': featured_varieties,
        'total_varieties_count': Microgreen.objects.filter(is_active=True).count(),
        'selected_category': selected_category,
        'selected_availability': selected_availability,
        'search_query': search_query,
        'inquiry_form': inquiry_form,
        'availability_choices': Microgreen.Availability.choices,
    }
    return render(request, 'catalog/home.html', context)


def variety_detail_view(request, slug):
    variety = get_object_or_404(
        Microgreen.objects.select_related('category').prefetch_related('gallery_images'),
        slug=slug
    )
    related_varieties = Microgreen.objects.filter(
        is_active=True
    ).exclude(pk=variety.pk).select_related('category')[:3]

    context = {
        'variety': variety,
        'related_varieties': related_varieties,
    }
    return render(request, 'catalog/variety_detail.html', context)


@user_passes_test(is_staff_user, login_url='/admin/login/')
def studio_dashboard_view(request):
    varieties = Microgreen.objects.select_related('category').all()
    categories = Category.objects.all()
    inquiries = WholesaleInquiry.objects.all()[:25]
    form = MicrogreenStudioForm()

    context = {
        'varieties': varieties,
        'categories': categories,
        'inquiries': inquiries,
        'form': form,
        'active_count': varieties.filter(is_active=True).count(),
        'featured_count': varieties.filter(is_featured=True).count(),
        'new_inquiries_count': WholesaleInquiry.objects.filter(status=WholesaleInquiry.Status.NEW).count(),
    }
    return render(request, 'catalog/studio_dashboard.html', context)


@user_passes_test(is_staff_user, login_url='/admin/login/')
def studio_create_view(request):
    if request.method == 'POST':
        form = MicrogreenStudioForm(request.POST, request.FILES)
        if form.is_valid():
            variety = form.save()
            messages.success(
                request,
                f"Added '{variety.name}' to the Chefs Garden Fiji catalog!"
            )
            return redirect('catalog:studio_dashboard')
    else:
        form = MicrogreenStudioForm()

    return render(request, 'catalog/studio_form.html', {
        'form': form,
        'is_edit': False,
    })


@user_passes_test(is_staff_user, login_url='/admin/login/')
def studio_edit_view(request, slug):
    variety = get_object_or_404(Microgreen, slug=slug)
    if request.method == 'POST':
        form = MicrogreenStudioForm(request.POST, request.FILES, instance=variety)
        if form.is_valid():
            variety = form.save()
            messages.success(
                request,
                f"Updated '{variety.name}' successfully!"
            )
            return redirect('catalog:studio_dashboard')
    else:
        form = MicrogreenStudioForm(instance=variety)

    return render(request, 'catalog/studio_form.html', {
        'form': form,
        'variety': variety,
        'is_edit': True,
    })


@user_passes_test(is_staff_user, login_url='/admin/login/')
def studio_delete_view(request, slug):
    variety = get_object_or_404(Microgreen, slug=slug)
    if request.method == 'POST':
        name = variety.name
        variety.delete()
        messages.success(request, f"Removed '{name}' from the catalog.")
    return redirect('catalog:studio_dashboard')


@user_passes_test(is_staff_user, login_url='/admin/login/')
def studio_inquiry_status_view(request, pk):
    inquiry = get_object_or_404(WholesaleInquiry, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(WholesaleInquiry.Status.choices):
            inquiry.status = new_status
            inquiry.save(update_fields=['status'])
            messages.success(
                request,
                f"Updated status for {inquiry.establishment_name} to '{inquiry.get_status_display()}'."
            )
    return redirect('catalog:studio_dashboard')
