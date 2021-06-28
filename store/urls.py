from rest_framework import routers

from store import views

router = routers.DefaultRouter()
router.register('product', views.ProductViewSet, basename='product')

urlpatterns = []
urlpatterns += router.urls
