import BeautifulSoup
import math
from datetime import datetime

def _s_(t):
    return unicode(t).encode('utf-8')

def aver(ratingDist,ratingUsers):
    pts = range(10,0,-1)
    res = 0
    for rt,pt in zip(ratingDist,pts):
        res+=rt*pt
    return res/ratingUsers

def getTitle(bsObj):
    try:
        titleinfo = bsObj.find('div', {'class': 'title_wrapper'})
        return titleinfo.find('h1').contents[0]
    except:
        return ''

def getYear(bsObj):
    try:
        return bsObj.find('span', {'id': 'titleYear'})\
            .find('a').get_text()
    except:
        return ''

def getSubtext(bsObj):
    try:
        return bsObj.find('div', {'class': 'subtext'})
    except:
        return ''

def getMpaa(bsObj,subtext):
    try:
        return subtext.find('meta', {'itemprop': 'datePublished'})['content']
    except:
        return ''

def getDuration(bsObj,subtext):
    try:
        return subtext.find('time')['datetime'][2:-1]
    except:
        return ''

def getGenrelist(subtext):
    genrelist = []
    try:
        genres = subtext.findAll('span', {'itemprop': 'genre'})
        for genre in genres:
            genrelist.append(genre.get_text().strip())
    except:
        genrelist.append('')
    return genrelist

def getDatepublished(subtext):
    try:
        return subtext.find('meta', {'itemprop': 'datePublished'})['content']
    except:
        return ''

def getDirector(bsObj):
    try:
        return bsObj.find('span',{'itemprop':'director'})\
            .find('span',{'itemprop':'name'}).get_text()
    except:
        return ''

def getStars(bsObj):
    stars = []
    try:
        names = bsObj.findAll('span', {'itemprop': 'actors'})
        for name in names:
            stars.append(name.find('span', {'itemprop': 'name'}).get_text())
    except:
        stars.append('')
    return stars

def getMetascore(bsObj):
    try:
        metaInfo = bsObj.find('div', {'class': 'titleReviewBarItem'})
        return metaInfo.find('a').find('div').find('span').get_text()
    except:
        return ''

def getReviews(bsObj):
    try:
        metaInfo = bsObj.find('div', {'class': 'titleReviewBarItem titleReviewbarItemBorder'})
        reviews = metaInfo.find('span', {'class': 'subText'}).findAll('a')[0].get_text()
        critics = metaInfo.find('span', {'class': 'subText'}).findAll('a')[1].get_text()
        return reviews.split()[0],critics.split()[0]
    except:
        return '',''

def getLanguage(bsObj):
    try:
        return bsObj.find('h4', string='Language:').parent.find('a').get_text().strip()
    except:
        return ''

def getBudget(bsObj):
    try:
        return bsObj.find('h4', string='Budget:').parent.contents[2].strip()
    except:
        return ''

def getGross(bsObj):
    try:
        return bsObj.find('h4', string='Gross:').parent.contents[2].strip()
    except:
        return ''

def getProductionco(bsObj):
    try:
        return bsObj.find('h4', string='Production Co:')\
            .parent.find('span',{'itemprop':'creator'})\
            .find('a').get_text().strip()
    except:
        return ''

def getColor(bsObj):
    try:
        return bsObj.find('h4', string='Color:').parent.find('a').get_text().strip()
    except:
        return ''

def getReclist(bsObj):
    reclist = []
    try:
        overviews = bsObj.find('div', {'class': 'rec_overviews'}) \
            .findAll('div', {'class': 'rec_overview'})
        for overview in overviews:
            reclist.append(overview['data-tconst'])
    except:
        reclist.append('')
    return reclist

# --------------------------------------------
# step 2: scraping those films
# --------------------------------------------

