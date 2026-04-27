from rest_framework.routers import DefaultRouter

from cart.views import CartViewSet

app_name = "catalog"

router = DefaultRouter()
router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = router.urls
