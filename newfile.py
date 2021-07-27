from flask import Flask
import urllib
import requests
from bs4 import BeautifulSoup
import re
import os
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
@app.route("/product")

def get_product():
    product = request.args["product"]
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
    for title in titles:
        product_title= title.select_one('a > dl > dd > div >div.name').text
        product_price= title.select_one('a > dl > dd > div > div > div > div > em >strong.price-value').text
        product_title= re.sub('\n','', product_title)
        product_price= re.sub('\n','', product_price)
        product_title= product_title.lstrip()
        product_price= product_price.lstrip()
        ImgUrl0=a[number].replace("//","https://")
        ImgUrl.append(ImgUrl0)
        urllib.request.urlretrieve(ImgUrl[number], f"imgs/"+'['+ str(number+1) + '] '+ str(product_title)+".jpg" )
        print('['+ str(number+1) + ']', product_title, product_price+'원')
        print(ImgUrl[number])
        number= number+ 1
        if number==8:
            break
if __name__ == "__main__":
    app.run()