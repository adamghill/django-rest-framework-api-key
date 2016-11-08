from rest_framework import permissions
from rest_framework_api_key.models import APIKey


class HasAPIAccess(permissions.BasePermission):
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')

        if not api_key:
            api_key = request.GET.get('apikey', '')

        return APIKey.objects.filter(key=api_key).exists()
