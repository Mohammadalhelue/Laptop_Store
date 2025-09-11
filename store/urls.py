from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AccessoryViewSet,
    RegisterView,
    MeView,
    SearchHistoryView,
    RecommendationsView,
    LoginView,
    LogoutView,
)

# Router that allows POST on the detail URL and maps it to viewset.method_override
class BrowsableSafeRouter(DefaultRouter):
    def get_routes(self, viewset):
        routes = super().get_routes(viewset)
        for r in routes:
            # Detail route has mapping for put/patch/delete; add post→method_override
            if getattr(r, 'detail', False) and isinstance(r.mapping, dict):
                if any(k in r.mapping for k in ('put', 'patch', 'delete')):
                    r.mapping.setdefault('post', 'method_override')
        return routes

# Allow both with/without trailing slash to avoid 301s
router = BrowsableSafeRouter(trailing_slash='/?')
router.register(r'accessories', AccessoryViewSet, basename='accessory')

auth_urls = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include((auth_urls, 'auth'))),
    path('search-history/', SearchHistoryView.as_view(), name='search-history'),
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),
]
