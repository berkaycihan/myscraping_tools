import requests
from bs4 import BeautifulSoup

dosya = open("veriler.txt", "w")
sayfa_say= int(input("Çekilecek sayfa sayisi gir: "))


href_list=[]
haberler= []
for i in range(1,sayfa_say+1):
    r = requests.get('https://shiftdelete.net/page/'+str(i))
    soup = BeautifulSoup(r.content,"lxml")
    dt1= soup.find_all("div",attrs={"class":"post-title"})
    for linkler in dt1:
        href_list.append(str(linkler.a.get("href")))
    for j in range(1,len(href_list)-1): 
        try:
            r = requests.get(href_list[j])
            soup = BeautifulSoup(r.content,"lxml")
            dt3 = soup.find_all("div",attrs={"class":"post-content entry-content"})
            dt4 = dt3[0].find_all("p")
            for parag in dt4:
                if(parag.text.startswith("\nSDN Yorumları")):
                    break
                print(parag.text)
                print("\n +1 paragraf çekildi "+"(sayfa no: "+str(i)+")"+"(haber no: "+str(j)+") \n")
                haberler.append(parag.text)
                dosya.write(parag.text)
            dosya.write("\n\n")
        except:
            continue

print("İşlem tamamlandı.("+str(sayfa_say)+"sayfa)")    
dosya.close()
