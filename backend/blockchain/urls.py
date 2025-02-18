from rest_framework.routers import DefaultRouter
from blockchain.views import SmartContractViewSet

urlpatterns = []
router = DefaultRouter()
router.register(r"smart-contract", SmartContractViewSet)

urlpatterns += router.urls
