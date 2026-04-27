from rest_framework.routers import DefaultRouter

from catalog.views import CategoryViewSet, ProductViewSet

app_name = "catalog"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"products", ProductViewSet, basename="products")

urlpatterns = router.urls
