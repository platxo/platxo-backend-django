"""platxo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from products.api import ProductCategoryViewSet, ProductTypeViewSet, ProductViewSet
from services.api import ServiceCategoryViewSet, ServiceTypeViewSet, ServiceViewSet
from sales.api import SaleViewSet
from purchases.api import PurchaseViewSet
from contact.api import ContactViewSet
from business.api import DataViewSet, InformationViewSet, KnowledgeViewSet

router = routers.DefaultRouter()
router.register(r'product_categories', ProductCategoryViewSet)
router.register(r'product_types', ProductTypeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'service_categories', ServiceCategoryViewSet)
router.register(r'service_types', ServiceTypeViewSet)
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
    url(r'api/', include(router.urls)),
]
