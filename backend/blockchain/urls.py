from rest_framework.routers import DefaultRouter
from blockchain.views import SmartContractViewSet, SmartContractDeploymentViewSet

urlpatterns = []
router = DefaultRouter()
router.register(r"smart-contract", SmartContractViewSet)
router.register(r"deploy", SmartContractDeploymentViewSet)

urlpatterns += router.urls
