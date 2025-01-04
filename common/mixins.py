import hashlib
import json
import logging
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class DynamicCacheMixin:
    """
    A mixin for caching responses in a ModelViewSet with dynamic cache control.
    """

    def get_cache_timeout(self, request):
        """
        Return the timeout (in seconds) for the cache. This can vary based on the request,
        e.g., different timeouts for authenticated users vs non-authenticated users.
        Reads the timeout from the settings.
        """
        timeout = settings.CACHE_TIMEOUT_DEFAULT

        # Check if user is authenticated and change timeout accordingly
        if request.user.is_authenticated:
            timeout = settings.CACHE_TIMEOUT_AUTHENTICATED

        # Allow query parameter-based adjustments (e.g., ?cache_timeout=120)
        timeout_from_request = request.GET.get('cache_timeout')
        if timeout_from_request:
            timeout = int(timeout_from_request)

        return timeout

    def get_cache_key(self, request, is_list=False):
        """
        Generate a unique cache key based on the request.
        This method can be further customized to make cache keys more dynamic.
        Reads the base URL path from the request and appends user-specific info.
        """
        base_key = f"{request.path}?{request.GET.urlencode()}"

        # Add user ID for authenticated users, ensuring different users get different cache
        if request.user.is_authenticated:
            base_key += f"&user_id={request.user.id}"

        base_key += '&is_list' if is_list else '&is_retrieve'

        return hashlib.md5(base_key.encode('utf-8')).hexdigest()

    def cache_response(self, response, cache_key, timeout):
        """
        Cache the response. This checks the cache backend in settings and caches data
        accordingly.
        """
        # Serialize response data to JSON to store in Redis
        serialized_data = json.dumps(response.data)

        # Cache based on selected backend
        cache_backend = settings.CACHE_BACKEND
        if cache_backend == 'redis':
            from django_redis import get_redis_connection
            redis_conn = get_redis_connection("default")
            redis_conn.setex(cache_key, timeout, serialized_data)
        elif cache_backend == 'memcached':
            from django.core.cache.backends.memcached import MemcachedCache
            cache_instance = MemcachedCache(settings.CACHES['memcached'])
            cache_instance.set(cache_key, serialized_data, timeout)
        else:
            cache.set(cache_key, serialized_data, timeout)

    def get_cached_response(self, cache_key):
        """
        Retrieve the cached response.
        """
        # Fetch from cache based on the backend
        cache_backend = settings.CACHE_BACKEND
        if cache_backend == 'redis':
            from django_redis import get_redis_connection
            redis_conn = get_redis_connection("default")
            cached_data = redis_conn.get(cache_key)
        elif cache_backend == 'memcached':
            from django.core.cache.backends.memcached import MemcachedCache
            cache_instance = MemcachedCache(settings.CACHES['memcached'])
            cached_data = cache_instance.get(cache_key)
        else:
            cached_data = cache.get(cache_key)

        # Deserialize the cached data if it exists
        if cached_data:
            return json.loads(cached_data)  # Deserialize the JSON data

        return None

    def check_cache(self, request, is_list=False):
        """
        Check if the response is cached, and return it if available.
        """
        cache_key = self.get_cache_key(request, is_list)
        cached_response = self.get_cached_response(cache_key)

        if cached_response:
            logger.info(f"Cache hit: {cache_key}")
            return Response(cached_response)

        logger.info(f"Cache miss: {cache_key}")
        return None

    def set_cache(self, request, response, is_list=False):
        """
        Cache the response after view processing.
        """
        cache_key = self.get_cache_key(request, is_list)
        timeout = self.get_cache_timeout(request)
        self.cache_response(response, cache_key, timeout)

    def retrieve(self, request, *args, **kwargs):
        """
        Handle GET requests for individual objects and cache the response.
        """
        cached_response = self.check_cache(request)
        if cached_response:
            return cached_response

        response = super().retrieve(request, *args, **kwargs)
        self.set_cache(request, response)
        return response

    def list(self, request, *args, **kwargs):
        """
        Handle GET requests for a list of objects and cache the response.
        """
        cached_response = self.check_cache(request, is_list=True)
        if cached_response:
            return cached_response

        response = super().list(request, *args, **kwargs)
        self.set_cache(request, response, is_list=True)
        return response

    def create(self, request, *args, **kwargs):
        """
        Handle POST requests, invalidate cache when necessary, and optionally cache the response.
        """
        response = super().create(request, *args, **kwargs)
        self.invalidate_related_caches(request)
        return response

    def update(self, request, *args, **kwargs):
        """
        Handle PUT requests, invalidate cache when necessary.
        """
        response = super().update(request, *args, **kwargs)
        self.invalidate_related_caches(request)
        return response

    def destroy(self, request, *args, **kwargs):
        """
        Handle DELETE requests, invalidate cache when necessary.
        """
        response = super().destroy(request, *args, **kwargs)
        self.invalidate_related_caches(request)
        return response

    def invalidate_related_caches(self, request):
        """
        Invalidate cache for related resources when a model is created, updated, or deleted.
        This includes invalidating caches for dependent or related views.
        """
        related_cache_keys = self.get_related_cache_keys(request)
        for key in related_cache_keys:
            logger.info(f"Invalidating cache for key: {key}")
            cache.delete(key)

    def get_related_cache_keys(self, request):
        """
        Generate cache keys for related views that need to be invalidated when a model changes.
        For example, list views or other related models.
        """
        return [
            self.get_cache_key(request),
            f"{self.get_cache_key(request, is_list=True)}"
        ]