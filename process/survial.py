# Process the Survival package
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda, df_map, add_suffix

class package(baseline):
    # --- (i) cancer --- #
    def process_cancer(self):
        df_cancer = load_rda(self.dir_process, 'cancer.rda')
        cn_fac = ['inst', 'ph.ecog', 'sex']
        cn_num = ['wt.loss', 'ph.karno', 'pat.karno', 'meal.cal', 'age']
        # (i) Create event, time, and id

        # (ii) Subset
        # (iii) Feature transform
        # (iv) Define num, fac, and Surv
        # (v) Write

        df_cancer['event'] = np.where(df_cancer['status'] == 2, 1, 0)
        df_cancer['time'] = df_cancer['time'].astype(int)
        # Define 0 as missing institution
        df_cancer['inst'] = df_cancer['inst'].fillna(0).astype(int)
        # Define -1 as missing
        df_cancer['ph.ecog'] = df_cancer['ph.ecog'].fillna(-1).astype(int)
        df_cancer['sex'] = df_cancer['sex'].map({1:'M',2:'F'})
        # Clean up 
        add_pid(df_cancer)
        df_cancer = df_cancer[self.cn_surv + cn_num + cn_fac]
        df_cancer = rename_cols(df_cancer , cn_num, cn_fac)
        # Save
        path_write = os.path.join(self.dir_output, 'cancer.csv')
        df_cancer.to_csv(path_write, index=False)


    # --- (ii) cgd --- #
    def process_cgd(self):
        df_cgd = load_rda(self.dir_process, 'cgd.rda')
        df_cgd.reset_index(drop=True, inplace=True)
        # Assign
        df_cgd.rename(columns={'id':'pid', 'tstart':'time', 'tstop':'time2', 'status':'event'}, inplace=True)
        df_cgd['steroids'] = df_cgd['steroids'].map({0:'N', 1:'Y'})
        df_cgd['propylac'] = df_cgd['propylac'].map({0:'N', 1:'Y'})
        # Clean up
        cn_fac = ['center', 'treat', 'sex', 'inherit', 'steroids', 'propylac', 'hos.cat']
        cn_num = ['age', 'height', 'weight']
        df_cgd = df_cgd[self.cn_surv2 + cn_num + cn_fac]
        df_cgd = rename_cols(df_cgd , cn_num, cn_fac)
        # Save
        path_write = os.path.join(self.dir_output, 'cgd.csv')
        df_cgd.to_csv(path_write, index=False)

    # --- (iii) colon --- #
    def process_colon(self):
        df_colon = load_rda(self.dir_process, 'colon.rda')
        # Subset to death event (100% event rate for this dataset)
        df_colon = df_colon[df_colon['etype'] == 2]
        df_colon.reset_index(drop=True, inplace=True)
        # Assign features
        df_colon['id'] = df_colon['id'].astype(int)
        df_colon.rename(columns={'id':'pid', 'status':'event'}, inplace=True)
        df_colon['sex'] = df_colon['sex'].map({1:'M',0:'F'})
        df_colon['surg'] = df_colon['surg'].map({1:'long',0:'short'})
        cn_bin = ['obstruct', 'perfor', 'adhere', 'node4']
        df_colon[cn_bin] = df_colon[cn_bin].apply(lambda x: x.map({1:'Y',0:'N'}))
        # Missing to zero
        df_colon['differ']
        
        # Convert floats to integers with no decimals
        cn_int = ['time', 'age', 'event', 'differ', 'extent']
        df_colon[cn_int] = df_colon[cn_int].apply(num2int)
        # Clean up
        cn_fac = ['sex', 'differ', 'extent', 'surg'] + cn_bin
        cn_num = ['age', 'nodes']
        df_colon = df_colon[self.cn_surv + cn_num + cn_fac]
        df_colon = rename_cols(df_colon , cn_num, cn_fac)
        # Save
        path_write = os.path.join(self.dir_output, 'colon.csv')
        df_colon.to_csv(path_write, index=False)


        

        df_colon['id'].isnull().any()

# # (iv) colon
# tmp.dat <- data.table(survival::colon)
# tmp.dat <- tmp.dat[tmp.dat[,.I[etype == max(etype)],by=id]$V1]
# # Median/mode fill for NAs
# tmp.dat[, `:=` (nodes = ifelse(is.na(nodes),median(nodes,na.rm=T),nodes),
#                 differ = ifelse(is.na(differ), as.numeric(names(sort(table



cn_surv = ['pid', 'time', 'event']
cn_surv2 = ['pid', 'time', 'time2', 'event']
dir_base = os.getcwd()
dir_output = os.path.join(dir_base, 'output')
dir_pkgs = os.path.join(dir_base, 'pkgs')
self = package(pkg='survival', dir_pkgs=dir_pkgs, dir_output=dir_output, cn_surv=cn_surv, cn_surv2=cn_surv2)






