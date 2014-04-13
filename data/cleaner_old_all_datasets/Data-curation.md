Data curation of combined dataet
================================

This document describes the process to clean and curate the combined
dataset, originally named `old_all_datasets.tsv`.

Main accomplishments: 
---------------------

1. All data record rows align appropriately under header row.
   Initially, the different repository datasets had non-identical sets
   of columns, even if most columns were shared.
2. Filled in missing publications for data records by performing
   searches (see below for search procedures used).
3. Whereever possible, updated data records to include at least one
   identifier for a data record's associated publication (e.g., PMID,
   DOI).
4. Rearranged columns so that those common across repository datasets
   come first, and those specific to only some follow those that are
   common.
5. Consolidated repository dataset-specific columns where possible and
   meaningful. Added the repository dataset-specific meaning in
   parentheses to the column header.
6. Added 3 columns for Month, Day, and Year the data record citations
   were collected from WOS. These dates are taken from the last
   modified date of the per-data record files holding the collected
   citation data. The citation data file was identified by matching
   the file name using the string documented in column `string matched
   to (partial) file name to extract data collection date data`.
7. Where included in the `article reference` but missing from the
   article DOI column (`Data Collection Article DOI`), extracted DOI
   from the reference and filled in missing article DOI. Also, where
   the article was missing but found by searching, entered PubmedID
   and/or DOI into the respective columns.
