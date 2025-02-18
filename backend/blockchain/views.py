from blockchain.models import SmartContract

from rest_framework import viewsets, status as DRF_status
from utils.decorators import DRF_response

class SmartContractViewSet(viewsets.GenericViewSet):
    queryset = SmartContract.objects.all()

    @DRF_response
    def create(self, request):
        
        data_file = request.FILES.get("data", None)
        print('here', data_file)
        smart_contract = SmartContract.objects.create(contract_file=data_file)

        return {"smart_contract_id": smart_contract.id}, DRF_status.HTTP_201_CREATED
    