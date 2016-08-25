from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token


from products.views import ProductCategoryViewSet, ProductTypeViewSet, ProductViewSet
from services.views import ServiceCategoryViewSet, ServiceTypeViewSet, ServiceViewSet
from sales.views import SaleViewSet
from purchases.views import PurchaseViewSet
from contact.views import ContactViewSet
from business.views import DataViewSet, InformationViewSet, KnowledgeViewSet

router = routers.DefaultRouter()
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'product-types', ProductTypeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'service-categories', ServiceCategoryViewSet)
router.register(r'service-types', ServiceTypeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'datas', DataViewSet)
router.register(r'informations', InformationViewSet)
router.register(r'knowledges', KnowledgeViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^_ah/', include('djangae.urls')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
url(r'^api-token-auth/', obtain_jwt_token),
# url(r'^api-token-refresh/', refresh_jwt_token),
url(r'^api-token-verify/', verify_jwt_token),
    url(r'api/', include(router.urls)),
]
