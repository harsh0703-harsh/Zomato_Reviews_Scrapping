from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo

app=Flask(__name__)
@app.route('/',methods=['GET'])
def homepage():
    return render_template('index.html')
@app.route('/search',methods=['POST'])
def search():
    if request.method=='POST':
        Link=request.form['locations']
        restraunts_links = Link+"/reviews"
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 RuxitSynthetic/1.0 v6392933410 t38550 ath9b965f92 altpub'}
        final_restarauntlink = requests.get(restraunts_links, headers=header)
        final_res_html = bs(final_restarauntlink.text, "html.parser")
        fetch_reviws_page = final_res_html.find_all('div', {"class": "sc-1y3q50z-3 eiMLBn"})
        review_box = fetch_reviws_page[2]
        reviews_box_link = review_box.span.a['href']
        entering_into_reviews = requests.get(reviews_box_link, headers=header)
        soup_reviews = bs(entering_into_reviews.text, "html.parser")
        comment = soup_reviews.find_all('p', {"class": "sc-1hez2tp-0 sc-jdeSqf kGmIUp"})
        print(comment)
        empty_list = []
        for reviews in comment:
            lissts = reviews.text
            mydict = {"Name": "", "Rating": "","Comment": lissts}
            empty_list.append(mydict)

        return render_template("results.html",reviews=empty_list)





if __name__=='__main__':
    app.run(debug=True)