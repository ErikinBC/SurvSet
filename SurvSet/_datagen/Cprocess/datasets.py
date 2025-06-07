"""
Contains the custom dataset processing classes for various datasets.
"""

# External imports
import os
import numpy as np
import pandas as pd
# Internal imports
from ..utils.funs_class import baseline
from ..utils.funs_support import str_subset, read_xls_with_encoding


class hosmer(baseline):
    # --- (i) uis --- #
    def process_uis(self, fn):
        dir_hosmer = os.path.join(self.dir_process, 'hosmer')
        path = os.path.join(dir_hosmer, '%s.dat' % fn)
        df = pd.read_csv(path, sep='\\s{1,}', engine='python', header=None)
        df = df.replace('.',np.nan)
        cn = ['id', 'age', 'beck', 'heroic', 'ivhx', 'ndrugtx', 'race', 'treat', 'site', 'los', 'time', 'censor']
        df.columns = cn
        cn_fac = ['heroic', 'ivhx', 'race', 'treat', 'site']
        cn_num = ['age', 'beck', 'ndrugtx']
        # (iii) Feature transform
        di_map = {'heroic':{'1':'Heroin&Cocaine','2':'Heroin','3':'Cocaine','4':'Neither',np.nan:np.nan}, 'ivhx':{'1':'Never','2':'Previous','3':'Recent', np.nan:np.nan}, 'race':{'0':'white','1':'other',np.nan:np.nan}, 'treat':{0:'short', 1:'long'}, 'site':{0:'A',1:'B'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'censor', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) FRTCS --- #
    def process_FRTCS(self, fn):
        dir_hosmer = os.path.join(self.dir_process, 'hosmer')
        path = os.path.join(dir_hosmer, '%s.dat' % fn)
        # 1. Define column names (must match order in FRTCS.dat)
        col_names = [
            "id","age","sex",
            "date0","sbp0","dbp0","antihyp0",
            "date1","sbp1","dbp1","antihyp1",
            "date2","sbp2","dbp2","antihyp2",
            "date_event","censor"
        ]
        # 2. Read the data
        df = pd.read_csv(
            path,
            sep=r'\s+',
            names=col_names,
            na_values=".",
            header=None,
            comment="#"
        )
        # 3. Parse date columns
        for dc in ["date0", "date1", "date2", "date_event"]:
            df[dc] = pd.to_datetime(df[dc], format="%d%b%y")
        # 4. Build the long‐format table
        records = []
        for _, row in df.iterrows():
            pid = row["id"]
            age = row["age"]
            sex = row["sex"]
            starts = [row["date0"], row["date1"], row["date2"]]
            ends   = [row["date1"], row["date2"], row["date_event"]]
            sbps     = [row["sbp0"], row["sbp1"], row["sbp2"]]
            dbps     = [row["dbp0"], row["dbp1"], row["dbp2"]]
            antihyps = [row["antihyp0"], row["antihyp1"], row["antihyp2"]]
            for i in range(3):
                start, end = starts[i], ends[i]
                if pd.isna(start) or pd.isna(end):
                    continue
                t0 = (start - row["date0"]).days
                t1 = (end   - row["date0"]).days
                event_flag = int(row["censor"]) if i == 2 else 0
                records.append({
                    "pid": pid,
                    "time": t0,
                    "time2": t1,
                    "sbp": sbps[i],
                    "dbp": dbps[i],
                    "antihyp": antihyps[i],
                    "event": event_flag,
                    "age": age,
                    "sex": sex
                })
        long_df = pd.DataFrame.from_records(records)
        # sort by pid & time
        long_df = long_df.sort_values(["pid","time"]).reset_index(drop=True)
        # Map the sex
        long_df['sex'] = long_df['sex'].map({1:'M',2:'F'})
        # Map the drug treatments
        long_df['antihyp'] = long_df['antihyp'].map({1:'Y',0:'N'})
        # (iv) Define num, fac, and Surv
        cn_num = ['age','sbp','dbp']
        cn_fac = ['sex','antihyp']
        df = self.Surv(df=long_df, cn_num=cn_num, cn_fac=cn_fac, cn_event='event', cn_time='time', cn_time2='time2', cn_pid='pid')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class openml(baseline):
    # --- (i) phpl04K8a --- #
    def process_phpl04K8a(self, fn ):
        path = os.path.join(self.dir_process, 'phpl04K8a.csv')
        df = pd.read_csv(path)
        cn_fac = ['sex']
        cn_num = ['age'] + list(str_subset(df.columns,'^g'))        
        # (i) Create event, time, and id
        df['OS_event']= df['OS_event'].str.replace('[^0-9]','',regex=True).astype(int)
        # (iii) Feature transform
        df['sex']= df['sex'].str.replace('[^a-z]','',regex=True)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'OS_event', 'OS_years')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
    

