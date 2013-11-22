library(vegan)

data = read.delim('data/keyword_matrix')

data2 = data[,3:length(data[1,])]

# data_type = dataset or citation, i.e. published data or reused data
# formula includes repository nested within data type 

adonis(data2 ~ data$data_type + 
               data$data_type*data$repo,
       data, permutations = 1000)
