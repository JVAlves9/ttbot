from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import time
import requests

def weather():
    driver = wd.Chrome("\\Users\\Joao Victor\\Documents\\chromedriver.exe")
    tempe =""
    feels=""
    text=""
    driver.get("https://www.accuweather.com/pt/br/recife/45090/weather-forecast/45090")
    content = driver.page_source
    soup = bs(content,features="html.parser")
    temp = soup.find(attrs={'class':'day-panel'})
    temp = temp.findChildren('div')
    tempe = temp[0].findChild(attrs={'class':'high'}).text
    feels = temp[1].text
    text = temp[2].text
    ch=""
    for a in tempe:
        if a.isnumeric() or a == '°':
            ch+=a
    tempe = ch
    ch=""
    for a in feels:
        if a.isnumeric() or a == '°':
            ch+=a
    feels = ch        
    text = text.split("\n")
    text = "".join(text)
    text = text.split("\t")
    text = "".join(text)
    driver.quit()
    return "A temperatura está em {0}, {1},com sensação térmica de {2}".format(tempe,text.lower(),feels)


def googleSearch(driver,sub,isPic=False): #can search on google or google images, just put True in isPic if you want pics
    if isPic:
        driver.get("https://www.google.com/imghp?hl=pt-BR")
    else:
        driver.get('https://www.google.com.br')
    time.sleep(3)
    srcharea = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    srcharea.send_keys(sub)
    srcharea.submit()

def getPic(pic,name=None,num=1):
    if(name == None):
        name = pic
    driver = wd.Chrome("\\Users\\Joao Victor\\Documents\\chromedriver.exe")
    try:
        if pic.startswith('http'):
            driver.get(pic)
        else:
            googleSearch(driver,pic,True)
            
            imgs = driver.find_element_by_xpath('//*[@id="islrg"]').find_elements_by_tag_name('img')
            imgs[num].click()
            time.sleep(2)
            img = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img')
            driver.get(img.get_attribute('src'))

        time.sleep(3)
        img = driver.find_element_by_tag_name('img')
        with open("pics\\{0}.jpg".format(name),'wb') as f:
            f.write(requests.get(img.get_attribute('src')).content)
            driver.quit()
        return 'pics\\{0}.jpg'.format(name)
    except NoSuchElementException:
        driver.quit()
        raise
    except:
        driver.quit()
        return getPic(pic,name,num+1)

def wiki(driver,sub):
    driver.get('https://www.wikipedia.org')
    time.sleep(3)
    srch = driver.find_element_by_xpath('//*[@id="searchInput"]')
    srch.send_keys(sub)
    srch.submit()
    time.sleep(3)

def search(sub):
    driver = wd.Chrome("\\Users\\Joao Victor\\Documents\\chromedriver.exe")
    
    try:
        wiki(driver,sub)
        content = driver.page_source
        soup = bs(content,features="html.parser")
        children = soup.find(name='div',attrs={'class':'mw-parser-output'})
        templs = children.findChildren(name='p')
        temp = templs[0]
        for a in templs:
            if a ==templs[0]:
                continue
            elif len(temp.findParents()) > len(a.findParents()):
                temp = a
            elif len(temp.findParents())==len(a.findParents()):
                break
        text = temp.text
        for a in text:
            if a.isnumeric():
                text = text.replace('[{0}]'.format(a),'')
        driver.quit()
        return text.replace('\n','')
    except:
        driver.quit()
        raise
