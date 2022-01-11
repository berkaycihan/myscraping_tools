import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime
from tqdm import tqdm    

def relu(x):
    return max(0, x)

zip_codes = ["10006","90013","78714"]
jtime2 = str(datetime.now()) # for naming file daily scraping and saving.
#################################################################
print("\t\t\t\tINDEED.COM SCRAPER\n\tInputs:\n\t\t+page count\n\t\t+radius\n\t\t+zip code\n\tContact:\n\t\tberkaycihan@icloud.com\n\n")
#################################################################

# STEP-1 
#creating a special variable for adding to the url
howmanypage = (int(input("page count: ")))*50

#the loop for preparing links that we will collected urls.
page_links=[]
for zip in zip_codes:
    for limit in range(0,int(relu(howmanypage)),50):
        page_link='https://www.indeed.com/jobs?l='+str(zip)+'&radius=3&limit=50&fromage=3&start='+str(limit) #default r=5
        page_links.append(page_link)
for i in page_links:
    print(i)

#STEP-2
#the loop for collecting urls
url_list=[]
for link in tqdm(page_links,desc='Collecting URLs '):
    #fakeuseragent: Up to date simple useragent faker with real world database. more: https://pypi.org/project/fake-useragent/
    try:
        ua = UserAgent()
        r = requests.get(link, {"User-Agent": ua.random})
        tqdm.write(str(r))
        soup = BeautifulSoup(r.content,"lxml")
        id3 = soup.find_all("div",attrs={"id":"mosaic-provider-jobcards"})
        id4 = id3[0].find_all("a",attrs={"target":"_blank"})
        for i in id4:
            url_list.append("http://www.indeed.com"+str(i.get("href")))
    except:
        pass
    tqdm.write(str(len(url_list))+" URLs were collected until now.")
tqdm.write("---Done.--- "+str(len(url_list))+" URLs were collected.")

#STEP-3
#scraping job pages so getting contents
df = pd.DataFrame() 
df.to_csv(r"indeed_dataset.csv",encoding="utf-8",index=False,mode="w")

for job_page in tqdm(url_list,desc='Scraping '):
    jcomp,jk,jdate,jdesc,jdet,jtit,jloc,jrat,jsal,jtime=" "," "," "," "," "," "," "," "," "," "
    try:
        ua2 = UserAgent()
        r = requests.get(job_page, {"User-Agent": ua2.random})
        soup = BeautifulSoup(r.content,"lxml")
    except:
        pass
    #company
    try:
        id_comp = soup.find_all("div",attrs={"class":"icl-u-lg-mr--sm icl-u-xs-mr--xs"})
        jcomp = str(id_comp[0].a.text)
    except:
        pass
    #jobkey
    try:
        jk = job_page[32:48]
    except:
        pass
    #jobdate
    try:
        id_jdate1 = soup.find("div",attrs={'class':'jobsearch-JobMetadataFooter'})
        jdate = id_jdate1.find_all("div")[1].text
    except:
        pass
    #jobdescription
    try:
        id_jdesc = soup.find_all("div",attrs={'id':'jobDescriptionText'})
        jdesc=""
        for i in id_jdesc:
            jdesc+=i.text
    except:
        pass
    #jobdetails
    try:
        id_jdet = soup.find_all("div",attrs={'class':'jobsearch-JobMetadataHeader-item'})
        jdet1 = id_jdet[0].find('span').text
        if((jdet1.startswith("Fu")) or (jdet1.startswith("Pa")) or (jdet1.startswith("Te"))):
            jdet = jdet1
        else:
            jsal = jdet1
    except:
        pass
    #job_page_url
        #job_page variable provides this.
    #job_title
    try:
        id_jtit = soup.find_all("div",attrs={'class':'jobsearch-JobInfoHeader-title-container'})
        jtit = id_jtit[0].find('h1').text
    except:
        pass
    #joblocation
    try:
        jloc = soup.find_all("div",attrs={'class':'jobsearch-jobLocationHeader-location'})[0].text
    except:
        pass
    #rating
    try:
        id_jrat = soup.find_all("div",attrs={'class':'icl-Ratings icl-Ratings--md icl-Ratings--gold'})
        jrat = id_jrat[0].find('meta').get('content')
    except:
        pass
    #salary
        #this part as same as jobdetails part.
    #scrapetime
    jtime = str(datetime.now())
    #state
        #i couldn't find any content in the job page source about this
    #zipcode
        #i couldn't find any content in the job page source about this
    content_list = [   ["",jcomp,jk,jdate,jdesc,jdet,"",job_page,jtit,jloc,"",jrat,jsal,jtime,"",""]   ] 
    df = df.append(content_list)
    tqdm.write(str(df.shape[0])+" "+"jobs were scraped. "+str(jtime))
print("------completed------"+str(df.shape[0])+" "+"jobs were scraped.\nSaving...")

#STEP-4
#save as csv
df.columns=['benefits','company','jk','job_date','job_description','job_details', 'job_label','job_page_url','job_title','location','qualifications','rating','salary','scrape_time','state','zipcode']
df.to_csv(r"indeed_dataset.csv",encoding="utf-8",index=False,mode="a")
print("Saved.\ncontact:berkaycihan@icloud.com") 
