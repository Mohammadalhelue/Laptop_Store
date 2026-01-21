from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from store import views
from store.views import RegisterView, LoginView, LogoutView, CartAPIView, CartAddUpdateAPIView, OrderCreateAPIView


# Same router customization here, since these routes are actually used at /api/
class BrowsableSafeRouter(DefaultRouter):
    def get_routes(self, viewset):
        routes = super().get_routes(viewset)
        for r in routes:
            if getattr(r, 'detail', False) and isinstance(r.mapping, dict):
                if any(k in r.mapping for k in ('put', 'patch', 'delete')):
                    r.mapping.setdefault('post', 'method_override')
        return routes


router = BrowsableSafeRouter(trailing_slash='/?')
router.register(r"accessories", views.AccessoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT (optional; kept)
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # DRF router
    path('', include(router.urls)),
    path('recommendations/', views.RecommendationsView.as_view(), name='recommendations'),
    # Auth endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Cart Management
    path('cart/', CartAPIView.as_view(), name='cart-detail'),
    # Example: POST /cart/add/1/ with body {"quantity": 2, "override": false}
    path('cart/add/<int:accessory_id>/', CartAddUpdateAPIView.as_view(), name='cart-add'),

    # Order System
    path('orders/create/', OrderCreateAPIView.as_view(), name='order-create'),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
