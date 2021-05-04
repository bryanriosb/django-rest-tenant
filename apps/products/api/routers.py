from rest_framework import routers
from .views.product_view import ProductViewSet
from .views.general_view import ProductCategoryViewSet, MeasureUnitViewSet, IndicatorViewSet

router = routers.DefaultRouter()
router.register(r'categories', ProductCategoryViewSet, basename='categories')
router.register(r'measure_units', MeasureUnitViewSet, basename='measure_units')
router.register(r'off_indicators', IndicatorViewSet, basename='off_indicators')
router.register(r'all_methods', ProductViewSet, basename='all_actions')
urlpatterns = router.urls
