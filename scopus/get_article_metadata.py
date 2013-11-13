import cPickle as pkl
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
        if not id in article_data:
            b = bibdata.entries[id].fields
            try:
                title = b['title'].strip('{}')
                article_data[id] = get_info_from_title(title)
            except KeyError: pass
            except NoMatchException:
                print '** NO MATCH FOUND **'

    with open('data/article_metadata.pkl', 'w') as pkl_file:
        pkl.dump(article_data, pkl_file)

except Exception as e:
    with open('data/article_metadata.pkl', 'w') as pkl_file:
        pkl.dump(article_data, pkl_file)
    raise