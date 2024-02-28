from BotScripts.create_bot import bot,dp 
from aiogram import Router,F
from aiogram.filters import Command
from aiogram.types import Message,BotCommand,BotCommandScopeChat,InlineKeyboardButton,CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import BaseFilter
from wordgame.models import GamersList,MatchList,ChempionsList
from BotScripts.functions import BotFuctions

import csv,re,json,itertools
csv.field_size_limit(1000000)
import pandas as pd






import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
    


router=Router()
chat_id=None

#message_id
message_id1=[]
#in_turn




# keyboards
join=(InlineKeyboardButton(text='join',callback_data='join'))
start=(InlineKeyboardButton(text='start',callback_data='start'))
end=(InlineKeyboardButton(text='end',callback_data='end'))

join_kb=InlineKeyboardBuilder()
join_kb.row(join)

mix_kb=InlineKeyboardBuilder()
mix_kb.row(join).row(start)

mix_kb2=InlineKeyboardBuilder()
mix_kb2.row(start).row(end)

End=InlineKeyboardBuilder()
End.row(end)






@router.message(Command('start'))
async def runbot(message:Message):
    await bot.send_message(chat_id=message.from_user.id,text='Hello send /help command to know what you can do with me')
    await bot.send_message(chat_id=message.from_user.id,text='The game is played only with an opponent and in a group.')
    await bot.set_my_commands([BotCommand(command='start',description='Run the bot'),BotCommand(command='help',description='If you want to know more about our bot, this command will help you')],BotCommandScopeChat(chat_id=message.from_user.id))
    BotFuctions.off()
            

    

@router.message(Command('help'))
async def help(message:Message):
    await bot.send_message(chat_id=message.from_user.id,text='This is a word chain game for English learners!')
    await bot.send_message(chat_id=message.from_user.id,text='The game is played only with an opponent and in a group.')
    await bot.send_message(chat_id=message.from_user.id,text="If you want to use the bot,add the bot to your group and give admin and send /new_match")
    await bot.set_my_commands([BotCommand(command='new_macht1',description='Create a new match',)],BotCommandScopeChat(chat_id=message.from_user.id),request_timeout=2)


@router.message(Command('new_match'))
async def fff(message:Message):
    chat_id=message.chat.id
    check_status= await bot.get_chat_member(chat_id=chat_id,user_id=bot.id)
    print(check_status.status)  
    if check_status.status=='administrator':
        last_id=BotFuctions.match_info()
        print(last_id)
        if last_id !=None:
            show_player=BotFuctions.show_players(match_id=last_id.match_ID)    
            if message.from_user.id in [i.user_id  for i in show_player] and last_id.start_game==True and last_id.finished==False:
                if message.text=='/new_match@GameWordEnglishbot':
                    i=message.text
                    print('davom et')
                #ID=message.message_id
                await bot.edit_message_text(chat_id=chat_id,text='davom et' ,message_id=)
        else:
            await bot.send_message(chat_id=chat_id,text="Great, get ready and click on start button below",reply_markup=join_kb.as_markup())        
    else:
        await bot.send_message(chat_id=chat_id,text='You can play only with an opponent(s) and in a group.')
        await bot.send_message(chat_id=chat_id,text="You can play only with an opponent(or more) and in a group.")
    
@router.callback_query(F.data=='join')
async def join_game(callback:CallbackQuery):
    global message_id  
    chat_id=callback.message.chat.id
    chat_info= await bot.get_chat(chat_id=chat_id)
    data=BotFuctions.game_boolen()
    if data==False:
        try:
            data2=BotFuctions.game_info(callback=callback.from_user.id)
            print(data2.start_game,5656)
            if data2.start_game==True and data2.finished==False:    
                await callback.answer(text='You have an unfinished game\n Please finished the game 😡',show_alert=True)
            else:
                create=BotFuctions.create_game(chat_id=chat_id,chat_name=chat_info.title,user_id=callback.from_user.id,user_name=callback.from_user.full_name)
                await callback.answer(text='You are create new game. Please wait for other to join!',show_alert=True)
        except AttributeError:
            create=BotFuctions.create_game(chat_id=chat_id,chat_name=chat_info.title,user_id=callback.from_user.id,user_name=callback.from_user.full_name)
            await callback.answer(text='You are create new game. Please wait for other to join!',show_alert=True)

    else:
        creator=BotFuctions.check_creator(user_id=callback.from_user.id,user_name=callback.from_user.full_name)
        print(creator)
        finish=BotFuctions.finished()
        if finish==False:
            if creator == True:
                await callback.answer(text='You already created the game. Please wait for others to join ‼️',show_alert=True)

            else:
                info=BotFuctions.match_info()
                shown=BotFuctions.show_players(info.match_ID)
                count=len(shown)
                await callback.answer(text='You joined the game',show_alert=True)
                get_id=await callback.message.answer(text=f"Match ID - {info.match_ID} \n Number of players - {count} \n Players -------",
                reply_markup=mix_kb.as_markup())
                message_id1.append(get_id.message_id)
                
        else:
            create=BotFuctions.create_game(chat_id=chat_id,chat_name=chat_info.title,user_id=callback.from_user.id,user_name=callback.from_user.full_name)
            await callback.answer(text='You are create new game. Please wait for other to join!',show_alert=True)
            

