from flask import Flask
from flask import request
import urllib
import requests
from bs4 import BeautifulSoup
import re
import os
import os.path, time
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route("/")
def hello():
    return "Main!"
@app.route("/product")
def product():
    diff=5000
    product = input("상품을 입력하세요 : ")
    # 
    if os.path.isfile("savedata/"+product+".save.txt"):
        mtime = os.path.getmtime("savedata/"+product+".save.txt")
        now=time.time()
        diff=now-mtime
    if diff>3600:
        url = "https://www.coupang.com/np/search?component=&q="+ product +"&channel=user"
        headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

        res = requests.get(url, headers=headers)
        html=res.content
        soup = BeautifulSoup(html, 'html.parser')
        a = []
        n=0
        ImgUrl=[]
        img=soup.find_all('img', {'class':'search-product-wrap-img'})
        for imglist in img:
            c=soup.find_all('img', {'src':re.compile('\.\.\/img\/gifts/img.*\.jpg')})
            a.append(imglist['src'])
        soup= BeautifulSoup(res.text, "lxml")
        titles = soup.select('#productList > li')
        number= 0
        product_ti=[]
        product_pr=[]
        for title in titles:
            product_title= title.select_one('a > dl > dd > div >div.name').text
            product_price= title.select_one('a > dl > dd > div > div > div > div > em >strong.price-value').text
            product_title= re.sub('\n','', product_title)
            product_price= re.sub('\n','', product_price)
            product_title= product_title.lstrip()
            product_ti.append(product_title)
            product_price= product_price.lstrip()
            product_pr.append(product_price)
            with open("savedata/"+product+".save.txt","a", encoding='utf-8') as f:
                f.write("[%d] %s %s원\n" % (number+1, product_title, product_price))
            ImgUrl0=a[number].replace("//","https://")
            ImgUrl.append(ImgUrl0)
            urllib.request.urlretrieve(ImgUrl[number], f"imgs/"+'['+ str(number+1) + '] '+ str(product_title)+".jpg" )
            print('['+ str(number+1) + ']', product_title, product_price+'원')
            print(ImgUrl[number])
            number= number+ 1
            if number==8:
                break
    else:
        r = open("savedata/"+product+".save.txt", mode='rt', encoding='utf-8')
        print(r.read())
        r.close
    return(product)
@app.route("/news")
def news():
    URL='https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=241&sid1=103&date=20210720&page=1'
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res= requests.get(URL, headers=headers)
    res.raise_for_status()
    soup= BeautifulSoup(res.text, "lxml")
    titles = soup.select('#main_content > div > ul > li >dl')
    number= 0
    for title in titles:
        number= number+ 1
        news_title= title.select('dt>a')
        if news_title[0].text.lstrip() == "":
            pt = news_title[1].text
        else:
            pt = news_title[0].text
        news_content= title.select_one('dd > span').text
        pt=pt.lstrip()
        pt=pt.rstrip()
        pt= re.sub('\n ','', pt)
        news_content= re.sub('\n','', news_content)
        news_content= news_content.lstrip()
        print('['+str(number)+'] '+ pt+ '\n'+ news_content)
        print('--------------------------------------------------------------------------------------------------------')
    return news_content
@app.route("/news2")
def news2():
    search=input("검색어를 입력하세요 :")
    raw = requests.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+ search,
                    headers={'User-Agent':'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")

    articles = html.select("ul.list_news > li")

    for news in articles:
        title = news.select_one("a.news_tit").text
        source = news.select_one("a.api_txt_lines.dsc_txt_wrap").text
        company = news.select_one("a.info.press").text
        print('----------------------------------------------------------------------------------')
        print(title + '----'+ company+'\n----------------------------------------------------------------------------------\n'+source+'\n')
    return title
if __name__ == "__main__":
    app.run(host='0.0.0.0')