#!/usr/bin/env python
import sys
import matplotlib
if len(sys.argv) > 1 and sys.argv[1].endswith('.svg'):
    matplotlib.use('SVG')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import math
from mpltools import style
from mpltools import layout
style.use('ggplot')
from canonical_repo_names import colors


DATASETS = 50

font = FontProperties()
font.set_size('medium')
font.set_weight('semibold')


distribution = []
with open('data/reuse_estimates') as input_file:
    for line in input_file:
        line = line.strip('\r\n ')

        # skip blank lines or lines with no dataset id
        if not line: continue

        repo, id, count = line.split('\t')
        try: count = float(count)
        except ValueError: count = 0

        distribution.append((count, repo))


distribution.sort(reverse=True)
distribution = distribution[:DATASETS]
c = [x for x in colors.keys() if x in [i[1] for i in distribution]]
repo_order = sorted(c, key=lambda x:[i[1] for i in distribution].index(x))
repo_pos = [[x[1] for x in distribution].index(c) for c in repo_order]

fig = plt.figure()
ys = []
cs = []
for i in range(DATASETS):
    n, repo = distribution[i]
    ys.append(n)
    cs.append(colors[repo])

bar = plt.bar(range(DATASETS), ys, color=cs)
plt.xlim(0,DATASETS)
plt.xticks([])

#fig.text(0.5, 0.04, 'rank', ha='center', va='center')
fig.text(0.06, 0.5, '# of citations', ha='center', va='center', rotation='vertical')

plt.legend([bar[x] for x in repo_pos], repo_order)

try:
    figname = sys.argv[1]
    plt.savefig(figname, dpi=200)
except IndexError:
    plt.show()