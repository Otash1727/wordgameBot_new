from django.core.management.base import BaseCommand
from wordgame.models import EnglishDictionary
import csv
csv.field_size_limit(1000000)

class Command(BaseCommand):
    help='upload csv file'
    def handle(self,**args):
        with open('englishDictionary.csv') as cfile:
            reader = csv.reader(cfile)
            for row in reader:
                upload=EnglishDictionary(dictionary=row)
                upload.save()
