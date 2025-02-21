from django.db.models.signals import post_save
from django.dispatch import receiver
from blockchain.models import SmartContractDeployment


@receiver(post_save, sender=SmartContractDeployment, dispatch_uid="on_deployment_post_save")
def smart_contract_deployment_post_save(sender, instance, created, **kwargs):
    if created:
        del SmartContractDeployment.get_latest_deployment.cache[instance.smart_contract.contract_name]
    