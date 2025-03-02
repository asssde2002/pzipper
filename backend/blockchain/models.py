from django.db import models
from django.conf import settings
from backend.storage_backends import ContractStorage
from web3 import Web3
from cachetools import cached
from utils.decorators import RedisTTLCache
from utils.exceptions import UserError
import solcx


def contract_upload_to(instance, filename):
    return filename

class SmartContract(models.Model):
    contract_file = models.FileField(storage=ContractStorage, upload_to=contract_upload_to)
    contract_name = models.TextField(unique=True)
    contract_abi = models.JSONField(default=list)
    contract_bytecode = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_contract_interface(file):
        solc_version = settings.BLOCKCHAIN_SOLIDITY_VERSION
        if solc_version not in solcx.get_installed_solc_versions():
            solcx.install_solc(solc_version)

        contract_source_code = ""
        for chunk in file.chunks():
            contract_source_code += chunk.decode("utf-8")

        compiled_sol = solcx.compile_source(
            contract_source_code, output_values=["abi", "bin"], solc_version=solc_version
        )
        contract_interface = next(iter(compiled_sol.values()))

        return contract_interface

    def deploy(self):
        w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_URL))
        deployer_account = w3.eth.account.from_key(settings.BLOCKCHAIN_ACCOUNT_PRIVATE_KEY)
        deployer_account_address = deployer_account.address

        contract = w3.eth.contract(abi=self.contract_abi, bytecode=self.contract_bytecode)
        tx_hash = contract.constructor().transact({
            "from": deployer_account_address,
            "gas_price": w3.eth.gas_price,
        })
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt["status"] == "0":
            raise UserError("Transaction failed")

        contract_address = tx_receipt.contractAddress
        deployment_data = {
            "smart_contract": self,
            "address": contract_address,
            "transaction_hash": f"0x{tx_hash.hex()}",
        }
        deployment = SmartContractDeployment.objects.create(**deployment_data)
        
        return deployment
        

class SmartContractDeployment(models.Model):
    smart_contract = models.ForeignKey("blockchain.SmartContract", on_delete=models.CASCADE)
    address = models.CharField(max_length=42, unique=True)
    transaction_hash = models.CharField(max_length=66, unique=True)
    deployed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["smart_contract", "deployed_at"]),
        ]
    
    @staticmethod
    @cached(RedisTTLCache("sc-deployment", timeout=300))
    def get_latest_deployment(contract_name):
        queryset = SmartContractDeployment.objects.select_related("smart_contract").filter(smart_contract__contract_name=contract_name).order_by('-deployed_at')
        return queryset.first()


