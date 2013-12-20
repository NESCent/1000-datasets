import sys
import matplotlib
import cPickle as pkl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from mpltools import style
from mpltools import layout
style.use('ggplot')
from collections import defaultdict


def main():
    try:
        if sys.argv[1].endswith('.svg'):
            matplotlib.use('SVG')
    except IndexError: pass
    
    font = FontProperties()
    font.set_size('medium')
    font.set_weight('semibold')
    
    with open('data/article_metadata.pkl') as data_file:
        data = pkl.load(data_file)
    
    data = data['datasets']
    
    citations = defaultdict(lambda: [])
    
    reuse_rates = {}
    with open('data/reuse_estimates') as data_file:
        for line in data_file:
            if line.startswith('#'):
                repo = line.split('[')[0][1:].strip()
                l = '[' + line.split('[')[1]
                l = eval(l)
                # average wos/gs reuse rates
                rate = (l[0][2] + l[1][2])/2
                reuse_rates[repo] = rate

    for (k,v) in data.items():
        repo = v['repo']
        years = v['years']
        years = [y - min(years) for y in years]
        citations[repo].append(years)
    
    vals = defaultdict(lambda: {})
    for repo in citations:
        v = vals[repo]
        for i in range(5+1):
            v[i] = []
            for y in citations[repo]:
                val = len([x for x in y if x <= i]) * reuse_rates[repo]
                v[i].append(val)
    
    fig = plt.figure(figsize=(12,8))
    subs = []
    
    for (n, (repo, v)) in enumerate(sorted(vals.items())):
        sub = plt.subplot(2,4,n+1)
        subs.append(sub)
        
        plt.ylim(0,25)
        plt.text(0.5, 0.9, repo, fontproperties=font,
                 horizontalalignment='center',
                 verticalalignment='center',
                 transform=sub.transAxes)
        
        k = sorted(v.keys())
        # show the median and 95%, 50% CIs
        for p in [2.5, 25, 50, 75, 97.5]:
            y = [np.percentile(v[i], p) for i in k]
            plt.plot(k, y, 'b-' if p==50 else 'b--')
    
    for sub in subs:
        sub.minorticks_off()
        layout.cross_spines(ax=sub)
    
    fig.text(0.5, 0.04, 'Years since publication', ha='center', va='center')
    fig.text(0.06, 0.5, 'Instances of reuse', ha='center', va='center', rotation='vertical')
    
    try:
        figname = sys.argv[1]
        plt.savefig(figname, dpi=200)
    except IndexError:
        plt.show()
        
        
if __name__ == '__main__':
    main()
