figs=repo_histograms_reuse repo_histograms_citation most_cited_datasets
sums=journal_list repo_list dataset_list citation_distribution dataset_counts reuse_estimates repo_citation_counts repo_dataset_counts repo_reuse_counts
fig_format=svg
figures=figures $(patsubst %, figures/%.$(fig_format), $(figs))
summaries=$(patsubst %, data/%, $(sums))

.PHONY: all clean tests figures
.SECONDARY: %.tsv

# by default, run all tests, then generate all figures
all: sums tests figs

# just generate the figures (create the figures directory first)
figs: figures $(figures)
sums: $(summaries)

# delete all intermediate files and products
clean:
	rm -rf figures
	rm -f $(summaries)
	#rm -f figures/*.tsv

# run all unit tests - will fail and give summary if any tests fail
tests: $(wildcard scripts/*.py Makefile)
	python run_tests.py

#all_datasets.tsv: %.tsv: %.csv scripts/convert_to_tsv.py scripts/canonical_repo_names.py
#	python scripts/convert_to_tsv.py $< | python scripts/canonical_repo_names.py > $@

data/journal_list: data/all.tsv scripts/title_case.py
	cat $< | tail -n +2 | cut -f 21 | python scripts/title_case.py | sort | uniq > $@

data/repo_list: data/all.tsv
	cat $< | tail -n +2 | cut -f 8 | sort | uniq > $@

data/citation_distribution: data/all_datasets.tsv scripts/process_dataset_list.py
	cat $< | cut -f 2,3,4 | python scripts/process_dataset_list.py > $@

data/reuse_subsample: data/all.tsv
	cat $< | tail -n +2 | grep -v "not valid" | cut -f 3,4,8 | sort | uniq -c > $@

data/dataset_list: data/all_datasets.tsv scripts/process_dataset_list.py
	cat $< | cut -f 2,3 | python scripts/process_dataset_list.py | sort | uniq > $@

data/dataset_counts: data/dataset_list
	cat $< | cut -f 1 | sort | uniq -c > $@

data/reuse_estimates: scripts/weighted_citations.py data/citation_distribution data/reuse_subsample
	python $^ > $@

data/repo_citation_counts: scripts/repo_citation_counts.py data/all_datasets.tsv
	python $< > $@

data/repo_dataset_counts: scripts/repo_dataset_counts.py data/all_datasets.tsv
	python $< > $@

data/repo_reuse_counts: scripts/repo_reuse_counts.py data/reuse_subsample
	python $< > $@

figures:
	mkdir -p figures

figures/repo_histograms_reuse.svg: scripts/plot_distributions.py data/reuse_estimates data/dataset_counts
	python $< data/reuse_estimates $@

figures/repo_histograms_citation.svg: scripts/plot_distributions.py data/citation_distribution data/dataset_counts
	python $< data/citation_distribution $@

figures/most_cited_datasets.svg: scripts/most_cited_datasets.py data/reuse_estimates
	python $< $@
