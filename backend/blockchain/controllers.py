from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from django.conf import settings

class CounterSmartContractController:
    def __init__(self, deployment):
        self.deployment = deployment
        self.w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_URL))
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        self.account = self.w3.eth.account.from_key(settings.BLOCKCHAIN_ACCOUNT_PRIVATE_KEY)
        self.account_address = self.account.address
        self.contract = self.w3.eth.contract(address=self.deployment.address, abi=deployment.smart_contract.contract_abi)

    def increase_count(self):
        tx_hash = self.contract.functions.increment().transact({
            "from": self.account_address, 
            "gas_price": self.w3.eth.gas_price
        })
        self.w3.eth.wait_for_transaction_receipt(tx_hash)


    def get_count(self):
        return self.contract.functions.count().call()

