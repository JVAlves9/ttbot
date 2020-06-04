from dotenv import load_dotenv as ld
from bs4 import BeautifulSoup as bs
import requests
import os, re, json

#API settings
BASE = os.path.abspath(os.path.dirname(__file__))
ld(os.path.join(BASE,'credentials.env'))
API_KEY = os.getenv('API_KEY')
ID=os.getenv('ID')
#wiki API pre settings
password = os.getenv('password')
username = os.getenv('username')
#weather api key
weather_api_key = os.getenv('weather_api_key')

def weather():
    url = f'http://api.openweathermap.org/data/2.5/weather?appid={weather_api_key}&id=3390760'
    resp = requests.get(url).json()
    if resp['cod'] != '404':
        temp = resp['main']
        tempe = round(float(temp['temp']-273.15),2)
        feels = round(float(temp['feels_like']-273.15),2)
        descr = resp['weather'][0]['description']
    return f"Temperature around {tempe}°C, with {descr}, feels like {feels}"

def getPic(pic:str,name:str=None,num=0):
    pattern = r'(\.[\w]+)' #pattern to take just the extension of the file
    if name == None:
        name = pic
    try:
        if pic.startswith('http'):#if it's already a link
            img = requests.get(pic).content
            dot = re.findall(pattern,pic)[-1]#search for the extension type on the link
        else:
            url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={ID}&q={pic}&searchType=image'
            data = requests.get(url).json()
            items = data['items']
            item0 = items[num]['link']
            img = requests.get(item0).content
            dot = re.findall(pattern,item0)[-1]
        with open(f'pics\\{name+dot}','wb') as f:
            f.write(img)
        return f'pics\\{name+dot}'
    except:
        if num !=3:
            return getPic(pic,name,num+1)
        else:
            raise
def search(sub:str):
    session = requests.Session()#session to mantain cookies for login purposes
    #wiki API settings
    log='https://www.mediawiki.org/w/api.php'
    log_params0 = {
        'action':'query',
        'meta':'tokens',
        'type':'login',
        'format':'json'
    }
    req = session.get(url=log,params=log_params0)
    log_data = req.json()
    login_token=log_data['query']['tokens']['logintoken']
    log_params1 = {
        'action':'login',
        'lgname':f'{username}',
        'lgpassword':f'{password}',
        'lgtoken':login_token,
        'format':'json'
    }
    req = session.post(log,data=log_params1)
    #search on wiki
    url = 'https://pt.wikipedia.org/w/api.php'
    srch_params = {
        'action':'query',
        'format':'json',
        'list':'search',
        'srlimit':1,
        'srsearch':sub
    }
    req1 = session.get(url=url,params=srch_params)
    title = req1.json()['query']['search'][0]['title'].replace(' ','_')
    page_params = {
        'action':'query',
        'titles':title,
        'prop':'extracts',
        'exlimit':1,
        'exchars':400,
        'explaintext':1,
        'formatversion':2,
        'format':'json'
    }
    req1=session.get(url=url,params=page_params)
    content = req1.json()
    return content['query']['pages'][0]['extract'].replace('...','.')
