* How often is data from repositories used in the published literature? What is 
the distribution of use across datasets and time?

    * rates of reuse by repository (histograms, ANOVA)
      PCA of histogram bin values - which repos have citation frequency 
      distributions which are the most similar

    * cumulative citations over time
        * needed: citation dates for each dataset (from Web of Science or Scopus)    
        * regression: IV=time, DV=cumulative citations

* AUTHORS: Who reuses data? Are investigators who reuse repository datasets 
similar to investigators who deposit data?

    * things to compare:
        * author department (cat)
        * author country (cat)
        * author institution (cat)

    * chi squared: IV=data vs reuse, DV=(dept, country, institution)

* STUDIES: What is data reused for? How similar are studies that reuse data to 
studies that deposit data?

    * things to compare:
        * keywords
        * number of authors
        * author institution
        * author country

    * will require keyword data

    * how similar (in multivariate space, by keywords) are citing papers to the 
      papers they cite?

    * figure 2 from proposal, topic cooccurrence network
