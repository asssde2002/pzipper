import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class ContractStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        contract_location = os.path.join(settings.BASE_DIR, "blockchain/contracts")
        super().__init__(*args, location=contract_location, **kwargs)
