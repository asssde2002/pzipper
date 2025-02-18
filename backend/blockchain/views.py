from blockchain.models import SmartContract, SmartContractDeployment
from blockchain.serializers import SmartContractSerializer, SmartContractDeploymentSerializer
from blockchain.controllers import CounterSmartContractController

from rest_framework import viewsets, status as DRF_status
from utils.decorators import DRF_response
from utils.exceptions import MissingInputError, AlreadyExistError, UserError, InternalServerError
from pathlib import Path
from rest_framework.decorators import api_view, action
from web3 import Web3
from django.conf import settings


@api_view(["GET"])
@DRF_response
def ping_hardhat(request):
    w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_URL))
    if not w3.is_connected():
        raise InternalServerError("Hardhat node does not start")


class SmartContractViewSet(viewsets.GenericViewSet):
    queryset = SmartContract.objects.all().order_by("-created_at")
    serializer_class = SmartContractSerializer

    @DRF_response
    def create(self, request):
        data_file = request.FILES.get("data", None)
        if not data_file:
            raise MissingInputError("no file")
        
        file_name = Path(data_file.name).stem 
        contract_interface = SmartContract.get_contract_interface(data_file)
        defaults = {
            "contract_abi": contract_interface["abi"],
            "contract_bytecode": contract_interface["bin"],
            "contract_file": data_file,
        }
        smart_contract, is_created = SmartContract.objects.get_or_create(contract_name=file_name, defaults=defaults)
        if not is_created:
            raise AlreadyExistError(f"file name ({file_name})")
        
        serializer = self.get_serializer(smart_contract)
        return serializer.data, DRF_status.HTTP_201_CREATED
    
    @DRF_response
    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        return serializer.data
    

class SmartContractDeploymentViewSet(viewsets.GenericViewSet):
    queryset = SmartContractDeployment.objects.all().order_by("-deployed_at")
    serializer_class = SmartContractDeploymentSerializer

    @DRF_response
    def create(self, request):
        request_data = request.data
        contract_id = request_data.get("contract_id")
        smart_contract = SmartContract.objects.get(id=contract_id)
        try:
            deployment = smart_contract.deploy()
            serializer = self.get_serializer(deployment)
            return serializer.data, DRF_status.HTTP_201_CREATED
        except Exception:
            raise UserError(f"smart contract({contract_id}) deployed failed")

    @DRF_response
    def list(self, request):
        contract_id = request.query_params.get("contract_id")
        if not contract_id:
            raise MissingInputError("contract_id is necessary")
        
        queryset = self.queryset.select_related("smart_contract").filter(smart_contract_id=contract_id)
        serializer = self.get_serializer(queryset, many=True)
        return serializer.data


class CounterSmartContractViewSet(viewsets.GenericViewSet):
    CONTRACT_NAME = "Counter"
    queryset = SmartContractDeployment.objects.select_related("smart_contract").filter(smart_contract__contract_name=CONTRACT_NAME).order_by('-deployed_at')
    serializer_class = SmartContractSerializer
    controller_class = CounterSmartContractController

    @action(detail=False, methods=["post"], url_path="increase-count")
    @DRF_response
    def increase_count(self, request):
        deployment = self.queryset.first()
        controller = self.controller_class(deployment)
        controller.increase_count()
        
    
    @action(detail=False, methods=["get"], url_path="get-count")
    @DRF_response
    def get_count(self, request):
        deployment = self.queryset.first()
        controller = self.controller_class(deployment)
        curr_count = controller.get_count()
        return {"current_count": curr_count}
    