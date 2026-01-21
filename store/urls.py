from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AccessoryViewSet,
    RegisterView,
    RecommendationsView,
    LoginView,
    LogoutView,
)


class BrowsableSafeRouter(DefaultRouter):
    def get_routes(self, viewset):
        routes = super().get_routes(viewset)
        for r in routes:
            if getattr(r, 'detail', False) and isinstance(r.mapping, dict):
                if any(k in r.mapping for k in ('put', 'patch', 'delete')):
                    r.mapping.setdefault('post', 'method_override')
        return routes


router = BrowsableSafeRouter(trailing_slash='/?')
router.register(r'accessories', AccessoryViewSet, basename='accessory')

auth_urls = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include((auth_urls, 'auth'))),
]
