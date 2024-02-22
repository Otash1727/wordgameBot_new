from django.core.management.base import BaseCommand
from BotScripts.create_bot import dp,bot
from BotScripts.handlers import BotAdmin

class Command(BaseCommand):
    help='Otabek'
    def handle(self,*args, **kwargs):
        print('Bot online....')
        dp.include_router(BotAdmin.router)
        dp.run_polling(bot)