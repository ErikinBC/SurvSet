
# --- (lii) UnempDur --- #
tmp.dat <- Ecdat::UnempDur
# Remove any patients who are neither jobless nor re-employed
tmp.dat <- tmp.dat[-which(apply(tmp.dat[,2:5],1,sum)==0),]
# Censor1/2/3 are types of re-employment, censor4 is remains jobless
So.unemp1 <- with(tmp.dat, Surv(time=spell, event=(censor4==0)))
X.unemp1 <- model.matrix(~age+ui+reprate+disrate+logwage+tenure,data=tmp.dat)[,-1]
id.unemp1 <- seq(nrow(X.unemp1))
tmp.cr <- as.character(apply(tmp.dat[,2:5],1,function(cc) which(cc == 1)))
tmp.cr <- as.numeric(as.character(fct_recode(tmp.cr,'0'='4')))
cr.unemp1 <- data.table(time=tmp.dat$spell, event=tmp.cr)

# --- (liii) Unemployment --- #
tmp.dat <- Ecdat::Unemployment
So.unemp2 <- with(tmp.dat, Surv(time=duration, event=spell))
# Only use the first survey record data (ftp1) as otherwise features we leak information about duratoin length
X.unemp2 <- model.matrix(~race+sex+reason+search+pubemp+ftp1,data=tmp.dat)[,-1]
id.unemp2 <- seq(nrow(X.unemp2))
cr.unemp2 <- NULL
