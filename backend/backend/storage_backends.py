from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class ContractStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        contract_location = os.path.join(settings.BASE_DIR, "blockchain/contracts")
        super().__init__(location=contract_location, *args, **kwargs)

    def url(self, name):
        # Return the correct URL with MEDIA_URL prefix
        return os.path.join(settings.MEDIA_URL, 'contracts', name)