all: journal_list repo_list dataset_list citation_distribution

all_clean.tsv: all_clean.csv convert_to_tsv.py canonical_repo_names.py
	python convert_to_tsv.py $< | python canonical_repo_names.py > $@

journal_list: all_clean.tsv title_case.py
	cat $< | tail -n +2 | cut -f 21 | python title_case.py | sort | uniq > $@

repo_list: all_clean.tsv
	cat $< | tail -n +2 | cut -f 8 | sort | uniq > $@

citation_distribution: all_clean.tsv
	cat $< | tail -n +2 | cut -f 8,15 | sort | uniq -c > $@
