from collections import Counter
import sys


KEYWORD_MIN_FREQ = 2

def main():
    import cPickle as pkl
    with open('data/article_metadata.pkl') as data_file:
        data = pkl.load(data_file)

    all_keywords = Counter([k.lower() 
                            for article_type in data.keys()
                            for i in data[article_type].values() 
                            for k in i['keywords']
                            ])
    # remove keywords that show up less than KEYWORD_MIN_FREQ times
    all_keywords = set([k for (k,v) in all_keywords.items() if v >= KEYWORD_MIN_FREQ])
    all_keywords = sorted(list(all_keywords))
    sys.stderr.write('Keywords: ' + str(len(all_keywords))+'\n')
    sys.stderr.flush()
                        
    print '\t'.join(['article_type', 'repo'] + all_keywords)

    n = 0
    for article_type in data.keys():
        for s in data[article_type].values():
            try: repo = s['repo']
            except KeyError: repo = 'na'
            k = set([i.lower() for i in s['keywords']])
            kl = ['1' if i in k else '0' for i in all_keywords]
            if not all([i=='0' for i in kl]):
                n += 1
                print '\t'.join([article_type, repo] + kl)

    sys.stderr.write('Datasets: %s\n' % (n))
    sys.stderr.flush()
            
if __name__ == "__main__":
    main()
