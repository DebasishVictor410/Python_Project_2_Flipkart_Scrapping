from flask import Flask
import requests
from flask import render_template
from bs4 import BeautifulSoup as bs
from flask import request
from urllib.request import urlopen
from flask_cors import cross_origin

flask_obj=Flask(__name__,template_folder="htmls",static_folder="css")

@flask_obj.route("/",methods=["GET"])
@cross_origin()
def home_page():
    return render_template("index.html")

@flask_obj.route("/review",methods=["POST","GET"])
@cross_origin()
def scrapping():
    if request.method=="POST":
        try:
            link="https://www.flipkart.com/search?q="
            search_item=request.form["content"].replace(" ","")
            link_search_item=link+search_item
            url_link_open=urlopen(link_search_item)
            url_link_open_read=url_link_open.read()
            url_link_open.close()
            url_link_open_html=bs(url_link_open_read,"html.parser")
            url_link_open_html_boxes=url_link_open_html.findAll("div",{"class":"_2kHMtA"})

            box_link1="https://www.flipkart.com"+url_link_open_html_boxes[0].a['href']
            box_link1_pro_req=requests.get(box_link1)
            box_link1_pro_req.encoding="utf-8"
            box_link1_pro_req_html=bs(box_link1_pro_req.text,"html.parser")

            prod_ratings=box_link1_pro_req_html.find('div',{'class':'_2d4LTz'}).text

            reviews=[]

            for i in url_link_open_html_boxes:
            
                box_link="https://www.flipkart.com"+i.a['href']
                box_link_pro_req=requests.get(box_link)
                box_link_pro_req.encoding="utf-8"
                box_link_pro_req_html=bs(box_link_pro_req.text,"html.parser")

                prod_name=box_link_pro_req_html.find('span',{'class':'B_NuCI'}).text
                prod_name=prod_name.replace("\xa0\xa0"," ")
                
                reviews_section=box_link_pro_req_html.find_all('div',{'class':'_16PBlm'})

                for i in reviews_section:
                    try:
                        each_review_title=i.find_all('p',{'class':'_2-N8zT'})[0].text
                        each_user_name=i.find('p',{'class':'_2sc7ZR _2V5EHH'}).text
                        each_rating=i.find_all('div',{'class':'_3LWZlK _1BLPMq'})[0].text
                        each_user_message=i.find('div',{'class':""}).text
                        
                        mydict = {"Product": search_item,"Overall_Rating":prod_ratings, "Name": each_user_name, "Rating": each_rating, "ReviewTitle":each_review_title ,"Comments": each_user_message}

                        reviews.append(mydict)
                    except Exception as e:
                        pass
            return render_template("review.html",reviews=reviews[0:(len(reviews)-1)])
        
        except Exception as e:
            print()
            print("I am outer exception",e)
            pass
    else:
        return render_template('index.html')

            



if __name__=="__main__":
    flask_obj.run(host="0.0.0.0")