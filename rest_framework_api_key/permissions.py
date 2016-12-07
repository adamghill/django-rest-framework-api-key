from django.core.cache import cache

from rest_framework import permissions
from rest_framework_api_key.models import APIKey


class HasAPIAccess(permissions.BasePermission):
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')

        if not api_key:
            api_key = request.GET.get('apikey', '')

        if api_key:
            cache_key = 'rest_framework_api_key:{}'.format(api_key)
            api_key_does_exist = cache.get(cache_key, None)

            if api_key_does_exist is None:
                api_key_does_exist = APIKey.objects.filter(key=api_key).exists()

                cache_timeout = 60 * 10
                cache.set(cache_key, api_key_does_exist, cache_timeout)

            return api_key_does_exist

        return False
