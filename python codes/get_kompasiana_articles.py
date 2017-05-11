import numpy as np
from bs4 import BeautifulSoup
import urllib2
import dateparser
import matplotlib.pyplot as plt
%pylab inline

kompasiana = open("../kompasiana/31jul.txt",'r').read()

dates = []
links = []
for c in cf:
    the_children = list(c.children)[1]
    the_link = list(list(the_children)[1])[0]['href']
    the_date = list(the_children)[3].find('span').text
    links.append(the_link)
    dates.append(the_date)

selected_dates = dates[5234:]
selected_links = links[5234:]
selected_dates=[dateparser.parse(x) for x in selected_dates]
date_str = [x.strftime('%Y-%m-%d') for x in selected_dates]

def main():
    for i in range(len(selected_links)):
        if i >= 1529:
            site=selected_links[i]
            ar = getDetailedArticleText(site)
            fname = "./kompasiana/" + str(i) + "-" + date_str[i] + '.txt'
            write_article(ar, fname)

def getDetailedArticleText(site):
    try:
        req = urllib2.Request(site)
        f = urllib2.urlopen(req)
        soup = BeautifulSoup(f.read(), 'html.parser')
        content = soup.find('article')
        text = '';
        for p in content.find_all('p'):
            text += ' ' + p.text
        text = text.encode('utf-8').strip()
        return text
    except:
        return "fail"

def write_article(ar, fname):
    with open(fname, "w") as f:
        f.write(ar)
        f.close()

main()
