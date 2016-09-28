from django.conf.urls import url, include
from django.contrib import admin
from views import IndexView

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from products.views import ProductCategoryViewSet, ProductTypeViewSet, ProductViewSet, LocationViewSet, SectionViewSet
from services.views import ServiceCategoryViewSet, ServiceTypeViewSet, ServiceViewSet
from sales.views import  SaleViewSet
from customers.views import PointViewSet
from purchases.views import PurchaseViewSet
from contacts.views import ContactViewSet
from business.views import BusinessViewSet, TaxViewSet, DataViewSet, InformationViewSet, KnowledgeViewSet
from users.views import UserViewSet, GroupViewSet
from accounts.views import OwnerViewSet, EmployeeViewSet, CustomerViewSet, SupplierViewSet
from parametrization.views import ParametrizationViewSet

router = routers.DefaultRouter()
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'product-types', ProductTypeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'service-categories', ServiceCategoryViewSet)
router.register(r'service-types', ServiceTypeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'business', BusinessViewSet)
router.register(r'taxes', TaxViewSet)
router.register(r'datas', DataViewSet)
router.register(r'informations', InformationViewSet)
router.register(r'knowledges', KnowledgeViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'owners', OwnerViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'sales', SaleViewSet, base_name='sales')
router.register(r'points', PointViewSet)
router.register(r'parametrizations', ParametrizationViewSet, base_name='parametrizations')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^_ah/', include('djangae.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'api/', include(router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]
