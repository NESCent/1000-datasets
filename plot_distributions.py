#!/usr/bin/env python
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import math
import sys


font = FontProperties()
font.set_size('medium')
font.set_weight('semibold')

distributions = {'all': []}
with open('citation_distribution') as input_file:
    for line in input_file:
        line = line.lstrip()

        # skip blank lines or lines with no dataset id
        if not line: continue
        if not line.split('\t')[1].strip(): continue

        chunks = line.split('\t')[0].split()
        n, repo = chunks[0], ' '.join(chunks[1:])
        if not repo in distributions:
            distributions[repo] = []
        distributions[repo].append(int(n))
        distributions['all'].append(int(n))

del distributions['all']

fig = plt.figure(figsize=(12,6))
for n, key in enumerate(sorted(distributions, key=lambda x:x.upper())):
    # plot a histogram for each repository
    sub = plt.subplot(2,5,n+1)
    
    distributions[key].sort(reverse=True)
    xs = []
    ys = []
    for n, value in enumerate(distributions[key]):
        xs.append(n+1)
        ys.append(value)
    
    bins = np.logspace(0, 8, num=9, base=2)
    plt.ylim(0,80)
    plt.text(0.5, 0.9, key, fontproperties=font,
             horizontalalignment='center',
             verticalalignment='center',
             transform=sub.transAxes)
    # rank-citation plot
    # plt.bar(xs, ys, width=1, log=key=='all')
    # histogram
    plt.hist(ys, bins=bins)
    plt.xscale('log', basex=2)


fig.text(0.5, 0.04, 'citations', ha='center', va='center')
fig.text(0.06, 0.5, 'datasets', ha='center', va='center', rotation='vertical')

try:
    figname = sys.argv[1]
    plt.savefig(figname, dpi=200)
except IndexError:
    plt.show()