@router.callback_query(F.data=='start')
async def start_game(callback:CallbackQuery):
    print(message_id1,'message_id')
    chat_id=callback.message.chat.id
    data=BotFuctions.start_game1()
    info=BotFuctions.match_info()
    shown=BotFuctions.show_players(info.match_ID)
    count=len(shown)
    await bot.edit_message_text(chat_id=chat_id,message_id=message_id1[0],text=f"Match ID - {info.match_ID} \n Number of players - {count} \n Players -------",reply_markup=End.as_markup())
    reply=await callback.message.answer(text=f'{callback.from_user.full_name} start the game',reply_to_message_id=message_id1[0])
    queue=BotFuctions.first_queue()
    await bot.send_message(chat_id=chat_id,text=f'<b><i>{queue[1]}</i></b> must write an English word',reply_to_message_id=reply.message_id,parse_mode=ParseMode.HTML)
    
   
    
@router.message()
async def empty_handler(message:Message):
    chat_id=message.chat.id
    current_game=BotFuctions.current_game(user_id=message.from_user.id)
    if current_game==True:
        current_id=BotFuctions.current_id(user_id=message.from_user.id)
        data=BotFuctions.get_queue(match_id=current_id.match_ID,user_id=message.from_user.id)
        attemp_count=BotFuctions.count_attemp(match_id=current_id.match_ID,user_id=message.from_user.id)
        current_user=BotFuctions.current_user(match_id=current_id.match_ID,user_id=message.from_user.id)
    else:
        pass
    
   
   
    
    
    #show_player=BotFuctions.show_players(match_id=count1) 
    #count=show_player.count()
    #
    
    #print(last_id.queue,data,'equals')
    #data2=BotFuctions.game_info(callback=message.from_user.id)
    #print(data2.finished)
    if current_game==True and current_id.start_game==True and current_id.finished==False and (current_id.queue==data) and current_user.finished==False:            
        print("O'yinchilar soni",current_id.    )
        dd=open('englishDictionary.csv',mode='r') 
    #        csvfile=csv.reader(dd)
    #        episode_one=False
    #        episode_two=[False,False]
    #        
    #        last_letter=BotFuctions.last_letter(match_id=last_id.match_ID)
    #        for i in csvfile:   
    #            if str(message.text.capitalize()) in i and len(message.text)>1:
    #                episode_one=True
    #                BotFuctions.count_queue(match_id=last_id.match_ID)
    #                break
    #            else:
    #                pass
    #        
    #        if last_id.queue==count:
    #                    print(last_id.queue,'equals')
    #                    BotFuctions.delete_queue(match_id=last_id.match_ID)
    #        
    #        # message text rigth or wrong 
    #        if episode_one==True:
    #            print('hello')
    #            gg=BotFuctions.found_word(match_id=last_id.match_ID,text=json.dumps(message.text))
    #            for i in gg:
    #                pass
    #            if str(message.text) not in i.founded_words.split('""'):
    #                print('hello baby')
    #                BotFuctions.found_word_save(match_id=last_id.match_ID,text=json.dumps(message.text),last_letter=message.text[-1])
    #                episode_two[0]=True
    #            else:
    #                episode_two[1]=True
    #                print(episode_two[1])
#
    #        
#
    #        else:
    #            BotFuctions.chance_over(match_id=last_id.match_ID,user_id=message.from_user.id)
    #            attemp_count=BotFuctions.count_attemp(match_id=last_id.match_ID,user_id=message.from_user.id)
    #            if attemp_count!=0:
    #                attemp_count=BotFuctions.count_attemp(match_id=last_id.match_ID, user_id=message.from_user.id)
    #                ID=message.message_id
    #                await bot.send_message(chat_id=chat_id,reply_to_message_id=ID,text=f"I can't recognize <del>{message.text.upper()}</del> as a word",parse_mode=ParseMode.HTML)           
    #                
    #            else:
    #                win_user=BotFuctions.win_user(match_id=last_id.match_ID)
    #                ddd=win_user.count()
    #                
    #                if ddd==1:
    #                    for i1 in win_user:
    #                        pass
    #                    #await bot.send_message(f'<spoiler><b>{i1.user_name}</b></spoiler> You win ')
    #                    await bot.send_message(chat_id=chat_id,text='<b>You lose</b>',parse_mode=ParseMode.HTML)
    #                    BotFuctions.finished_users(match_id=last_id.match_ID,user_id=message.from_user.id)
    #                    print('bye bye')
    #                
