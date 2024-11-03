from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SupplierViewSet, ProductViewSet, OrderViewSet, PaymentViewSet, InventoryViewSet, InventoryTransactionViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'inventories', InventoryViewSet)
router.register(r'inventory-transactions', InventoryTransactionViewSet)

urlpatterns = router.urls
