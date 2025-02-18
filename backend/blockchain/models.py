from django.db import models
from backend.storage_backends import ContractStorage

class SmartContract(models.Model):
    contract_file = models.FileField(storage=ContractStorage, upload_to="")
    created_at = models.DateTimeField(auto_now_add=True)


class SmartContractDeployment(models.Model):
    smart_contract = models.ForeignKey("blockchain.SmartContract", on_delete=models.CASCADE)
    address = models.CharField(max_length=42, unique=True, db_index=True)
    transaction_hash = models.CharField(max_length=66, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

