"""asset_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('show/', views.IndexView.as_view(),name='index'),
    path('', views.dashboard_view, name='index'),
    path('all_category/', views.all_assettype_view, name='all_category'),
    path('add_category/', views.add_assettype_view, name='add_category'),
    path('edit_category/<int:id>/', views.update_assettype_view, name='update_category'),
    path('remove_category/<int:id>/', views.remove_assettype_view, name='remove_category'),
    path('all_items/', views.all_items_view, name='all_items'),
    path('add_item/', views.add_item_view, name='add_item'),
    path('update_item/<id>/', views.update_item_view, name='update_item'),
    path('remove_item/<id>/', views.remove_item_view, name='remove_item'),
    path('item_images/<id>/', views.show_images, name='item_images'),
    path('pie_data/', views.pie_chart_view, name='pie_data'),
    path('bar_data/', views.bar_chart_view, name='bar_data'),
    path('export_items_csv/', views.export_items_csv, name='export-csv'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
