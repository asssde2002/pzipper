from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class ContractStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        contract_location = os.path.join(settings.BASE_DIR, "blockchain/contracts")
        super().__init__(location=contract_location, *args, **kwargs)
