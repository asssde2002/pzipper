from blockchain.models import SmartContract, SmartContractDeployment
from blockchain.serializers import SmartContractSerializer, SmartContractDeploymentSerializer

from rest_framework import viewsets, status as DRF_status
from utils.decorators import DRF_response
from utils.exceptions import MissingInputError, AlreadyExistError, UserError
from pathlib import Path


class SmartContractViewSet(viewsets.GenericViewSet):
    queryset = SmartContract.objects.all()
    serializer_class = SmartContractSerializer

    @DRF_response
    def create(self, request):
        data_file = request.FILES.get("data", None)
        if not data_file:
            raise MissingInputError("no file")
        
        file_name = Path(data_file.name).stem 
        smart_contract, is_created = SmartContract.objects.get_or_create(contract_name=file_name, defaults={"contract_file": data_file})
        if not is_created:
            raise AlreadyExistError(f"file name ({file_name})")
        
        serializer = self.get_serializer(smart_contract)
        return serializer.data, DRF_status.HTTP_201_CREATED
    

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

    