Instructions
============

To generate all figures and analyses, just type `make`. Figures will be saved in 
the "figures" directory, and summaries of analyses in the "results" directory.


Prerequisites
=============

* GNU Make
* Python 2 with the following libraries:
    * numpy
    * matplotlib
    * mpltools
* the vegan R package (available from CRAN)


Figures
=======

![reuse histograms by repository](https://raw.github.com/bendmorris/1000-datasets/master/figures/repo_histograms_reuse.png)

*Histogram showing frequency of datasets with a given number of citations. Red 
bar indicates no citations.*

![top 100 most cited datasets](https://raw.github.com/bendmorris/1000-datasets/master/figures/most_cited_datasets.png)

*The top 100 datasets by number of times reused, and the repositories they come from.*

![citations and reuse](https://raw.github.com/bendmorris/1000-datasets/master/figures/repo_comparison.png)

*A comparison of per-dataset citation and reuse rates between repositories.*

![citations and reuse](https://raw.github.com/bendmorris/1000-datasets/master/figures/reuse_over_time.png)

*Instances of reuse for a dataset. Shows median and 50%/95% confidence intervals.*