from django.urls import path
from django.apps import apps
import importlib

def get_websocket_urlpatterns(prefix="ws"):
    """Dynamically aggregate websocket_urlpatterns from all apps."""
    patterns = []
    for app_config in apps.get_app_configs():
        try:
            routing = importlib.import_module(f"{app_config.name}.routing")
            app_patterns = getattr(routing, 'websocket_urlpatterns', [])

            for pattern in app_patterns:
                patterns.append(path(prefix + pattern.pattern._route, pattern.callback))
        except (ModuleNotFoundError, AttributeError):
            # Skip apps without a routing module or websocket_urlpatterns
            continue
    return patterns

websocket_urlpatterns = get_websocket_urlpatterns()