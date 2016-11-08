from django.contrib import admin
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.helpers import generate_key


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'modified')

    fieldsets = (
        ('Required Information', {'fields': ('name',)}),
        ('Additional Information', {'fields': ('key_message',)}),
    )
    readonly_fields = ('key_message',)

    search_fields = ('id', 'name',)

    def has_delete_permission(self, request, obj=None):
        return False

    def key_message(self, obj):
        if obj.key:
            return obj.key

        return "The API Key will be generated once you click save."

    def save_model(self, request, obj, form, change):
        if not obj.key:
            obj.key = generate_key()

        obj.save()

admin.site.register(APIKey, ApiKeyAdmin)
