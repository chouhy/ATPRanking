from urllib.request import Request,urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation
import time

class ATPRanking():
    
    def __init__(self):
        self.rankRange = '1-10'
        self.index = 0
        self.url = 'https://www.atpworldtour.com/en/rankings/singles?'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        self.rankDate = self.updateDateList()
        #https://www.atpworldtour.com/en/rankings/singles?rankDate=2016-09-12&rankRange=1-10
    
    def getTable(self,date=''):
        self.curDate = date
        req = Request(self.url+'rankRange='+self.rankRange+'&rankDate='+date,headers=self.headers)
        html = urlopen(req).read()
        soup = bs(html,'html.parser')
        tableStruct = soup.find('table')
        th = tableStruct.find_all('th')
        heads = []
        for i in th:
            heads.append(i.find('div',class_='sorting-label').string.strip())
        #self.heads = heads
        tr = tableStruct.find('tbody').find_all('tr')
        
        table = []
        #table.append(heads)
        for things in tr:
            td = things.find_all('td')   
            content = []
            for i in td: 
                content.append(i.get_text().strip())
            table.append(content)
        #self.table = table
        self.tableFrame = pd.DataFrame(table,columns=heads)
        self.tableFrame = self.tableFrame[['Ranking','Player','Age','Points']]
        

    def next(self):
        #
        self.index +=1

    def updateDateList(self):

        req = Request(self.url,headers=self.headers)
        html = urlopen(req).read()
        #print(html)
        soup = bs(html,'html.parser')
        rankDate = soup.find(attrs={'data-value':'rankDate'})
        dateList = rankDate.find_all('li')
        date = []
        for i in dateList:
            week = i.get('data-value')
            if not week:
                continue
            date.append(week)
        return date[::-1]
    def open_file(self,mode="a"):
        self.f = open('ATPRankingHistory',mode)
    def close_file(self):
        self.f.close()

    def to_csv(self):
        self.open_file()
        if len(self.tableFrame) == 10:
            self.f.write(self.curDate+',')
        
            for i in range(10):
                ls = list(self.tableFrame.iloc[i])
                text = '+'.join(ls)
                text = text.replace(',','')
                self.f.write(text)
                if not i == 9:
                    self.f.write(',')
                else:
                    self.f.write('\n')
        else:
            pass
        self.close_file()
        
    def auto_save(self,start,num):
        
        for i in range(num):
            self.getTable(self.rankDate[start+i])
            self.to_csv()
            time.sleep(2)
        

def main():
    #print(weeks)
    rk = ATPRanking()
    #rk.getTable()
    rk.getTable(rk.rankDate[1350])
    print(rk.curDate)
    print(rk.tableFrame)
    
if __name__ == '__main__':
    main()
