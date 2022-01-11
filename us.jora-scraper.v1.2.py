import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime
from tqdm import tqdm   

zip_codes = ["10006","90013","78714"]
jtime2 = str(datetime.now()) # for naming file daily scraping and saving.
#################################################################
print("\t\t\t\tUS.JORA.COM SCRAPER\n\tInputs:\n\t\t+page count\n\t\t+radius\n\t\t+zip code\n\tContact:\n\t\tberkaycihan@icloud.com\n\n")
#################################################################


# STEP-1
#the loop for preparing links that we will collected urls. 
howmanypage = int(input("page count: "))

page_links=[]
for zip in zip_codes:
    for page in range(howmanypage):
        page_link='http://us.jora.com/j?a=7&l='+str(zip)+'&p='+str(page)+'&q=&r=3&since=lv&sp=facet_since_last_visit&st=date&surl=0&'  #default r=5
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

        id3 = soup.find_all("div",attrs={"id":"jobresults"})
        #id4 = id3[0].find_all("article",attrs={'class':'job-card result organic-job'})
        id4 = id3[0].find_all("a",attrs={'class':'job-link'})
        for i in id4:
            url_list.append("http://us.jora.com"+str(i.get("href")))
    except:
        pass
    tqdm.write(str(len(url_list))+" URLs were collected until now.")
tqdm.write("---Done.--- "+str(len(url_list))+" URLs were collected.")


#STEP-3
#scraping job pages so getting contents
df = pd.DataFrame() 
df.to_csv(r"us.jora_dataset.csv",encoding="utf-8",index=False,mode="w")

for job_page in tqdm(url_list,desc='Scraping '):
    jcomp,jk,jdate,jdesc,jdet,jtit,jloc,jstate,jtime=" "," "," "," "," "," "," "," "," "
    try:
        ua2 = UserAgent()
        r = requests.get(job_page, {"User-Agent": ua2.random})
        soup = BeautifulSoup(r.content,"lxml")
    except:
        pass
    #company
    try:
        id_comp = soup.find("div",attrs={"id":"company-location-container"})
        for i in id_comp:
            jcomp=i.text
            break
    except:
        pass
    #jobkey
    try:
        id_jobkey = soup.find("div",attrs={"class":"job-view-content grid-content"})
        jk = id_jobkey.get("job-id")[2:]
    except:
        pass
        #alternative way to find jk
            #id_jobkey = soup.find_all("span",attrs={"class":"branded-links"})
            #for i in id_jobkey:
                #if i.a.get("href").startswith("/support/enquiries/n"):
                    #jk = str(i.a.get("href")[115:147]) 
    #jobdate
        #id_jobdate = soup.find_all("div",attrs={"class":"heading-xsmall"})
    try:
        id_jobdate = soup.find("span",attrs={"class":"listed-date"})
        jdate = id_jobdate.text
    except:
        pass
    #jobdescription
    try:
        id_jobdesc = soup.find_all("div",attrs={"id":"job-description-container"})
        jdesc=""
        for i in id_jobdesc:
            jdesc+=i.text      
    except:
        pass
    #jobdetails
    try:
        id_jdet = soup.find_all("div",attrs={"id":"job-info-container"})
        jdet = id_jdet[0].find("div",attrs={"class":"content"}).text                
    except:
        pass
    #job_page_url
        #job_page variable provides this
    #job_title
    try:
        id_jtit = soup.find("h3",attrs={"class":"job-title heading-xxlarge"})
        jtit = id_jtit.text
    except:
        pass
    #job_location
    try:
        jloc = soup.find_all("div",attrs={"id":"company-location-container"})[0].text
        #jloc = id_jloc[0].find("a",attrs={"class":"location -link-muted"}).text
    except:
        pass
    #rating
        #i couldn't find any content in the job page source about this
    #salary
        #i couldn't find any content in the job page source about this
    #scrapetime
    jtime = str(datetime.now())
    #state
    try:
        jstate = jloc.split(',')[::-1][0]
    except:
        pass
    #zipcode
        #i couldn't find any content in the job page source about this
                
    content_list = [   ["",jcomp,jk,jdate,jdesc,jdet,"",job_page,jtit,jloc,"","","",jtime,jstate,""]   ] 
    df = df.append(content_list)
    tqdm.write(str(df.shape[0])+" "+"jobs were scraped. "+str(jtime))
print("------completed------"+str(df.shape[0])+" "+"jobs were scraped.\nSaving...")

#STEP-4
#save as csv
df.columns=['benefits','company','jk','job_date','job_description','job_details', 'job_label','job_page_url','job_title','location','qualifications','rating','salary','scrape_time','state','zipcode']
df.to_csv(r"us.jora_dataset.csv",encoding="utf-8",index=False,mode="a")
print("Saved.\ncontact:berkaycihan@icloud.com") 
