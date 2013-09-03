figs=repo_histograms.svg most_cited_datasets.svg
sums=journal_list repo_list dataset_list citation_distribution dataset_counts
figures=figures $(patsubst %, figures/%, $(figs))
summaries=$(patsubst %, data/%, $(sums))

.PHONY: all clean

all: $(figures) $(summaries)

clean:
	rm -f $(figures)
	rm -f $(summaries)
	rm -f figures/*.tsv

%.tsv: %.csv scripts/convert_to_tsv.py scripts/canonical_repo_names.py
	python scripts/convert_to_tsv.py $< | python scripts/canonical_repo_names.py > $@

data/journal_list: data/all.tsv scripts/title_case.py
	cat $< | tail -n +2 | cut -f 21 | python scripts/title_case.py | sort | uniq > $@

data/repo_list: data/all.tsv
	cat $< | tail -n +2 | cut -f 8 | sort | uniq > $@

data/citation_distribution: data/all.tsv
	cat $< | tail -n +2 | cut -f 8,15 | sort | uniq -c > $@

data/dataset_list: data/all_datasets.tsv scripts/process_dataset_list.py
	cat $< | cut -f 2,3 | python scripts/process_dataset_list.py | sort | uniq > $@

data/dataset_counts: data/dataset_list
	cat $< | cut -f 1 | sort | uniq -c > $@

figures:
	mkdir figures

figures/repo_histograms.svg: scripts/plot_distributions.py data/citation_distribution data/dataset_counts
	python $< $@

figures/most_cited_datasets.svg: scripts/most_cited_datasets.py data/citation_distribution
	python $< $@