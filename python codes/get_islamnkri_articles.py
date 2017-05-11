import urllib2
from bs4 import BeautifulSoup
import datetime
import regex as re

list_article = open("list-islamnkri.txt","r")
the_list = list_article.read().split("\n")

def main():
    for i in range(len(the_list)):
        site = the_list[i]
        article, date = getDetailedArticleText(site)
        write_article(article, date, i)
        print '\r',"%",str((i+1)*100./len(the_list))[:4],

def getDetailedArticleText(site):
    try:
        req = urllib2.Request(site)
        f = urllib2.urlopen(req)
        soup = BeautifulSoup(f.read(), 'html.parser')
        date = soup.find("abbr").get("title")[:10]
        text = soup.find("div", {"class":"post-body-inner"}).text
        text = text.replace('\n', '')
        text = text.replace("SPIRITNKRI.COM","")
        text = text.replace("ISLAMNKRI.COM","")
        text = text.replace("islamnkri.com","")
        text = text.replace("spiritnkri.com","")
        return re.sub(r'[^\x00-\x7f]',r'', text).encode('utf8'), date
    except:
        return "fail", "no date"

def write_article(article, date, ix):
    fname = './islamnkri/' + date + "-" + str(ix) +'-islamnkri.txt'
    with open(fname, "w") as f:
        f.write(article)
        f.close()

main()