def getMovieInfo(link,movielist):

    base_url = "http://www.imdb.com/title/"
    url = base_url + link
    h = requests.get(url)
    bsObj = BeautifulSoup(h.content,'lxml')

    ## title
    title = getTitle(bsObj)
    ## year
    year = getYear(bsObj)

    subtext = getSubtext(bsObj)
    ## mpaa
    mpaa = getMpaa(bsObj,subtext)
    ## duration
    duration = getDuration(bsObj,subtext)
    ## genrelist
    genrelist = getGenrelist(subtext)
    ## datePublished
    datePublished = getDatepublished(subtext)

    ## director
    director = getDirector(bsObj)
    ## stars
    stars = getStars(bsObj)
    ## metaScore
    metaScore = getMetascore(bsObj)
    ## reviews,critics
    reviews,critics = getReviews(bsObj)
    ## reclist
    reclist = getReclist(bsObj)
    ## language
    language = getLanguage(bsObj)

    ## budget
    budget = getBudget(bsObj)
    ## grossUS
    grossUS = getGross(bsObj)
    ## productionCo
    productionCo = getProductionco(bsObj)
    ## color
    color = getColor(bsObj)

    ##

    #----------------- rating distribution
    ratingUrl = url+'/ratings'
    h = requests.get(ratingUrl)
    bsObj = BeautifulSoup(h.content,'lxml')
    p = bsObj.find('a',string='weighted average').parent
    ## total rating user number
    ratingUsers = int(p.get_text().split()[0])
    ## rating value from imdb
    ratingValue = float(p.findAll('a')[-1].get_text())

    ## rating distribution by points
    ratingDist = []
    table = bsObj.findAll('table')
    trs = table[0].findAll('tr')
    for tr in trs[1:]:
        td = tr.findAll('td')[0].get_text().strip()
        ratingDist.append(int(td))
    ## rating average by calculation
    ratingAver = aver(ratingDist,ratingUsers)

    ## rating distribution by user type
    ratingDemoList = ['Males', 'Females', 'Aged under 18', 'Males under 18',
                      'Females under 18', 'Aged 18-29', 'Males Aged 18-29',
                      'Females Aged 18-29', 'Aged 30-44', 'Males Aged 30-44',
                      'Females Aged 30-44', 'Aged 45+', 'Males Aged 45+',
                      'Females Aged 45+', 'IMDb staff', 'Top 1000 voters',
                      'US users', 'Non-US users']
    ratingDemo = []
    trs = table[1].findAll('tr')
    for tr in trs[1:-2]:
        tds = tr.findAll('td')
        dt = []
        for td in tds:
            dt.append(td.get_text().strip())
        dt[0] = str(dt[0])
        dt[1] = int(dt[1])
        dt[2] = float(dt[2])
        ratingDemo.append(dt)

    movieInfo = [title, link, year, mpaa, duration, ','.join(genrelist)
        , datePublished, director, ','.join(stars), metaScore
        , reviews, critics, ','.join(reclist), budget, grossUS,language
        , productionCo, color,ratingUsers, ratingValue
        , ratingAver]
    for rD in ratingDist:
        movieInfo.append(rD)
    rdNum = ['' for _ in range(len(ratingDemoList))]
    rdAver = ['' for _ in range(len(ratingDemoList))]
    for rD in ratingDemo:
        rdNum[ratingDemoList.index(rD[0])] = rD[1]
    movieInfo.extend(rdNum)
    for rD in ratingDemo:
        rdAver[ratingDemoList.index(rD[0])] = rD[2]
    movieInfo.extend(rdAver)
    movielist.append(movieInfo)

from threading import Thread

def main():

    links = []
    base_url = ""
    f = open(base_url+"movieVotes100.tsv", 'r')
    for line in reversed(f.readlines()):
        l = line.strip().split('\t')
        links.append(l[-2])
    f.close()

    tp = 10
    i = 0
    N = math.ceil(len(links)/tp)
    print N
    while i<N:
        print '{}th step started...'.format(i)
        processingFile = open(base_url+'processing.txt', 'a+')
        processingFile.writelines('{}\t{}\t{}\t{}'.format(i, int(N), 'start',datetime.now().time())+'\n')
        movielist = []
        threadlist = []
        if (i+1)*tp<=len(links):
            links_range = links[i*tp:(i+1)*tp]
        else:
            links_range = links[i*tp:]
        for link in links_range:
            t = Thread(target=getMovieInfo,args=(link,movielist,))
            t.start()
            threadlist.append(t)
        for t in threadlist:
            t.join()
        f = open(base_url+'movieInfo/{}.tsv'.format(i),'w+')
        f.writelines('\t'.join([_s_(_) for _ in range(len(movielist[0]))])+'\n')
        for movie in movielist:
            f.writelines('\t'.join([_s_(m) for m in movie])+'\n')
        f.close()
        processingFile.writelines('{}\t{}\t{}\t{}'.format(i, int(N), 'finish',datetime.now().time()) + '\n')
        processingFile.close()
        print '{}th step finished...'.format(i)
        i+=1

if __name__=='__main__':
    main()