def main():
    import sys
    import matplotlib
    try:
        if sys.argv[1].endswith('.svg'):
            matplotlib.use('SVG')
    except IndexError: pass
    import cPickle as pkl
    import matplotlib.pyplot as plt
    import numpy as np
    from mpltools import style
    from mpltools import layout
    style.use('ggplot')

    with open('data/article_metadata.pkl') as data_file:
        data = pkl.load(data_file)

    data = data['datasets']

    citations = []

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
        citations.append((repo, years))

    vals = {}
    for i in range(8+1):
        vals[i] = []
        for repo, y in citations:
            val = len([x for x in y if x <= i]) * reuse_rates[repo]
            vals[i].append(val)

    k = sorted(vals.keys())
    # show the median and 95%, 50% CIs
    for p in [2.5, 25, 50, 75, 97.5]:
        y = [np.percentile(vals[i], p) for i in k]
        plt.plot(k, y, 'b-' if p==50 else 'b--')
    plt.xlabel('Years since publication')
    plt.ylabel('Instances of dataset reuse')

    try:
        figname = sys.argv[1]
        plt.savefig(figname, dpi=200)
    except IndexError:
        plt.show()
        
        
if __name__ == '__main__':
    main()
