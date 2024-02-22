from django.core.exceptions import ObjectDoesNotExist
from BotScripts.create_bot import bot
from wordgame.models import MatchList,GamersList,ChempionsList,EnglishDictionary
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()



def game_boolen():
    start_or_not=False
    try:
        last_progress=MatchList.objects.last()
        data2=GamersList.objects.last()
        if last_progress.progress=='active':
            if last_progress.start_game==False:
                start_or_not=True
                return start_or_not
            else:
                
                return start_or_not 
        else:
            if last_progress.start_game==False:
                return start_or_not      
            else:
                start_or_not=True
                return start_or_not 
    except AttributeError:
        return start_or_not     

 
def check_creator(user_id,user_name):
    exists=False
    try:
        data=MatchList.objects.last()
       
        check_user=GamersList.objects.filter(match_ID=data.match_ID)
        if user_id in [i.user_id for i in check_user ]:
            exists=True
            return  exists
        else:
            print('bu yerga')
            last_queue=GamersList.objects.last()
            fsm=(GamersList(user_id=user_id,user_name=user_name,match_ID=data.match_ID,queue=last_queue.queue+1))
            fsm.save()
            return exists
    except (ObjectDoesNotExist,AttributeError):
        return exists,print(404)
    

def create_game(chat_id,chat_name,user_id,user_name):
    data=MatchList(channel_name=chat_name,channel_ID=chat_id)
    data.save()
    copy_data=MatchList.objects.last()
    copy_data.progress='active'
    copy_data.save()
    creator=GamersList(user_id=user_id,user_name=user_name,match_ID=copy_data.match_ID)
    creator.save()

def match_info():
    last_match=MatchList.objects.last()
    return last_match

def show_players(match_id):
    data=GamersList.objects.filter(match_ID=match_id)   
    return data

def start_game1():
        last_match=MatchList.objects.last()
        change_start=GamersList.objects.filter(match_ID=last_match.match_ID)
        for i in change_start:
            i.start_game=True
            i.save()
        last_match.start_game=True
        last_match.save()
        return print(last_match.start_game)

def first_queue():
    queue=GamersList.objects.filter(queue=1)
    for i in queue:
        return i.user_id,i.user_name

def get_queue(match_id,user_id):
    queue=GamersList.objects.filter(match_ID=match_id,user_id=user_id)
    for i in queue:
        return i.queue  
         
def count_queue(match_id):
    last_match=MatchList.objects.filter(match_ID=match_id)
    for i in last_match:
        i.queue+=1
        i.save()

def delete_queue(match_id):
    last_match=MatchList.objects.filter(match_ID=match_id)
    for i in last_match:
        i.queue=1
        i.save()

def name_queue(match_id,queue):
    data=GamersList.objects.filter(match_ID=match_id,queue=queue)
    for i in data:
        return i.user_name

def finished():
    last_match=MatchList.objects.last()
    return last_match.finished

def dictionary1(message):
    word=EnglishDictionary.objects.all()
    return word

def game_info(callback):    
    data=GamersList.objects.filter(user_id=callback).last()
    return data 


def off():
    oddd=GamersList.objects.all()
    oddd.delete()
    dd=MatchList.objects.all()
    dd.delete()

     