# # (v) flchain
# tmp.dat <- survival::flchain
# So.flchain <- with(tmp.dat, Surv(futime,death))
# tmp.dat$creatinine <- ifelse(is.na(tmp.dat$creatinine),median(tmp.dat$creatinine,na.rm = T),tmp.dat$creatinine)
# X.flchain <- model.matrix(~age+sex+sample.yr+kappa+lambda+creatinine+mgus,data=tmp.dat)[,-1]
# id.flchain <- seq(nrow(X.flchain))
# cr.flchain <- NULL

# # (vi) heart
# So.heart <- with(survival::heart, Surv(start,stop,event))
# X.heart <- model.matrix(~age+year+surgery+transplant,data=survival::heart)[,-1]
# id.heart <- as.numeric(as.factor(survival::heart$id))
# cr.heart <- NULL

# # (vii) lung
# tmp.dat <- data.table(survival::lung)
# tmp.dat[, (colnames(tmp.dat)) := lapply(.SD, function(ll) ifelse(is.na(ll),median(ll,na.rm=T),ll)), .SDcols=colnames(tmp.dat) ]
# tmp.dat[, `:=` (inst = fct_lump(as.factor(inst),prop=0.05))]
# X.lung <- model.matrix(~inst+age+sex+ph.ecog+ph.karno+pat.karno+meal.cal+wt.loss,data=tmp.dat)[,-1]
# So.lung <- with(tmp.dat,Surv(time,status==2))
# id.lung <- seq(nrow(X.lung))
# cr.lung <- NULL

# # (viii) mgus2
# tmp.dat <- data.table(survival::mgus2)
# cn <- c('mspike','hgb','creat')
# tmp.dat[, (cn) := lapply(.SD, function(ll) ifelse(is.na(ll),median(ll,na.rm=T),ll)), .SDcols=cn ]
# So.mgus2 <- with(mgus2, Surv(futime, death))
# X.mgus2 <- model.matrix(~age+sex+hgb+creat+mspike+ptime+pstat,data=tmp.dat)[,-1]
# id.mgus2 <- as.numeric(as.factor(tmp.dat$id))
# cr.mgus2 <- NULL

# # (ix) ovarian
# So.ovarian <- with(survival::ovarian,Surv(futime,fustat))
# X.ovarian <- model.matrix(~age+factor(resid.ds)+factor(rx)+factor(ecog.ps),data=survival::ovarian)[,-1]
# id.ovarian <- seq(nrow(X.ovarian))
# cr.ovarian <- NULL

# # (x) pbc
# tmp.dat <- data.table(survival::pbc)
# tmp.dat <- tmp.dat[-which(apply(tmp.dat,1,function(rr) sum(is.na(rr)))>2)]
# # Fill in the missing values < 5%
# cn <- c('copper','platelet')
# tmp.dat[, (cn) := lapply(.SD, function(ll) ifelse(is.na(ll),median(ll,na.rm=T),ll)), .SDcols=cn ]
# tmp.dat[, edema := fct_recode(as.character(edema),'none'='0','untreated'='0.5','edema'='1')]
# X.pbc <- model.matrix(~factor(trt)+age+sex+ascites+hepato+spiders+factor(edema)+bili+
#                albumin+copper+alk.phos+ast+platelet+protime+factor(stage),data=tmp.dat)[,-1]
# So.pbc <- with(tmp.dat,Surv(time=time,event=(status==2)))
# id.pbc <- as.numeric(as.factor(tmp.dat$id))
# cr.pbc <- data.table(time=tmp.dat$time, event=tmp.dat$status)

# # (xi) retinopathy
# So.retinopathy <- with(survival::retinopathy, Surv(futime,status))
# X.retinopathy <- model.matrix(~laser+eye+age+type+trt+risk,data=retinopathy)[,-1]
# id.retinopathy <- as.numeric(as.factor(survival::retinopathy$id))
# cr.retinopathy <- NULL

# # (xii) veteran
# So.veteran <- with(survival::veteran, Surv(time,status))
# X.veteran <- model.matrix(~factor(trt)+celltype+karno+diagtime+age+factor(prior),data=survival::veteran)[,-1]
# id.veteran <- seq(nrow(X.veteran))
# cr.veteran <- NULL

# # (xiii) nwtco
# So.nwtco <- with(survival::nwtco, Surv(time=edrel, event=rel))
# X.nwtco <- model.matrix(~factor(instit)+factor(histol)+factor(stage)+factor(study)+age+in.subcohort,data=nwtco)[,-1]
# id.nwtco <- as.numeric(as.factor(survival::nwtco$seqno))
# cr.nwtco <- NULL
