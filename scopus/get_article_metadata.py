import cPickle as pkl
import spynner
try:
    with open('data/article_metadata.pkl', 'r') as pkl_file:
        article_data = pkl.load(pkl_file)
except:
    article_data = {k:{} for k in {'datasets', 'citations'}}
from scopus_scraper import get_info_from_title, NoMatchException
from pybtex.database.input import bibtex


parser = bibtex.Parser()
bibdata = parser.parse_file('data/all.bib')
data_to_gather = {k:{} for k in ('datasets', 'citations')}

try:
    # get all titles of data publications
    input_file = open('data/titles.tsv')
    for line in input_file:
        line = line.strip()
        if not line: continue
        print line
        vals = line.split('\t')
        repo, accession = vals[:2]
        title = '\t'.join(vals[2:])
        article_info = {'title': title, 'repo': repo, 'accession': accession}
        if not (accession in article_data['datasets']):
            data_to_gather['datasets'][accession] = article_info
    
    # get all titles of their citations
    for id in bibdata.entries:
        print '==>', id
        if not id in article_data:
            b = bibdata.entries[id].fields
            try:
                article_info = {}
                title = b['title'].strip('{}')
                title = title.replace('{', '').replace('}', '')
                if '^' in title: title = title.split('^')[-1]
                article_info['title'] = title
                for key in ('year', 'journal'):
                    if key in b:
                        article_info[key] = b[key]
                data_to_gather['citations'][id] = article_info
            except NoMatchException:
                print '** NO MATCH FOUND **'
            except Exception as e:
                print '** %s **' % e

    # look everything up on Scopus by title
    for key in data_to_gather:
        for id, article_info in data_to_gather[key].items():
            try:
                article_info.update(get_info_from_title(title))
                article_data[key][id] = article_info
            except KeyError: pass

    # pickle the result
    with open('data/article_metadata.pkl', 'w') as pkl_file:
        pkl.dump(article_data, pkl_file)

except:
    # if anything goes wrong, pickle what we've gathered so far and exit
    with open('data/article_metadata.pkl', 'w') as pkl_file:
        pkl.dump(article_data, pkl_file)
    raise