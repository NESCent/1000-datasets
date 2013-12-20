#!/usr/bin/env python
import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import math
from mpltools import style
from mpltools import layout
style.use('ggplot')

if __name__ == '__main__':
    # plot is either reuse, or all citations
    plot_type = sys.argv[1]
    if sys.argv[2].endswith('.svg'):
        matplotlib.use('SVG')
    
    font = FontProperties()
    font.set_size('medium')
    font.set_weight('semibold')
    
    plt.title(plot_type)
    
    distributions = {'ALL': []}
    num_datasets = {'ALL': 0}
    filename = {'reuse': 'data/reuse_estimates',
                'citation': 'data/all_datasets.tsv'}[plot_type]
    with open(filename) as input_file:
        if plot_type == 'citation': input_file.readline()
        
        for line in input_file:
            line = line.strip('\r\n ')
            
            # skip blank lines or lines with no dataset id
            if not line or line.startswith('#'): continue
            
            repo, id, count = line.split('\t')[:3]
            try: count = float(count)
            except: count = 0
            count = int(round(count))
            
            if plot_type == 'citation': count += int(line.split('\t')[3])
            
            if not repo in distributions: distributions[repo] = []
            if not repo in num_datasets: num_datasets[repo] = 0
            
            if count > 0:
                distributions[repo].append(count)
                distributions['ALL'].append(count)
            
            num_datasets[repo] += 1
            num_datasets['ALL'] += 1
    
    
    fig = plt.figure(figsize=(12,8))
    subs = []
    
    column_order=['Journal Archives', 'ALL']
    for n, key in enumerate(sorted(distributions, 
                            key=lambda x:(column_order.index(x) if x in column_order else -1, 
                                          x.upper()))):
        print n, key
        # plot a histogram for each repository
        sub = plt.subplot(3,4,n+1)
        subs.append(sub)
        
        distributions[key].sort(reverse=True)
        data = []
        for value in distributions[key]:
            data.append(value)
        
        zeroes = [0] * (num_datasets[key] - len(data))
        weight = 100./num_datasets[key]
        weights = [weight for x in data]
        zero_weights = [weight for x in zeroes]
        
        bins = [0] + list(np.logspace(0, 10, num=11, base=2))
        plt.ylim(0,100)
        plt.text(0.5, 0.9, key, fontproperties=font,
                 horizontalalignment='center',
                 verticalalignment='center',
                 transform=sub.transAxes)
        plt.text(0.5, 0.8, 'median=%s' % int(np.median(data+zeroes)),
                 horizontalalignment='center',
                 verticalalignment='center',
                 transform=sub.transAxes)
        plt.text(0.5, 0.7, 'mean=%s' % round(np.mean(data+zeroes), 1),
                 horizontalalignment='center',
                 verticalalignment='center',
                 transform=sub.transAxes)
        
        if data:
            plt.hist(data, bins=bins, weights=weights, color='blue')
        if zeroes:
            plt.hist(zeroes, bins=bins, weights=zero_weights, color='red')
        
        plt.xscale('symlog', basex=2)
        sub.set_xticks([x*2 if x > 0 else 1 for x in bins])
        sub.set_xticklabels([int(x) for x in bins],rotation=45, rotation_mode="anchor", ha="right")
        sub.set_xlim(0,bins[-1])
    
    
    fig.text(0.5, 0.04, '%s count' % plot_type, ha='center', va='center')
    fig.text(0.06, 0.5, '% of datasets', ha='center', va='center', rotation='vertical')
    
    for sub in subs:
        sub.minorticks_off()
        layout.cross_spines(ax=sub)
    
    
    try:
        figname = sys.argv[2]
        plt.savefig(figname, dpi=200)
    except IndexError:
        plt.show()
