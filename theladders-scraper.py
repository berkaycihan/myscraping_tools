import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime
from tqdm import tqdm  

zip_codes = ["10006","90013","78714"]
jtime2 = str(datetime.now()) # for naming file daily scraping and saving.
#################################################################
print("\t\t\t\tTHELADDERS.COM SCRAPER\n\tInputs:\n\t\t+page count\n\t\t+radius\n\t\t+zip code\n\t\t+BrowserDriverPath\n\tContact:\n\t\tberkaycihan@icloud.com\n\n")
#################################################################


# STEP-1
#the loop for preparing links that we will collected urls.
howmanypage = int(input("page count: "))
page_links=[]
for zip in zip_codes:
    for page in range(howmanypage):
        page_link='https://www.theladders.com/jobs/searchresults-jobs?location='+str(zip)+'&order=PUBLICATION_DATE&daysPublished=7&distance=3&page='+str(page)  #default r=8
        page_links.append(page_link)
for i in page_links:
    print(i)

#STEP-2
#the loop for collecting urls
url_list=[]
driver_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe' # CHANGE WITH YOUR CHROME DRIVER PATH
browser=webdriver.Chrome(driver_path)
for link in tqdm(page_links,desc='Collecting URLs '):
    #fakeuseragent: Up to date simple useragent faker with real world database. more: https://pypi.org/project/fake-useragent/
    try:
        browser.get(link)
        for i in (browser.find_elements_by_class_name('job-card-title')):
            print(i.get_attribute("href"))
            url_list.append(i.get_attribute("href"))
    except:
        pass
    tqdm.write(str(len(url_list))+" URLs were collected until now.")
tqdm.write("---Done.--- "+str(len(url_list))+" URLs were collected.")
browser.close()

#STEP-3
#scraping job pages so getting contents
df = pd.DataFrame() 
df.to_csv(r"theladders_dataset.csv",encoding="utf-8",index=False,mode="w")

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
        id_comp = soup.find_all("div",attrs={"class":"job-view-header-details-inner"})
        id_comp = id_comp[0].find("span",attrs={'class':'job-view-header-details'})
        for i in id_comp:
            jcomp = i.text
            break
    except:
        pass
    #jobkey
    try:
        jk = job_page[int(len(job_page))-8::]
    except:
        pass
    #jobdate
    try:
        jdate = soup.find("div",attrs={"class":"header-data-posted-days"}).text
    except:
        pass
    #jobdescription
    try:
        id_jdesc = soup.find_all("section",attrs={"class":"job-description-section"})
        jdesc=""
        for i in id_jdesc:
            jdesc += i.text
    except:
        pass
    #jobdetails
    try:
        jdet = soup.find_all("div",attrs={"class":"job-view-detail-value"})[1].text
    except:
        pass    
    #job_page_url
        #job_page variable provides this
    #job_title
    try:
        jtit = soup.find_all("h1",attrs={"class":"job-view-title"})[0].text
    except:
        pass
    #job_location
        #we can use company variables for this content
    try:
        for i in id_comp:
            jloc = i.text
    except:
        pass
    #rating
        #i couldn't find any content in the job page source about this
    #salary
        #there are compensation values in page sources.
    #scrapetime
    jtime = str(datetime.now())
    #state
        #i couldn't find or create any content in the job page source about this.
    #zipcode
        #i couldn't find or create content any in the job page source about this.

    content_list = [   ["",jcomp,jk,jdate,jdesc,jdet,"",job_page,jtit,jloc,"",jrat,jsal,jtime,"",""]   ] 
    df = df.append(content_list)
    tqdm.write(str(df.shape[0])+" "+"jobs were scraped. "+str(jtime))
print("------completed------"+str(df.shape[0])+" "+"jobs were scraped.\nSaving...")

#STEP-4
#save as csv
df.columns=['benefits','company','jk','job_date','job_description','job_details', 'job_label','job_page_url','job_title','location','qualifications','rating','salary','scrape_time','state','zipcode']

df.to_csv(r"theladders_dataset.csv",encoding="utf-8",index=False,mode="a")
print("Saved.\ncontact:berkaycihan@icloud.com") 
