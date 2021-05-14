from django.core.management.base import BaseCommand
from django.utils import timezone
from substitute.data_import.link_api_db import LinkApiDb


class Command(BaseCommand):
    help = "Import food from api (open food fact)"

    def handle(self, *args, **kwargs):
        obj = LinkApiDb()
        obj.add_in_table(1, 1)
