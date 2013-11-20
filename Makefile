figs=repo_histograms_reuse repo_histograms_citation most_cited_datasets repo_comparison
sums=journal_list repo_list dataset_list dataset_counts reuse_estimates repo_citation_counts repo_dataset_counts repo_reuse_counts
fig_format=png
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

data/all_datasets.tsv: scripts/all_datasets.py
	python $< > $@

data/journal_list: data/all.tsv scripts/title_case.py
	cat $< | tail -n +2 | cut -f 21 | python scripts/title_case.py | sort | uniq > $@

data/repo_list: data/all.tsv
	cat $< | tail -n +2 | cut -f 8 | sort | uniq > $@

data/reuse_subsample_%: data/all.tsv
	cat $< | tail -n +2 | grep -v "not valid" | grep -i $* | cut -f 3,4,8 | sort | uniq -c > $@

data/dataset_list: data/all_datasets.tsv scripts/process_dataset_list.py
	cat $< | cut -f 2,3 | python scripts/process_dataset_list.py | sort | uniq > $@

data/dataset_counts: data/dataset_list
	cat $< | cut -f 1 | sort | uniq -c > $@

data/reuse_estimates: scripts/weighted_citations.py data/all_datasets.tsv data/reuse_subsample_wos data/reuse_subsample_gs
	python $< > $@

data/repo_citation_counts: scripts/repo_citation_counts.py data/all_datasets.tsv
	python $< > $@

data/repo_dataset_counts: scripts/repo_dataset_counts.py data/all_datasets.tsv
	python $< > $@

data/repo_reuse_counts: scripts/repo_reuse_counts.py data/reuse_subsample_wos data/reuse_subsample_gs
	python $< > $@

data/year_citation_counts: scripts/canonical_repo_names.py data/all.tsv
	tail -n +2 data/all.tsv | python scripts/canonical_repo_names.py | cut -f 8,17,26,36 | sort | uniq -c > $@

data/refs.tsv: scripts/get_refs.py data/old_all_datasets.tsv
	python $^ > $@

figures:
	mkdir -p figures

figures/repo_histograms_%.$(fig_format): scripts/plot_distributions.py data/reuse_estimates
	python $< $* $@

figures/most_cited_datasets.$(fig_format): scripts/most_cited_datasets.py data/reuse_estimates
	python $< $@

figures/repo_comparison.$(fig_format): scripts/repo_comparison.py data/reuse_estimates data/all_datasets.tsv
	python $< $@