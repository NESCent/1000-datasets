#!/usr/bin/env python
if __name__ == '__main__':
    import sys
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    import numpy as np
    import math
    from mpltools import style
    from mpltools import layout
    style.use('ggplot')
    from collections import defaultdict
    import matplotlib
    if len(sys.argv) > 1 and sys.argv[1].endswith('.svg'):
        matplotlib.use('SVG')
    
    # get the reuse rate for each repo, per dataset
    reuses = defaultdict(lambda: 0.0)
    totals = defaultdict(lambda: 0)
    with open('data/reuse_estimates') as input_file:
        for line in input_file:
            line = line.strip()
            if not line or line.startswith('#'): continue
            
            repo, id, n = line.split('\t')[:3]
            n = float(n)
            
            reuses[repo] += n
            totals[repo] += 1
            
    reuse_rate = {key: reuses[key] / totals[key] for key in reuses}
    
    # get the total number of citations per dataset
    citations = defaultdict(lambda: 0.0)
    totals = defaultdict(lambda: 0)
    with open('data/all_datasets.tsv') as input_file:
        input_file.readline()
        
        for line in input_file:
            line = line.strip()
            if not line or line.startswith('#'): continue
            
            repo, id, n1, n2 = line.split('\t')[:4]
            n = float(n1) + float(n2)
            
            citations[repo] += n
            totals[repo] += 1
            
    citation_rate = {key: citations[key] / totals[key] for key in citations}
    
    xs = np.log10([reuse_rate[key] for key in reuses])
    ys = np.log10([citation_rate[key] for key in reuses])
    labels = reuses.keys()
    
    plt.xlabel('Instances of reuse per dataset')
    plt.ylabel('Citations per data paper')
    
    plt.xlim(-2,1)
    
    axes = plt.gca()
    xticks = axes.get_xticks()
    xticks = range(int(xticks[0]), int(xticks[-1])+1, 1)
    axes.set_xticks(xticks)
    axes.set_xticklabels([10**x for x in xticks])
    yticks = axes.get_yticks()
    axes.set_yticklabels([round(10**y, 1) for y in yticks])
    
    plt.scatter(xs, ys)
    for (x, y, label) in zip(xs, ys, labels):
        plt.annotate(
            label, 
            xy = (x, y), xytext = (0,-5),
            textcoords = 'offset points', ha = 'right', va = 'top',
            bbox = dict(boxstyle = 'round,pad=0.4', fc = 'grey', alpha = 0.5),
            )
    
    try:
        figname = sys.argv[1]
        plt.savefig(figname, dpi=200)
    except IndexError:
        plt.show()
