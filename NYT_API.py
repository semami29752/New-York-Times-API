import requests
import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
import time

def query_site(page=0):
    days_to_go_back = -1
    delta = datetime.timedelta(days_to_go_back)
    begin_date = datetime.datetime.today() + delta

    api_key = "#######"
    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    params = {"api-key": api_key,
    'q': 'iran','begin_date' : begin_date.strftime('%Y%m%d'), 'page': page}
    r = requests.get(url, params = params)
    if r.status_code == 200:
        data = r.json()
        articles = data['response']
        return articles
    else:
        return dict()

content = ""

try:
    page_no = (query_site()['meta']['hits']/10)+1  #return the number of pages of returned data
except KeyError:
    content = 'The query was not executed properly. No response received!'
    page_no = 0

article_no = 1

try:
    for page in range(page_no):
        articles = query_site(page)
        time.sleep(7) #Pause for 7 seconds to respect the API usage limit (10 per min)
        for article in articles['docs']:
            if 'Iran' in article['abstract']:
                content +=  "Article {}".format(article_no)+"\n"
                content += ">TITLE: "
                content += (article['headline']['main']+"\n")
                content += (">ABSTRACT: ")
                content += (article['abstract']+"\n")
                content += (">FIRST PARAGRAPH: ")
                content += (article['lead_paragraph']+"\n")
                content += (">SOURCE: ")
                content += (article['source']+"\n")
                content += (">URL: ")
                content += (article['web_url']+"\n\n")
                article_no +=1
except KeyError:
    content = 'The query was not executed properly. No response received!'

#Check to see if any Iran related article were found
if content:
    content = content.encode('utf-8') #Convert Unicode content to ascii
else:
    content = "No articles related to Iran found!"

#Define Login info
from_email = '######@gmail.com'
password = '###########'

#Define Email attributes
msg = MIMEMultipart()
msg["Subject"] = "NYTimes Article " + str(datetime.datetime.today().strftime('%m-%d'))
msg["From"] = "Samin Emami   ######@gmail.com"
msg["To"] = "########@gmail.com"
#msg["Cc"] = ""
body = MIMEText(content)
msg.attach(body)

#Establish connection to server and send the email
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls() #encryption
smtp.ehlo()
smtp.login(from_email, password)
smtp.sendmail(msg["From"], msg["To"], msg.as_string())
smtp.quit()
