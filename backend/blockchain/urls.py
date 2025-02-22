from rest_framework.routers import DefaultRouter
from blockchain.views import SmartContractViewSet, SmartContractDeploymentViewSet, ping_hardhat, CounterSmartContractViewSet
from django.urls import path

urlpatterns = [
    path("ping-hardhat/", ping_hardhat),
]

router = DefaultRouter()
router.register(r"smartcontract", SmartContractViewSet, basename="smartcontract")
router.register(r"deployment", SmartContractDeploymentViewSet, basename="smartcontractdeployment")
router.register(r"smartcontract-counter", CounterSmartContractViewSet, basename="smartcontractcounter")

urlpatterns += router.urls

