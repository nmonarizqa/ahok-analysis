import urllib2
from bs4 import BeautifulSoup
import datetime
import regex as re

dt = datetime.datetime(2016, 7, 1)
end = datetime.datetime(2016, 8, 1)
step = datetime.timedelta(days=1)

dateseries = []

while dt < end:
    dateseries.append(dt.strftime('%Y-%m-%d'))
    dt += step

#site= 'http://www.portal-islam.id/search?updated-max=2016-12-19T21%3A54%3A00%2B07%3A00&max-results=100'
#site = "http://www.portal-islam.id/2017/05"
def getListArticle(site):
    ret=[]
    try:
        req = urllib2.Request(site)
        f = urllib2.urlopen(req)
        soup = BeautifulSoup(f.read(), 'html.parser')
        for article in soup.find_all('article'):
            ret.append(list(article.find('h2').children)[1]['href'])
    except urllib2.HTTPError:
        return ret
    return ret

def getDetailedArticleText(site):
    try:
        req = urllib2.Request(site)
        f = urllib2.urlopen(req)
        soup = BeautifulSoup(f.read(), 'html.parser')
        date = soup.find_all("abbr")[0]['title'][:10]
        placeholder = soup.find_all("div", id=lambda x: x and x.startswith('ads'))
        the_text = placeholder[1].text.replace('\n', '').encode('utf8')
        return re.sub(r'[^\x00-\x7f]',r'', the_text), date
    except:
        return "fail", "no date"

def write_article(article, date, ix):
    fname = './piyungan/' + str(ix) + "-" + date + '.txt'
    with open(fname, "w") as f:
        f.write(article)
        f.close()

for i in range(len(all_links)):
    site = all_links[i]
    article, date = getDetailedArticleText(site)
    write_article(article, date, i)
    print '\r',"%",str((i+1)*100./len(all_links))[:4],
