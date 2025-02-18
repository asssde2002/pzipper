from rest_framework.routers import DefaultRouter
from blockchain.views import SmartContractViewSet, SmartContractDeploymentViewSet, ping_hardhat
from django.urls import path

urlpatterns = [
    path("ping-hardhat/", ping_hardhat),
]

router = DefaultRouter()
router.register(r"smart-contract", SmartContractViewSet)
router.register(r"deploy", SmartContractDeploymentViewSet)

urlpatterns += router.urls