class princeton(baseline):
    # --- (i) divorce --- #
    def process_divorce(self, fn ):
        path = os.path.join(self.dir_process, f'{fn}.dat')
        df = pd.read_csv(path,sep='\\s{2,}',engine='python')
        cn_num = []
        cn_fac = ['heduc', 'heblack', 'mixed']
        # (i) Create event, time, and id
        df['div'] = np.where(df['div'] == 'Yes',1,0)
        # (iii) Feature transform
        df['heduc'] = df['heduc'].str.replace('\\s|years','',regex=True)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'div', 'years')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class Reddy(baseline):
    # All four datasets have the same format
    def clean_df(self, fn):
        fold = os.path.join(self.dir_process, 'Gene_expression_data')
        path = os.path.join(fold, '%s.csv' % fn)
        df = pd.read_csv(path)
        # First three columns are time, event, ignore
        cn_df = df.columns
        cn_A = cn_df[3:]
        n_A = len(cn_A)
        cn_gene = 'gene_'+pd.Series(range(1,n_A+1)).astype(str)
        di_cn = dict(zip(cn_A, cn_gene))
        self.df_rename(df, di_cn)
        df.rename(columns=dict(zip(cn_df[:3],['time','event','drop'])), inplace=True)
        cn_fac = []
        cn_num = list(cn_gene)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return df

    # --- (i) NSBCD --- #
    def process_NSBCD(self, fn ):
        df = self.clean_df(fn)
        return fn, df

    # --- (ii) AML_Bull --- #
    def process_AMLBull(self, fn ):
        df = self.clean_df(fn)
        return fn, df

    # --- (iii) DBCD --- #
    def process_DBCD(self, fn ):
        df = self.clean_df(fn)
        return fn, df

    # --- (iv) DLBCL --- #
    def process_DLBCL(self, fn ):
        df = self.clean_df(fn)
        return fn, df



class vanderbilt(baseline):
    # --- (i) support2 --- #
    def process_support2(self, fn):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        dir_support = os.path.join(dir_vanderbilt, '%scsv' % fn)
        path = os.path.join(dir_support, '%s.csv' % fn)
        df = pd.read_csv(path)
        cn_fac = ['sex', 'dzgroup', 'dzclass', 'num.co', 'race', 'diabetes', 'dementia', 'ca', 'dnr', 'sfdm2', 'income']
        cn_num = ['age', 'num.co', 'edu', 'scoma', 'hday', 'sps', 'surv2m', 'surv6m', 'meanbp', 'wblc', 'hrt', 'resp', 'temp', 'pafi', 'alb', 'bili', 'crea', 'sod', 'ph', 'glucose', 'bun', 'urine', 'adlp', 'adls']
        # (iii) Feature transform
        di_map = {k:{1:'Y',0:'N'} for k in ['diabetes', 'dementia']}
        self.df_map(df, di_map)
        
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'death', 'd.time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) prostate --- #
    def process_prostate(self, fn ):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        path = os.path.join(dir_vanderbilt, '%s.xls' % fn)
        df = read_xls_with_encoding(path)
        cn_num = ['age', 'wt', 'sbp', 'dbp', 'hg', 'sz', 'sg', 'ap', 'sdate']
        cn_fac = ['stage', 'rx', 'pf', 'hx', 'ekg', 'bm']
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 'alive', 0, 1)
        # (iii) Feature transform
        di_map = {k:{1:'Y',0:'N'} for k in ['hx', 'bm']}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'dtime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) Framingham --- #
    def process_Framingham(self, fn):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        path = os.path.join(dir_vanderbilt, '2.20.%s.csv' % fn)
        df = pd.read_csv(path)
        cn_fac = ['sex','month']
        cn_num = ['sbp','dbp','scl','age','bmi']
        # (iii) Feature transform
        di_map = {'sex':{2:'F',1:'M'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'chdfate', 'followup')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iv) rhc --- #
    def process_rhc(self, fn):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        path = os.path.join(dir_vanderbilt, f'{fn}.csv')
        df = pd.read_csv(path).reset_index(drop=True)
        cn_hx = list(str_subset(df.columns, 'hx$'))
        cn_1 = str_subset(df.columns,'1$')
        cn_1_num = list(cn_1[((df[cn_1].dtypes == float) | (df[cn_1].dtypes == int)).values])
        cn_1_fac = list(cn_1[(df[cn_1].dtypes == object).values])
        cn_fac = ['cat1', 'cat2', 'ca', 'sex', 'ninsclas', 'resp', 'card', 'neuro', 'gastr', 'renal', 'meta', 'hema', 'seps', 'trauma', 'ortho', 'race', 'income']
        cn_fac += cn_hx + cn_1_fac
        cn_fac = list(np.unique(cn_fac))
        cn_num = ['age', 'edu', 'adld3p'] + cn_1_num
        # (i) Create event, time, and id
        df = df.assign(death=lambda x: np.where(x['death'] == 'Yes', 1, 0))
        df = df.assign(time=lambda x: np.where(x['death']==1, x['dthdte']-x['sadmdte'], x['lstctdte']-x['sadmdte']).astype(int))
        # (iii) Feature transform
        di_map = {k:{1:'Y',0:'N'} for k in cn_hx}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'death', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (v) acath --- #
    def process_acath(self, fn):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        path = os.path.join(dir_vanderbilt, '%s.xls' % fn, '%s.xls' % fn)
        df = pd.read_excel(path, engine='xlrd')
        cn_num = ['age', 'choleste']
        cn_fac = ['sex']
        # (iii) Feature transform
        di_map = {'sex':{0:'M', 1:'F'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'sigdz','cad.dur')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (vi) vlbw --- #
    def process_vlbw(self, fn):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        fold_vlbw = os.path.join(dir_vanderbilt, 'vlbw')
        path = os.path.join(fold_vlbw, f'{fn}.csv')
        df = pd.read_csv(path)
        cn_fac = ['race', 'inout', 'delivery', 'pvh', 'ivh', 'ipe', 'sex', 'twn', 'magsulf', 'meth', 'toc', 'vent', 'pneumo', 'pda', 'cld']
        cn_num = ['birth', 'lowph', 'pltct', 'bwt', 'gest', 'lol', 'apg1', ]
        # (ii) Subset
        df = df.query('hospstay > 0').reset_index(drop=True)
        # (iii) Feature transform
        
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'dead', 'hospstay')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
