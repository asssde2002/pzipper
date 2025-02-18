from rest_framework import serializers
from blockchain.models import SmartContract, SmartContractDeployment


class SmartContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartContract
        fields = ["id", "contract_name", "created_at"]


class SmartContractDeploymentSerializer(serializers.ModelSerializer):
    contract_name = serializers.SerializerMethodField()

    def get_contract_name(self, obj):
        return obj.smart_contract.contract_name

    class Meta:
        model = SmartContractDeployment
        fields = ["contract_name", "address", "deployed_at"]