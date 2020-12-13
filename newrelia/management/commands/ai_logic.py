from django.core.management.base import BaseCommand
from demo import ai_logic


class Command(BaseCommand):
    help = "AI"

    def handle(self, *args, **options):
        ai_logic.main()
