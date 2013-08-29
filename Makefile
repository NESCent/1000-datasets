figures=figures/repo_histograms.svg
summaries=journal_list repo_list dataset_list citation_distribution

.PHONY: all clean

all: $(figures) $(summaries)

clean:
	rm -f $(figures)
	rm -f $(summaries)

%.tsv: %.csv scripts/convert_to_tsv.py scripts/canonical_repo_names.py
	python scripts/convert_to_tsv.py $< | python canonical_repo_names.py > $@

journal_list: all.tsv scripts/title_case.py
	cat $< | tail -n +2 | cut -f 21 | python scripts/title_case.py | sort | uniq > $@

repo_list: all.tsv
	cat $< | tail -n +2 | cut -f 8 | sort | uniq > $@

citation_distribution: all.tsv
	cat $< | tail -n +2 | cut -f 8,15 | sort | uniq -c > $@

dataset_list: all_datasets.tsv scripts/process_dataset_list.py
	cat $< | cut -f 2,3 | python scripts/process_dataset_list.py | sort | uniq > $@

dataset_counts: dataset_list
	cat $< | cut -f 1 | sort | uniq -c > $@

figures/repo_histograms.svg: scripts/plot_distributions.py citation_distribution dataset_counts
	python $< $@