from django.db import models
from backend.storage_backends import ContractStorage

def contract_upload_to(instance, filename):
    return filename

class SmartContract(models.Model):
    contract_file = models.FileField(storage=ContractStorage, upload_to=contract_upload_to)
    contract_name = models.TextField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SmartContractDeployment(models.Model):
    smart_contract = models.ForeignKey("blockchain.SmartContract", on_delete=models.CASCADE)
    address = models.CharField(max_length=42, unique=True, db_index=True)
    transaction_hash = models.CharField(max_length=66, unique=True, db_index=True)
    deployed_at = models.DateTimeField(auto_now_add=True)

