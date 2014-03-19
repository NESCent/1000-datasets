ReadMe_old_all_datasets_v2.txt describes process to clean old_all_datasets.tsv to produce old_all_datasets_v2.tsv.

Main accomplishment: data aligns appropriately under header rows.
Data common across datasets in left side of table.
Data unique to (a) dataset(s) in right side of table. For these, corresponding datasets named in header, with notes as necessary.
Data collection dates added based on WOS citation file collection dates.
For datasets with PubMed ID's, DOI's embedded in reference material, not otherwise, these were extracted, included in appropriate columns.
Empty cells filled with 'NA'.
Notes in 'article reference' column moved to new 'article reference notes' column.


IN MORE DETAIL:


OPENING old_all_datasets.tsv:
In text editing program, opened old_all_datasets.tsv
replaced " with '
replaced \t with |
went through repository change points, adjusted headings

opened in excel:
import as unicode 5.1 (UTF-8) - a few authors' names appear broken, but less so than with other encodings
imported all columns as "Text" (rather than General, the default)
replaced empty cells with NA

Opening 'fixes' reduced file to 18 columns


DATASET LEVEL CHANGES
rearranged columns to line up data across datasets
added date data for each set based on dropbox files at 'data/10-wos_citations_to_data_collection_papers/<dataset_name>: file list written to text (ls -l > <data_set>_file_list.txt) 
Data entered in table in new columns :
MONTH_wos_citingPaper_colxn
DAY_wos_citingPaper_colxn
YEAR_wos_citingPaper_colxn

see 'CHANGES BY DATASET' (datasets listed in order visited) for changes/notes specific to a dataset


FINALIZING DRAFT DATASET
Re-order entries to correct for changes when matching collection date data
remove extra (mid-file) headers
check each column of data, move stray comments to 'COMMENTS' column
Added 'article reference note' column to remove extra info from 'article reference' column
Note on 'Dropbox filenames' column: new column, 'string matched to (partial) file name to extract data collection date data' contains either the file name (- '.txt') or partial filename used to match date data

Notes:
'WoS Cited by how many?' appears to hold the same data as 'total citations'. Tested in Pangaea - exactly the same for this set - didn't test others.

CHANGES BY DATASET

PANGAEA
Note on Pangaea data: Data associated with a publication is collocated under one Pangaea data DOI, with description. Each collocated dataset is also given a Pangaea data DOI and is linked to a web display with additional description. Description for the composite dataset is downloaded in zip file with dataset; for each individual dataset, at the beginning to the tab delimited file.

compared 'data citation (dataset doi) OLD' & 'data citation (dataset doi) NEW', kept items that differed - these are primarily (if not all) article DOI's

data URL's tested (~5) did not bring up the corresponding row in the data set - apparently not persistent. A search is executed and the result associated with the '&offset=' is displayed, but this result did not match data table entries examined. According to the search results, there were 219 datasets found for the search specified in the URL ('@supplement year:2005 citation:year:2005')

Added dates from file list. Files names by DOI included in 'data citation (dataset doi) OLD' - therefore, file names, slightly transformed, matched to old dataset DOI's, to add collection dates to data table.


ARRAY EXPRESS
Added dates from file list. Files named by accession, which was used to match txt file with dates, add to dates to data file.

Went back and checked the apparent missing entries in ArrayExpress. Most of these seem to be a result of multiple entries for some experiments in our dataset. Only one (E-UMCU-15) appears to have been moved, removed, or something else:
http://www.ebi.ac.uk/arrayexpress/experiments/E-UMCU-15/
Message at this URL: "We’re sorry but we can’t find the page or file you requested… The resource located at /arrayexpress/experiments/E-UMCU-15/ may have been removed, had its name changed, or be temporarily unavailable…ArrayExpress update… We’ve just updated ArrayExpress, so things have moved around a bit. Please contact us and we will look into it for you."

BMRB
Added dates from file list. Files names by accession, which was used to match txt file with dates, add to dates to data file.

GEO:
Note on GEO data: previously saw that these might be hierarchical / linked data (based on Data Citation Index review) - could look into at source

Rearrange reference, 'in ISI', a couple of other columns 
extract PMIDs from reference, if available:
^(.+?)PMID:[\s](\d{8,})
replace with \2

Added dates from file list. Files named by accession, which was used to match txt file with dates, add to dates to data file.
GSE3221.txt (data collected on Oct 23 2010): file not matched to data in data table (maybe was misnamed?)
manually matched files, collection dates when results spread across 2 files


GEOROC
Added data collection dates as above, matching on accession. No exceptions in matching for this set.

HEPData
Reference entries look like:
"Published: PL B638,128 Preprint: CERN-PH-EP/2005-058 (Spires ID: 6618987)"

When adding dates, did not find a listing in data table for p729 (Collected Jul 27 2011) though there is a file for it. Matched on 'Dropbox filenames'

JOURNAL ARCHIVES
liberal switching columns to match other data sets. Original Google Spreadsheet did not import well; headings visible in text program; original Journal tracking excel file useful
added column to all: "Journal (for Journal Archives sets)".
Many versions / groupings of bibliographic data available across journals -  grouped these in columns on the far right of the data table.
Added dates from file list. Files named by 'ID' (old column name, now 'accession')

data varies by journal… 

BIOSTAT
extracted DOI's from abbreviated reference entry (e.g., "Biostat (2005) 6(1): 27-38 doi:10.1093/biostatistics/kxh015") using:
Find: ^(.+?)doi:(\d+)
Replace: \2

JOURNAL OF MONEY CREDIT AND BANKING
note: no article DOI's available in data table
fixed ref broken across fields

SYSTEMATIC BIOLOGY
A couple of entries had different issue numbers indicated in different places - should check references to verify the rest of the information (items noted in "COMMENTS")
DOI'S adjusted to contain just DOI, extra bib info moved to 'COMMENTS' (amount of info recorded differs by row/item)

JOURNAL OF APPLIED ECONOMETRICS
note: no article DOI's available in data table

ECONOMETRIC SOCIETY
note: no article DOI's available in data table

THE FEDERAL RESERVE BANK OF St. LOUIS REVIEW
note: no article DOI's available in data table

CONFLICT RESOLUTION
note: no article DOI's available in data table

INTERNATIONAL STUDIES QUARTERLY
note: no article DOI's available in data table

JOURNAL OF PEACE RESEARCH
note: no article DOI's available in data table
--- end jrnl archives ---

PDB
Added dates from file list. files names by accession.

TreeBase
When matching dates, file found for S1253 (collected Dec 17 2010), but with no corresponding entry in the data table
