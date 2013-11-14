import cPickle as pkl
import spynner
try:
    with open('data/article_metadata.pkl', 'r') as pkl_file:
        article_data = pkl.load(pkl_file)
except:
    article_data = {}
from scopus_scraper import get_info_from_title, NoMatchException
from pybtex.database.input import bibtex


parser = bibtex.Parser()
bibdata = parser.parse_file('data/all.bib')

try:
    for id in bibdata.entries:
        print '==>', id
        if not id in article_data:
            b = bibdata.entries[id].fields
            try:
                title = b['title'].strip('{}')
                title = title.replace('{', '').replace('}', '')
                if '^' in title: title = title.split('^')[-1]
                article_data[id] = get_info_from_title(title)
            except KeyError: pass
            except NoMatchException:
                print '** NO MATCH FOUND **'
            except Exception as e:
                print '** %s **' % e

    with open('data/article_metadata.pkl', 'w') as pkl_file:
        pkl.dump(article_data, pkl_file)

except:
    with open('data/article_metadata.pkl', 'w') as pkl_file:
        pkl.dump(article_data, pkl_file)
    raise