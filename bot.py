import tweepy as tp
import time
import weather
from dotenv import load_dotenv as ld
import os

#getting the credentials from de .env file
BASE = os.path.abspath(os.path.dirname(__file__))
ld(os.path.join(BASE,'credentials.env'))
consumerUserKey = os.getenv('consumerUserKey')
consumerUserSKey = os.getenv('consumerUserSKey')
appt = os.getenv('appt')
appts = os.getenv('appts')
#setting the authenticator
auth = tp.OAuthHandler(consumerUserKey,consumerUserSKey)
auth.set_access_token(appt, appts)
api = tp.API(auth, wait_on_rate_limit=True) #used to make actions at the tt account

def verifyDmText(api):
    dms = verifyDm(api)
    if dms !=[]:
        for a in dms:
            try:
                if a.startswith('#newpic'):
                    temp = a.replace('#newpic ','')
                    pic = weather.getPic(temp,'profile pic')
                    api.update_profile_image(pic)
                elif a.startswith('#newback'):
                    temp = a.replace('#newback','')
                    pic = weather.getPic(temp)
                    api.update_profile_banner(pic)
            except NoSuchElementException:
                    api.send_direct_message(577376111,'Problem with the html elements, they must\'ve been changed' + u'\u1F614')

def verifyDm(api):
    try:
        ndm = api.list_direct_messages()
        dmIds = []
        ids = []
        with open('ids.txt') as f:
            temp2 = f.readlines()
            for a in ndm:
                temp = a.__dict__
                if temp['id']+'\n' not in temp2:
                    dmIds.append(temp['id'])
                    ids.append(temp['message_create']['message_data']['text'])
        with open('ids.txt','a') as f:
            for a in dmIds:
                f.write(a+'\n')
        return ids
    except FileNotFoundError:
        with open('ids.txt','w') as f:
            f.write('')
        return verifyDm(api)

def verifyTextMentions(api):
    mentions = verifyMentions(api)
    if mentions != {}:
        for a in mentions:
            if '#searchforme' in mentions[a].lower():
                temp = mentions[a].replace('@storyte13743308 ','').lower().replace('#searchforme','')
                try:
                    search = weather.search(temp)
                    while len(search) > 280: #try to reduce to 280 by taking text between dots
                        temp2 = search.split('.')
                        if len(temp2) ==1:
                            break
                        temp2.remove(temp2[-1])
                        search = '.'.join(temp2)
                    while len(search) > 280:#try to reduce to 280 by taking text between commas
                        temp2 =search.split(',')
                        temp2.remove(temp2[-1])
                        search = ','.join(temp2)
                    search+='.'
                    api.update_status(search,a)
                    pic = weather.getPic(temp)
                    api.upload_with_media(pic,a)
                except NoSuchElementException:
                    api.send_direct_message(577376111,'Problem with the html elements, they must\'ve been changed')
                except:
                    api.update_status('We couldn\'t find anything about this. Please, try with again changing your words',a)

def verifyMentions(api):
    try:
        ntl= api.mentions_timeline() #get mentions at the time
        tlIds = []
        ids = {}
        with open('idsTl.txt') as f:
            temp2 = f.readlines() #get the ids of the mentions that were already answered in the archive
            for a in ntl:
                temp = a.__dict__ 
                if temp['id_str']+'\n' not in temp2: #verify if the mentions are in the archive
                    tlIds.append(temp['id_str'])
                    ids[temp['id']] = temp['text']
        with open('idsTl.txt','a') as f:
            for a in tlIds:
                f.write(a+'\n')
        return ids
    except FileNotFoundError:
        with open('idsTl.txt','w') as f:
            f.write('')
        return verifyMentions(api)

def verifyTime(tempo):
    now = int(time.strftime('%M',time.gmtime()))
    temp = tempo+20
    if temp > 60:
        temp = temp-60
    if temp == now:
        return True
    return False

ch= ''
ch2=''
tempo = 0
while True:
    time.sleep(20)
    verifyDmText(api)
    verifyTextMentions(api)
    if tempo==0 or verifyTime(tempo):
        tempo = int(time.strftime('%M',time.gmtime()))
        api.update_status(time.asctime())
        ch = ""
        ch = weather.weather()
        if ch2 !=ch:
            api.update_status(ch)
            ch2 =ch
    
