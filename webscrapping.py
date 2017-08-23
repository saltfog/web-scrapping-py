import urllib
from bs4 import BeautifulSoup
html = urllib.urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsObj = BeautifulSoup(html)

nameList = bsObj.findAll("span", {"class":"green"})
for name in nameList:
 print(name.get_text())