# Process the Survival package
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda, str_subset

# (i) Create event, time, and id
# (ii) Subset
# (iii) Feature transform
# (iv) Define num, fac, and Surv

class package(baseline):
    def run_all(self):
        # Get list of process functions
        methods = str_subset(pd.Series(dir(self)), '^process\\_')
        for method in methods:
            fun_process = getattr(self, method)
            fn, df = fun_process()
            self.write_csv('%s.csv' % fn, df)

    # --- (i) cancer --- #
    def process_cancer(self, fn = 'cancer'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        df.reset_index(drop=True, inplace=True)
        cn_fac = ['inst', 'ph.ecog', 'sex']
        cn_num = ['wt.loss', 'ph.karno', 'pat.karno', 'meal.cal', 'age']
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 2, 1, 0)
        # (ii) Subset
        # (iii) Feature transform
        di_map = {'sex':{1:'M',2:'F'}}
        self.df_map(df, di_map)
        df[cn_fac] = self.fill_fac(df[cn_fac])
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='status', cn_time='time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) cgd --- #
    def process_cgd(self, fn = 'cgd'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['center', 'treat', 'sex', 'inherit', 'steroids', 'propylac', 'hos.cat']
        cn_num = ['age', 'height', 'weight']
        # (i) Create event, time, and id
        # (ii) Subset (covariate features do not change)
        #       This is the time to first infection
        df = df.sort_values(['id','status'],ascending=False)
        df = df.groupby('id').head(1).sort_values('id').reset_index(drop=True)
        # (iii) Feature transform
        di_map = {'steroids':{0:'N', 1:'Y'}, 'propylac':{0:'N', 1:'Y'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'tstart', 'tstop', 'id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) colon --- #
    def process_colon(self, fn = 'colon'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_bin = ['obstruct', 'perfor', 'adhere', 'node4']
        cn_fac = ['rx', 'sex', 'differ'] + cn_bin
        cn_num = ['age', 'nodes']
        # (i) Create event, time, and id
        # (ii) Subset
        df = df[df['etype'] == 2]  # Time to death
        df.drop(columns=['etype','study'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # (iii) Feature transform
        di_map = {'sex':{1:'M',0:'F'}, 'surg':{1:'long',0:'short'}, 'differ':{1:'well', 2:'moderate', 3:'poor'}, 'extent':{1:'submucosa', 2:'muscle', 3:'serosa', 4:'contiguous structures'}}
        di_map = {**di_map, **{cn:{1:'Y',0:'N'} for cn in cn_bin}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        df[cn_fac] = self.fill_fac(df[cn_fac])  # Fill missing factors
        
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time', cn_pid='id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


# IS ADD SUFFIX UNIVERSAL??

import os
cn_surv = ['pid', 'time', 'event']
cn_surv2 = ['pid', 'time', 'time2', 'event']
dir_base = os.getcwd()
dir_output = os.path.join(dir_base, 'output')
dir_pkgs = os.path.join(dir_base, 'pkgs')
self = package(pkg='survival', dir_pkgs=dir_pkgs, dir_output=dir_output, cn_surv=cn_surv, cn_surv2=cn_surv2)
self.run_all()



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