#
#
#
#
    #    # words function
#
    #        if episode_two[0]==True:
    #            last_letter=BotFuctions.last_letter(match_id=last_id.match_ID)
    #            print(last_letter)
    #            print('keyingi navbat')
    #            new_queue=BotFuctions.new_queue(match_id=last_id.match_ID)
    #            get_name=BotFuctions.name_queue(match_id=last_id.match_ID,queue=new_queue)
    #            await bot.send_message(chat_id=chat_id,text=f"<b>{get_name}</b>, It is your turn. send a word for  <b>{last_letter.upper()}</b>",parse_mode=ParseMode.HTML)
#
    #        elif episode_two[1]==True:
    #            #next_queue=BotFuctions.name_queue(match_id=last_id.match_ID,queue=)
    #            await bot.send_message(chat_id=chat_id,text='this word used before')
    
    elif current_game==True and current_id.queue!=data:
        print(data)
        current_queue=BotFuctions.current_queue(match_id=current_id.match_ID,queue=current_id.queue)
        await bot.send_message(chat_id=chat_id,text=f"Sorry {message.from_user.full_name},it's not your turn\nPlease wait\nit's your turn-{data}\n Now it is<b>{current_queue.user_name}</b>",parse_mode=ParseMode.HTML)
                  


    else:   
        print('oddiy rejim')
        print(current_game,4545)
        await bot.set_my_commands([BotCommand(command='new_match',description='Star new match')],BotCommandScopeChat(chat_id=chat_id))

                        
        
        
        
        
         






           
    #finished true will be progress false
#    
#    
#    print(data)
#  #  print(chat_info)
#    data_id=BotFuctions.get_ID(chat_id=chat_id,chat_name=chat_info.title)
#    print(data_id[1])
#    if data_id[1]==True:
#        players=BotFuctions.connect_gamers(user_id=callback.from_user.id,user_name=callback.from_user.full_name,match_ID=data_id[0])
#        show=BotFuctions.show_players(match_id=data_id[0])
#        
#        await callback.message.answer(text=f"Match_ID: {data_id[0]}\nPlayers:\n{[i.user_name  for i in show]}")
#    


    #try:
    #    if last_match.finished ==False:
    #      
    #            data=BotFuctions.check_users(callback=callback.message.from_user.id) 
    #            print(data)     
    #            await callback.answer('You are practicipating in the game',show_alert=True)
    #    elif last_match.finished==True:
    #        await callback.answer('You are already practicipating in the game!\n Please wait for others to join',show_alert=True)
    #        fsm_save=MatchList(channel_name=channel_info.title,channel_ID=channel_info.id)
    #        fsm_save2=GamersList(user_id=callback.from_user.id,user_name=callback.from_user.full_name,match_ID=last_match.match_ID+1)
    #        fsm_save.save()
    #        fsm_save2.save()
    #except AttributeError:
    #    pass
        
   

    
    

    



            #
            ##episode one yozilgan so'zni to'gri yoki yo'qligini aniqlaydi
            #if episode_one==True:
            #    
            #    
#
#
#
            #
            #else:
            #    
#
#
#
#
#
            #if episode_two[1]==True:
            #    ID=message.message_id
            #    last_letter=BotFuctions.last_letter(match_id=last_id.match_ID)
            #    await bot.send_message(chat_id=chat_id,reply_to_message_id=ID,text=f'This word has been used before\nPlease write another word\n send a word for <b>{last_letter.upper()}</b>',parse_mode=ParseMode.HTML)
          #
#
            #
#
            #            print(message.from_user.id)
            #        if last_id.queue==count:
            #            print(last_id.queue,'equals')
            #            BotFuctions.delete_queue(match_id=last_id.match_ID)
            #        break  
            #    elif last_letter==None:
            #        BotFuctions.count_queue(match_id=last_id.match_ID)
            #        gg=BotFuctions.found_word(match_id=last_id.match_ID,text=json.dumps(message.text))
            #        for i in gg:
            #            pass
            #        print('hello baby 1')
            #        word[0]=True
            #        BotFuctions.found_word_save(match_id=last_id.match_ID,text=json.dumps(message.text),last_letter=message.text[-1])
            #        word[1]=False
            #        
            #        break
            #    else:
            #        word[2]=True  
            #else:
            #    print('off')
               
           
            #
            #  #elif word[2]==True:
            #    await bot.send_message(chat_id=chat_id,text='sen')
            #else:
            #
    #elif message.from_user.id in [i.user_id  for i in show_player]:
    #   

 
            