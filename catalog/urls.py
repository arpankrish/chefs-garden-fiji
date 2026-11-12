from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('variety/<slug:slug>/', views.variety_detail_view, name='variety_detail'),
    path('manage/', views.studio_dashboard_view, name='studio_dashboard'),
    path('manage/new/', views.studio_create_view, name='studio_create'),
    path('manage/edit/<slug:slug>/', views.studio_edit_view, name='studio_edit'),
    path('manage/delete/<slug:slug>/', views.studio_delete_view, name='studio_delete'),
    path('manage/inquiry/<int:pk>/status/', views.studio_inquiry_status_view, name='studio_inquiry_status'),
]
