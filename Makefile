all: all_clean.tsv

%.tsv: %.csv convert_to_tsv.py
	python convert_to_tsv.py $< > $@

journal_list: all_clean.tsv title_case.py
	cat $< | cut -f 21 | python title_case.py | sort | uniq > $@