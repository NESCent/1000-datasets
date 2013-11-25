import matplotlib.pyplot as plt
import cPickle as pkl
import collections


def main():
    with open('data/article_metadata.pkl') as pkl_file:
        article_data = pkl.load(pkl_file)
    
    citations_per_year = sorted(collections.Counter([max(0, y - int(i['year'])) 
                                                    for i in article_data.values() 
                                                    for y in i['years'] 
                                                    if 'year' in i]).items())
    
    x, y = [[p[n] for p in citations_per_year] for n in (0,1)]
    y = [float(n)/len(article_data) for n in y]
    
    plt.plot(x, y)
    
    plt.figure()
    
    plt.plot(x, [sum(y[:n+1]) for n in range(len(y))])
    
    plt.show()

if __name__ == '__main__': main()