8. Filled all empty cells with `NA` so it is clear that the
   corresponding value is not available (rather than missing due to
   pending searches or other data curation tasks). (A final pass over
   the whole dataset [is still pending]
   (https://github.com/NESCent/1000-datasets/issues/10).)
9. Moved notes previously contained in `article reference` column to a
   new column named `article reference note`. Typically, these notes
   concern the data collection process.


Details:
--------

### Initial cleanup

The original version of `old_all_datasets.tsv` did not cleanly open in
Excel, due to embedded non-delimiting tabs and double quotes. To
address this, a text editor was used to open the file, and to perform
the following changes:

- Replaced double quotes with single quotes.
- Replaced `\t` embedded within fields and replaced with `|` (bar).
- Based on repository change history, adjusted column headings.

After this, the table opened (more) cleanly in Excel. Further cleanup
was performed in Excel:

- Imported file as Unicode 5.1 (UTF-8). After this, a few authors'
  names continue to display incorrectly, but fewer than with other
  encodings.
- Imported all columns as "Text" (rather than General, which is the
  default but causes errors).
- Replaced empty cells with `NA`.

These cleanup steps reduced the apparent number of columns in the file
from more than 30 (depending on encoding) to 18.


### Dataset-Level Changes

- Rearranged the columns to line up data across the repository datasets.
- Added citation data collection dates for each repository dataset
  based on Dropbox files at
  `data/10-wos_citations_to_data_collection_papers/<dataset_name>`
  (wrote the file list with dates to text using `ls -l >
  <data_set>_file_list.txt`). Entered dates into table in the form of
  3 new columns (`MONTH_wos_citingPaper_colxn`,
  `DAY_wos_citingPaper_colxn`, `YEAR_wos_citingPaper_colxn`).
- Added `article data` column, coded as follows: 
    * `1` = identifier available for reference (1151 items);
    * `2` = no identifier, but reference complete (29 items); 
    * `0` = incomplete reference (63 items).

For further changes and notes specific to a repository dataset see
"Changes By Dataset" below, which lists the datasets the in order
visited.


### Search For Publications Associated With A Data Record

To match publications to datasets via GS searches, GS search phrase
that included the accession number was first searched. If there were
more than 10 references, either the first author of the dataset was
added to the search in an author search, or a keyword from the title
of the dataset, or the species name (either genus species or just the
specific name to account for truncation of genera names). In some
cases, where there were many results, a combination of these was
performed and/or the results were truncated to include only
2000-present. In cases where data was also filed elsewhere (e.g.,
StemBank), the StemBank accession number and 'Stembank' were also
searched, with possible additions of extra query terms as described
above. No more than 15 minutes was devoted to searching for any given
dataset.

If a publication indicated that the named dataset searched for was
deposited or submitted or similar to a data repository, that
publication was identified as the 'article reference' for the dataset.


### Finalizing Draft Dataset

Re-order entries to correct for changes when matching collection date data
remove extra (mid-file) headers
check each column of data, move stray comments to 'COMMENTS' column
Added 'article reference note' column to remove extra info from 'article reference' column
Note on 'Dropbox filenames' column: new column, 'string matched to (partial) file name to extract data collection date data' contains either the file name (- '.txt') or partial filename used to match date data

Notes:
'WoS Cited by how many?' appears to hold the same data as 'total citations'. Tested in Pangaea - exactly the same for this set - didn't test others.

### Changes By Dataset

#### PANGAEA

Note on Pangaea data: Data associated with a publication is collocated
under one Pangaea data DOI, with description. Each collocated dataset
is also given a Pangaea data DOI and is linked to a web display with
additional description. Description for the composite dataset is
downloaded in zip file with dataset; for each individual dataset, at
the beginning to the tab delimited file.

compared 'data citation (dataset doi) OLD' & 'data citation (dataset
doi) NEW', kept items that differed - these are primarily (if not all)
article DOI's

data URL's tested (~5) did not bring up the corresponding row in the
data set - apparently not persistent. A search is executed and the
result associated with the '&offset=' is displayed, but this result
did not match data table entries examined. According to the search
results, there were 219 datasets found for the search specified in the
URL ('@supplement year:2005 citation:year:2005')

Added dates from file list. Files names by DOI included in 'data
citation (dataset doi) OLD' - therefore, file names, slightly
transformed, matched to old dataset DOI's, to add collection dates to
data table.


#### ArrayExpress

Added dates from file list. Files named by accession, which was used
to match txt file with dates, add to dates to data file.

Went back and checked the apparent missing entries in
ArrayExpress. Most of these seem to be a result of multiple entries
for some experiments in our dataset. Only one (E-UMCU-15) appears to
have been moved, removed, or something else:
http://www.ebi.ac.uk/arrayexpress/experiments/E-UMCU-15/ Message at
this URL: "We’re sorry but we can’t find the page or file you
requested… The resource located at
/arrayexpress/experiments/E-UMCU-15/ may have been removed, had its
name changed, or be temporarily unavailable…ArrayExpress update… We’ve
just updated ArrayExpress, so things have moved around a bit. Please
contact us and we will look into it for you."

#### BMRB

Added dates from file list. Files names by accession, which was used
to match txt file with dates, add to dates to data file.

#### GEO:

Note on GEO data: previously saw that these might be hierarchical /
linked data (based on Data Citation Index review) - could look into at
source

Rearrange reference, 'in ISI', a couple of other columns 
extract PMIDs from reference, if available:
^(.+?)PMID:[\s](\d{8,})
replace with \2

Added dates from file list. Files named by accession, which was used to match txt file with dates, add to dates to data file.
GSE3221.txt (data collected on Oct 23 2010): file not matched to data in data table (maybe was misnamed?)
manually matched files, collection dates when results spread across 2 files


#### GEOROC

Added data collection dates as above, matching on accession. No
exceptions in matching for this set.

##### HEPData

Reference entries look like:
> Published: PL B638,128 Preprint: CERN-PH-EP/2005-058 (Spires ID: 6618987)

When adding dates, did not find a listing in data table for p729
(Collected Jul 27 2011) though there is a file for it. Matched on
'Dropbox filenames'

#### Journal Archives

- liberal switching columns to match other data sets. Original Google
  Spreadsheet did not import well; headings visible in text program;
  original Journal tracking excel file useful
- added column to all: `Journal (for Journal Archives sets)`
- Many versions / groupings of bibliographic data available across
  journals - grouped these in columns on the far right of the data
  table.  Added dates from file list. Files named by 'ID' (old column
  name, now `accession`)

Journal-specific notes:

- **BIOSTAT**: extracted DOI's from abbreviated reference entry (e.g.,
  "Biostat (2005) 6(1): 27-38 doi:10.1093/biostatistics/kxh015")
  using: `Find: ^(.+?)doi:(\d+) Replace: \2`

- **Journal Of Money Credit And Banking**: in data table fixed
  references broken across fields

- **Systematic Biology**:
    * A couple of entries had different issue numbers indicated in
      different places - should check references to verify the rest of
      the information (items noted in `COMMENTS`)
    * DOIs adjusted to contain just DOI, extra bibliographic info moved to
      `COMMENTS` (amount of info recorded differs by row/item)

- For several journals there were no article DOIs available in the
  data table:
    * Journal Of Money Credit And Banking
    * Journal Of Applied Econometrics
    * Econometric Society
    * The Federal Reserve Bank Of St. Louis Review
    * Conflict Resolution
    * International Studies Quarterly
    * Journal Of Peace Research

#### PDB

Added dates from file list. files names by accession.
GS Search Terms were constructed for PDB entries that did not yet have publication info, following the example of previous GS Search Term phrases.


#### TreeBase

When matching dates, file found for S1253 (collected Dec 17 2010), but
with no corresponding entry in the data table

