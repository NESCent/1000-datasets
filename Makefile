figures=figures/citation_distributions.png

all: $(figures) journal_list repo_list dataset_list citation_distribution

%.tsv: %.csv convert_to_tsv.py canonical_repo_names.py
	python convert_to_tsv.py $< | python canonical_repo_names.py > $@

journal_list: all.tsv title_case.py
	cat $< | tail -n +2 | cut -f 21 | python title_case.py | sort | uniq > $@

repo_list: all.tsv
	cat $< | tail -n +2 | cut -f 8 | sort | uniq > $@

citation_distribution: all.tsv
	cat $< | tail -n +2 | cut -f 8,15 | sort | uniq -c > $@

dataset_list: all_datasets.tsv process_dataset_list.py
	cat $< | cut -f 2,3 | python process_dataset_list.py | sort | uniq > $@

dataset_counts: dataset_list
	cat $< | cut -f 1 | sort | uniq -c > $@

figures/citation_distributions.png: plot_distributions.py citation_distribution dataset_counts
	python $< $@