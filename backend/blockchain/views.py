from blockchain.models import SmartContract

from rest_framework import viewsets, status as DRF_status
from utils.decorators import DRF_response
from utils.exceptions import MissingInputError, AlreadyExistError
from pathlib import Path


class SmartContractViewSet(viewsets.GenericViewSet):
    queryset = SmartContract.objects.all()

    @DRF_response
    def create(self, request):
        data_file = request.FILES.get("data", None)
        if not data_file:
            raise MissingInputError("no file")
        
        file_name = Path(data_file.name).stem 
        smart_contract, is_created = SmartContract.objects.get_or_create(contract_name=file_name, defaults={"contract_file": data_file})
        if not is_created:
            raise AlreadyExistError(f"file name ({file_name})")

        return {"smart_contract_id": smart_contract.id}, DRF_status.HTTP_201_CREATED
    