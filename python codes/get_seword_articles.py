import urllib2
from bs4 import BeautifulSoup

site= 'https://seword.com/2016/08/'
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def traverseSeword(month, date=None):
    site='https://seword.com/2016'
    hrefs=[];
    hrefs = hrefs + getListArticle(site + '/'+ str(month) +'/')
    if date!= None:
        hrefs = hrefs + getListArticle(site + '/'+ str(month) +'/' + str(date) + '/')
    for i in range(len(hrefs)):
        href = hrefs[i]
        content, datestr =(getDetailedArticleText(href))
        if(len(content) > 0):
            write_article(content, datestr, i)

def getListArticle(site):
    j=1
    ret=[]
    try:
        while(True):
            if(j > 1):
                newSite= site+"page/"+ str(j)
            else:
                newSite= site
            req = urllib2.Request(newSite, headers=hdr)
            f = urllib2.urlopen(req)
            soup = BeautifulSoup(f.read(), 'html.parser')
            j=j+1
            for article in soup.find_all('article'):
                href = article.find('a', {"class":"image-link"})['href']
                if ("politik" in href):
                    ret.append(href)
    except urllib2.HTTPError:
        return ret
    return ret
    print ret[-1]


def getDetailedArticleText(site):
    try:
        req = urllib2.Request(site, headers=hdr)
        f = urllib2.urlopen(req)
        soup = BeautifulSoup(f.read(), 'html.parser')
        content = soup.find('div', {"class": "post-content"})
        datespan = soup.find('span', {"class": "dtreviewed"})
        date = datespan.find('time')['datetime'][:10]
        text = '';
        for p in content.find_all('p'):
            text += ' ' + p.text
        return text.encode('utf-8').strip(), date
    except:
        return "fail", "no date"

def write_article(article, date, ix):
    fname = './seword/' + str(ix+1000) + "-" + date + '.txt'
    with open(fname, "w") as f:
        f.write(article)
        f.close()

traverseSeword(7,1)
