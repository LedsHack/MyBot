import requests
from bs4 import BeautifulSoup

class Get:    
    def Update(self):
        r = requests.get("https://www.kfc-ukraine.com/promo/")
        if(r.status_code == 200): 
            r.encoding = 'utf-8'
            #file = open('parse/index.html', 'w')
            #file.write(r.text)
            #file.close
            return([True, r.text])
        else:
            return([False, "Ошибка запроса KFC: " + str(r.status_code)])

        
    def GetInfo(self, data):
        soup = BeautifulSoup(data, "html.parser")
        end_promo = soup.find('div', {'class': 'main-content-inr group'}).find('li', {'class': 'content-list-item'})
        img = end_promo.find('img').get('src')
        txt = end_promo.find('p').text
        return([img, txt.split('\n')[0]])
        
        
def goPromo():
    ex = Get()
    data = ex.Update()
    if(data[0]):
        return([True, ex.GetInfo(data[1])])
    else:
        return([False, data[1]])
    


#print(goPromo())
