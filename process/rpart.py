# --- (xxxi) stagec --- #
tmp.dat <- data.table(rpart::stagec)
So.stagec <- with(tmp.dat, Surv(time=pgtime, event=pgstat))
# Pad missing values with mode/median
tmp.dat.na.mu <- apply(tmp.dat,2,function(cc) mean(is.na(cc)))
cn.na <- names(which(tmp.dat.na.mu > 0))
idx.na.class <- as.character(sapply(tmp.dat[,cn.na,with=F],class))
cn.na.int <- cn.na[which(idx.na.class == 'integer')]
cn.na.num <- cn.na[which(idx.na.class == 'numeric')]
tmp.dat[, (cn.na.int) := lapply(.SD, function(cc) ifelse(is.na(cc),as.numeric(names(sort(table(cc),decreasing=T)[1])),cc)),
        .SDcols=cn.na.int]
tmp.dat[, (cn.na.num) := lapply(.SD, function(cc) ifelse(is.na(cc),median(cc,na.rm=T),cc)), .SDcols=cn.na.num]
# Aggregate factor
tmp.dat[, `:=` (grade = fct_recode(as.character(grade),'1+2'='1','1+2'='2','3+4'='3','3+4'='4'),
                gleason = fct_recode(as.character(gleason),'3+4+5'='3','3+4+5'='4','3+4+5'='5','8+9+10'='8','8+9+10'='9','8+9+10'='10' ))]
# model matrix
X.stagec <- model.matrix(~pgtime+pgstat+age+factor(eet)+g2+factor(grade)+factor(gleason)+ploidy,data=tmp.dat)[,-1]
id.stagec <- seq(nrow(X.stagec))
cr.stagec <- NULL
