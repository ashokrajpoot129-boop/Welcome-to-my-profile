from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'mobile_number', 'created_at')
	search_fields = ('name', 'email', 'mobile_number', 'message')
