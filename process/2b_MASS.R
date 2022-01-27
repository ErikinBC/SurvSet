
# ------------------ MASS DATASETS ---------------- #

# (xiiv) Aids2: https://rdrr.io/cran/MASS/src/inst/scripts/ch13.R
# This is domain knowledge but the point of this date is thta AZT started being used for AIDS patient in mid-1987 and
#   HIV patient in mid-1990, so the data is usually split
time.depend.covar <- function(data) {
  id <- row.names(data); n <- length(id)
  events <- c(0, 10043, 11139, 12053) # julian days
  crit1 <- matrix(events[1:3], n, 3 ,byrow = TRUE)
  crit2 <- matrix(events[2:4], n, 3, byrow = TRUE)
  diag <- matrix(data$diag,n,3); death <- matrix(data$death,n,3)
  incid <- (diag < crit2) & (death >= crit1); incid <- t(incid)
  indr <- col(incid)[incid]; indc <- row(incid)[incid]
  ind <- cbind(indr, indc); idno <- id[indr]
  state <- data$state[indr]; T.categ <- data$T.categ[indr]
  age <- data$age[indr]; sex <- data$sex[indr]
  late <- indc - 1
  start <- t(pmax(crit1 - diag, 0))[incid]
  stop <- t(pmin(crit2, death + 0.9) - diag)[incid]
  status <- matrix(as.numeric(data$status),n,3)-1 # 0/1
  status[death > crit2] <- 0; status <- status[ind]
  levels(state) <- c("NSW", "Other", "QLD", "VIC")
  levels(T.categ) <- c("hs", "hsid", "id", "het", "haem",
                       "blood", "mother", "other")
  levels(sex) <- c("F", "M")
  data.frame(idno, zid=factor(late), start, stop, status,
             state, T.categ, age, sex)
}
Aids3 <- time.depend.covar(Aids2)
tmp.dat <- data.table(Aids3)
tmp.dat[, `:=` (T.categ = fct_recode(as.character(T.categ),'mother'='other'),
               zid = factor(zid)) ]
X.aids <- model.matrix(~zid+state+sex+T.categ+age,data=tmp.dat)[,-1]
So.aids <- with(tmp.dat, Surv(start,stop,status==1))
id.aids <- as.numeric(as.factor(tmp.dat$idno))
cr.aids <- NULL

# (xv) Melanoma
tmp.dat <- MASS::Melanoma
So.melanoma <- with(tmp.dat, Surv(time, status %in% c(1,3)))
X.melanoma <- model.matrix(~sex+age+year+thickness+ulcer,data=tmp.dat)[,-1]
id.melanoma <- seq(nrow(X.melanoma))
cr.melanoma <- data.table(time=tmp.dat$time, 
                          event=as.numeric(as.character(fct_recode(as.character(tmp.dat$status),'1'='1','0'='2','2'='3'))))
