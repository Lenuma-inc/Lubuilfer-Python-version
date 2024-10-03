from django.contrib import admin
from .models import Package, Build

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'user', 'created_at')
    search_fields = ('name', 'version', 'user__username')
    list_filter = ('created_at',)

@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('id', 'package', 'status', 'created_at')
    search_fields = ('package__name', 'status')
    list_filter = ('status', 'created_at')
