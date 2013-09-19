figs=repo_histograms_reuse repo_histograms_citation most_cited_datasets
sums=journal_list repo_list dataset_list citation_distribution dataset_counts reuse_estimates
fig_format=svg
figures=figures $(patsubst %, figures/%.$(fig_format), $(figs))
summaries=$(patsubst %, data/%, $(sums))

.PHONY: all clean

all: $(figures)

clean:
	rm -rf figures
	rm -f $(summaries)
	rm -f figures/*.tsv

%.tsv: %.csv scripts/convert_to_tsv.py scripts/canonical_repo_names.py
	python scripts/convert_to_tsv.py $< | python scripts/canonical_repo_names.py > $@

data/journal_list: data/all.tsv scripts/title_case.py
	cat $< | tail -n +2 | cut -f 21 | python scripts/title_case.py | sort | uniq > $@

data/repo_list: data/all.tsv
	cat $< | tail -n +2 | cut -f 8 | sort | uniq > $@

data/citation_distribution: data/all_datasets.tsv scripts/process_dataset_list.py
	cat $< | cut -f 2,3,4 | python scripts/process_dataset_list.py > $@

data/reuse_subsample: data/all.tsv
	cat $< | tail -n +2 | cut -f 3,4,8 | sort | uniq -c > $@

data/dataset_list: data/all_datasets.tsv scripts/process_dataset_list.py
	cat $< | cut -f 2,3 | python scripts/process_dataset_list.py | sort | uniq > $@

data/dataset_counts: data/dataset_list
	cat $< | cut -f 1 | sort | uniq -c > $@

data/reuse_estimates: scripts/weighted_citations.py data/citation_distribution data/reuse_subsample
	python $^ > $@

figures:
	mkdir figures

figures/repo_histograms_reuse.svg: scripts/plot_distributions.py data/reuse_estimates data/dataset_counts
	python $< data/reuse_estimates $@

figures/repo_histograms_citation.svg: scripts/plot_distributions.py data/citation_distribution data/dataset_counts
	python $< data/citation_distribution $@

figures/most_cited_datasets.svg: scripts/most_cited_datasets.py data/reuse_estimates
	python $< $@
