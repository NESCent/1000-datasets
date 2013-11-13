import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from spynner import Browser
from pyquery import PyQuery
import difflib
import re

print '* starting browser...'
browser = Browser()
browser.set_html_parser(PyQuery)

def match_score(a, b):
    return difflib.SequenceMatcher(lambda x: x==' ', a, b).ratio()

def get_info_from_title(title):
    print '[%s]' % title
    data = {}
    
    # navigate to scopus
    print '* navigating to Scopus...'
    browser.load('http://www.scopus.com/')

    # fill in search info
    print '* filling search...'
    browser.wk_fill('input[name="searchterm1"]', title)
    browser.wk_select('select[name="field1"]', 'TITLE')

    print '* submitting...'
    browser.submit('input[value="Search"]')
    
    print 'search results:'

    open('test.html', 'w').write(browser.html)

    # check all results and do fuzzy string comparison to verify which one is
    # the article you're looking for - title must be at least a 90% match
    soup = browser.soup
    results = soup('div#srchResultsList ul.documentListData.docMain')
    titles = results.find('li.dataCol2')
    n = 0
    for result in titles:
        result_title_link = result.find('div')
        result_title_link = result_title_link.find('span')
        result_title_link = result_title_link.find('a')
        result_title_text = result_title_link.text

        score = match_score(title, result_title_text)
        if score < 0.9:
            print n+1, 'bad match: ', result_title_text, '(%s)' % score
            n += 1
            continue

        print n+1, 'good match:', result_title_text, '(%s)' % score
        data['title'] = result_title_text
        break

    if not 'title' in data: raise Exception("Couldn't find a good title match")

    # load the article page on Scopus
    link = result_title_link.get('href')
    print '* visiting article page (%s)...' % link
    link = link.split('&origin')[0] + '&origin=resultslist'
    print link
    browser.load(link)
    soup = browser.soup

    #open('test.html', 'w').write(browser.html)
    
    # get author info
    print '* getting author ids...'
    author_list = soup('p#authorlist')
    author_spans = author_list.find('span')
    author_links = [x.find('a') for x in author_spans if x.find('a') is not None]
    author_urls = [x.get('href') for x in author_links]
    author_ids = [re.findall('authorId=([0-9]+)', x)[0] for x in author_urls]
    data['author_ids'] = author_ids

    # get keyword info
    keyword_blocks = soup('p.marginB5')
    keywords = []
    for block in keyword_blocks:
        itertext = block.itertext()
        for t in itertext:
            if t.endswith(':'):
                keywords.extend([x.strip() for x in itertext.next().split(';')])
                break
    data['keywords'] = keywords
        
    # get citation years
    citation_link = (x.get('href') for x in soup('a') if x.get('href') 
                     and 'citedby.url' in x.get('href')).next()
    print '* loading citations page (%s)...' % citation_link
    browser.load(citation_link)
    # show 200 results per page
    browser.wk_select('select[name="resultsPerPage"]', '200')
    browser.runjs("document.SearchResultsForm.displayPerPageFlag.value='t';nextPageResults();")
    browser.wait_load()

    soup = browser.soup
    date_cols = soup('li.dataCol4')
    years = [int(x.find('div').text) for x in date_cols if x.find('div') is not None]
    data['years'] = years

    return data


if __name__ == '__main__':
    if len(sys.argv) > 1: title = sys.argv[1]
    else: title = 'A genome-wide analysis of the effects of sucrose on gene expression in Arabidopsis seedlings under anoxia.'

    print get_info_from_title(title)