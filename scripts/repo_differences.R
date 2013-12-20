data = read.delim('data/reuse_estimates', header=FALSE)
names(data) = c('repo', 'id', 'reuses')

result = aov(reuses~repo, data=data)
summary(result)