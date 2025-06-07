"""
Contains all the different R packages and their respective dataset processing function
"""

# External modules
import os
import numpy as np
import pandas as pd
# Internal modules
from ..utils.funs_class import baseline
from ..utils.funs_support import load_rda, str_subset


class AdapEnetClass(baseline):
    pkg_name = 'AdapEnetClass'
    # --- (i) MCLcleaned --- #
    def process_MCLcleaned(self, fn: str):
        df = load_rda(self.dir_process, '%s.RData' % fn)
        cn_fac = []
        cn_num = list(str_subset(df.columns,'^X'))
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'cens', 'time', cn_pid='ID')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

class AF(baseline):
    pkg_name = 'AF'
    # --- (i) rott2 --- #
    def process_rott2(self, fn:str):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        di_cn = {'size':'tsize', 'pr':'progesterone', 'er':'estrogen'}
        self.df_rename(df, di_cn)
        cn_fac = ['meno', 'tsize', 'grade', 'hormon', 'chemo', 'recent']
        cn_num = ['year', 'age', 'nodes', 'progesterone', 'estrogen']
        # (i) Create event, time, and id
        df['osi'] = np.where(df['osi'] == 'deceased', 1, 0)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='osi', cn_time='os', cn_pid='pid')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class asaur(baseline):
    pkg_name = 'asaur'
    # --- (i) hepatoCellular --- #
    def process_hepatoCellular(self, fn = 'hepatoCellular'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = list(df.columns[2:15])
        cn_num = ['Age'] + list(df.columns[19:])
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='Death', cn_time='OS')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) pharmacoSmoking --- #
    def process_pharmacoSmoking(self, fn = 'pharmacoSmoking'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['grp', 'gender', 'race', 'employment', 'levelSmoking', 'ageGroup2', 'ageGroup4']
        cn_num = ['age', 'yearsSmoking', 'priorAttempts', 'longestNoSmoke']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='relapse', cn_time='ttr', cn_pid='id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) prostateSurvival --- #
    def process_prostateSurvival(self, fn = 'prostateSurvival'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['grade', 'stage', 'ageGroup']
        cn_num = []
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 1, 1, 0)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='status', cn_time='survTime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class bujar(baseline):
    pkg_name = 'bujar'
    # --- (i) chop --- #
    def process_chop(self, fn = 'chop'):
        # Merge chop and rchop datasets
        df1 = load_rda(self.dir_process, '%s.rda' % fn)
        df2 = load_rda(self.dir_process, 'r%s.rda' % fn)
        df = pd.concat(objs=[df1, df2], axis=0)
        df.reset_index(drop=True, inplace=True)
        del df1, df2
        cn_fac = []
        cn_num = list(df.columns[2:])        
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'survtime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class coin(baseline):
    pkg_name = 'coin'
    # --- (i) glioma --- #
    def process_glioma(self, fn = 'glioma'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex', 'histology', 'group']
        cn_num = ['age']
        # (i) Create event, time, and id
        df['event'] = df['event'].astype(int)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class coxph(baseline):
    pkg_name = 'coxphf'
    # --- (i) breast --- #
    def process_breast(self, fn = 'breast'):
        path = os.path.join(self.dir_process, '%s.txt' % fn)
        df = pd.read_csv(path, sep='\\s{1,}', engine='python')
        cn_fac = ['T','N','G','CD']
        cn_num = []
        df = df.drop_duplicates()
        # (iii) Feature transform
        di_map = {k:{1:'Unfavourable', 0:'Favourable'} for k in cn_fac}
        self.df_map(df, di_map)
        # (iv) Define Surv, and rename
        df = self.Surv(df, cn_num, cn_fac, 'CENS', 'TIME')
        df = self.add_suffix(df, cn_num, cn_fac)
        di_cn = {'T':'TumorStage', 'N':'NodalStatus', 'G':'Histology','CD':'CathepsinD'}
        di_cn = {'fac_'+k:'fac_'+v for k,v in di_cn.items()}
        self.df_rename(df, di_cn)
        return fn, df
    

class coxphf(baseline):
    pkg_name = 'coxphf'
    # --- (i) ova --- #
    def process_ova(self, fn = 'ova'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['karn', 'diam', 'figo']
        cn_num = ['karn', 'diam']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='death', cn_time='time', cn_pid='x')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
    

class CoxRidge(baseline):
    pkg_name = 'CoxRidge'
    # --- (i) ova --- #
    def process_ova(self, fn = 'ova'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['karn', 'diam', 'figo']
        cn_num = ['karn', 'diam']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='death', cn_time='time', cn_pid='x')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class Ecdat(baseline):
    pkg_name = 'Ecdat'
    # --- (i) UnempDur --- #
    def process_UnempDur(self, fn = 'UnempDur'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['ui']
        cn_num = ['age','reprate','disrate','tenure','logwage',]
        # (i) Create event, time, and id
        cn_censor = str_subset(df.columns, '^censor')
        cn_censor3 = str_subset(cn_censor, 'censor[1-3]')
        df['event'] = df[cn_censor3].sum(1)
        # (ii) Subset
        df = df[df[cn_censor].sum(1) == 1]
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'spell')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) Unemployment --- #
    def process_Unemployment(self, fn = 'Unemployment'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        # not using ftp to prevent information leakage
        cn_fac = ['race', 'sex', 'reason', 'search', 'pubemp']
        cn_num = []
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'spell', 'duration')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class EHA(baseline):
    pkg_name = 'EHA'
    # --- (i) scania --- #
    def process_scania(self, fn = 'scania'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex', 'parish', 'ses', 'immigrant']
        cn_num = ['birthdate']
        # (i) Create event, time, and id
        df = df.assign(time=lambda x: x['exit']-x['enter'])
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time', cn_pid='id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) oldmort --- #
    def process_oldmort(self, fn = 'oldmort'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex','civ','ses.50','birthplace', 'region']
        cn_num = ['birthdate','imr.birth']
        # (i) Create event, time, and id
        df['event'] = df['event'].astype(int)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'enter', 'exit', 'id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class frailtySurv(baseline):
    pkg_name = 'frailtySurv'
    # --- (i) hdfail --- #
    def process_hdfail(self, fn = 'hdfail'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['brand', 'type', 'rsc', 'rer', 'psc']
        cn_num = ['temp']
        # (iii) Feature transform
        # Extract model vs version
        u_models = pd.Series(list(df.model.unique()))
        u_brands = u_models.str.split(pat='\\s',n=1,expand=True)[0]
        u_brands = np.where(u_brands.str.contains('^[ST]'),'ST',u_brands)
        di_brands = dict(zip(u_models, u_brands))
        u_type = u_models.str.split(pat='\\s',regex=True).str[0]
        di_type = dict(zip(u_models, u_type))
        df['brand'] = df['model'].map(di_brands)
        df['type'] = df['model'].map(di_type)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class hdnom(baseline):
    pkg_name = 'hdnom'
    # --- (i) smart --- #
    def process_smarto(self, fn = 'smarto'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        df.columns = df.columns.str.lower()
        cn_fac = ['sex', 'diabetes', 'cerebral', 'aaa', 'periph', 'stenosis', 'albumin', 'smoking', 'alcohol']
        cn_num = ['age', 'systbp', 'diastbp', 'systh', 'diasth', 'length', 'weight', 'bmi', 'chol', 'hdl', 'ldl', 'trig', 'homoc', 'glut', 'creat', 'imt', 'packyrs']
        # (ii) Subset
        # (iii) Feature transform
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'tevent')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class iBST(baseline):
    pkg_name = 'iBST'
    # --- (i) burn --- #
    def process_burn(self, fn = 'burn'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        di_cn = {'Z1':'treatment', 'Z2':'sex', 'Z3':'race', 'Z4':'burn_area', 'Z5':'burn_head', 'Z6':'burn_buttock', 'Z7':'burn_trunk', 'Z8':'burn_upper_leg', 'Z9':'burn_lower_leg', 'Z10':'burn_resp', 'Z11':'burn_type'}
        self.df_rename(df, di_cn)
        cn_fac = list(np.setdiff1d(list(di_cn.values()),'burn_area'))
        cn_num = ['burn_area']
        # (i) Create event, time, and id
        # (iii) Feature transform
        di_map = {'sex':{0:'M',1:'F'}, 'race':{0:'nonwhite',1:'white'}, 'burn_type':{'1':'chemical', 2:'scald', 3:'eletric', 4:'flame'}, 'treatment':{0:'bath', 1:'cleanse'}}
        di_bool = {k:{1:'Y',0:'N'} for k in np.setdiff1d(str_subset(di_cn.values(), 'burn'),['burn_area','burn_type'])}
        di_map = {**di_map, **di_bool}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'D3', 'T3')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class invGauss(baseline):
    pkg_name = 'invGauss'
    # --- (i) d.oropha.rec --- #
    def process_oropha(self, fn = 'd.oropha.rec'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['inst', 'sex', 'treatm', 'grade', 'cond','site', 'tstage', 'nstage']
        cn_num = ['age', 'cond', 'tstage', 'nstage']
        # (iii) Feature transform
        di_map = {'sex':{1:'M',2:'F', 'treatm':{1:'standard',2:'test'}}}
        self.df_map(df, di_map)
        
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class JM(baseline):
    pkg_name = 'JM'
    # --- (i) aids --- #
    def process_aids(self, fn = 'aids'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['drug', 'gender', 'prevOI', 'AZT']
        cn_num = ['CD4']
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'start', 'stop', 'patient')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class joineR(baseline):
    pkg_name = 'joineR'
    # --- (i) heartvalve --- #
    def process_heartvalve(self, fn = 'heart.valve'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        df.reset_index(drop=True, inplace=True)
        cn_bin = ['lvh','redo','con.cabg','dm','acei']
        cn_fac = ['sex','prenyha','lv','emergenc','hc','sten.reg.mix','hs'] + cn_bin
        cn_num = ['age','grad','lvmi','ef','bsa','size','creat']
        di_cn = {'time':'time2'}
        self.df_rename(df, di_cn)
        # Remove rows with no change in information
        df['visit'] = df.groupby('num').cumcount() + 1
        df = df.reset_index(drop=True).rename_axis('idx').reset_index()
        tmp_df = df.melt(['idx','num','visit'],cn_num+cn_fac,'cn','val')
        tmp_df['val'] = tmp_df['val'].fillna('miss')
        tmp_df['lval'] = tmp_df.groupby(['num','cn'])['val'].shift(1)
        tmp_df = tmp_df.assign(lval=lambda x: np.where(x['lval'].isnull(),x['val'],x['lval']))
        tmp_df = tmp_df.assign(dd=lambda x: x['val'] != x['lval'])
        tmp_dd = tmp_df.groupby('idx')['dd'].any()
        idx_keep = tmp_dd[tmp_dd].index.values
        idx_keep = np.sort(np.append(idx_keep, tmp_df.query('visit == 1')['idx'].unique()))
        df = df[df['idx'].isin(idx_keep)]
        # (i) Create event, time, and id
        df = df.assign(time = lambda x: x.groupby('num')['time2'].shift(+1))
        df['time'] = df['time'].fillna(0)
        df = df.assign(time2=lambda x: np.where(x.groupby('num')['fuyrs'].shift(-1).isnull(), x['fuyrs'], x['time2']))
        # Status should only occur on the last value
        tmp_df = df.groupby('num')[['status','visit']].max().reset_index().rename(columns={'status':'event'})
        df = df.merge(tmp_df,'left')
        df['event'] = df['event'].fillna(0).astype(int)
        # (ii) Subset
        df = df[df['time2'] != 0]
        # (iii) Feature transform
        di_map = {'sex':{1:'F',0:'M'},'prenyha':{1:'I/II',3:'III/IV'}, 'lv':{1:'good', 2:'moderate', 3:'poor'}, 'emergenc':{0:'elective', 1:'urgent', 3:'emergency'}, 'hc':{0:'absent', 1:'treated',  2:'untreated'}, 'sten.reg.mix':{1:'stenosis', 2:'regurgitation', 3:'mixed'}}
        di_map = {**di_map, **{k:{1:'Y',0:'N'} for k in cn_bin}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time', 'time2', 'num')
        df = self.add_suffix(df, cn_num, cn_fac)
        # remove period from dataset
        fn = fn.replace('.','')
        return fn, df

    # --- (ii) epileptic --- #
    def process_epileptic(self, fn = 'epileptic'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        di_cn = {'time':'time2', 'with.time':'mtime'}
        cn_cens = ['with.status','with.status2','with.status.uae','with.status.isc']
        di_cens = dict(zip(cn_cens, [cn.split('.')[-1] for cn in cn_cens]))
        cn_cens = list(di_cens.values())
        di_cn = {**di_cn, **di_cens}
        self.df_rename(df, di_cn)
        cn_fac = ['treat', 'gender', 'learn.dis']
        cn_num = ['dose', 'age']
        # (i) Subset
        df['visit'] = df.groupby('id').cumcount()+1
        # dose is only variable with variations, only keep rows with change
        dat_shift = df.assign(ldose=lambda x: x.groupby('id')['dose'].shift(1))[['id','visit','dose','ldose']]
        dat_shift = dat_shift.query('dose != ldose & ldose.notnull()')[['id','visit']]
        tmp_df = df.groupby('id')['visit'].min().reset_index()
        dat_shift = pd.concat(objs=[tmp_df, dat_shift]).sort_values(['id','visit']).reset_index(drop=True)
        df = df.merge(dat_shift, 'inner')
        # (ii) Create event, time, and id
        df = df.assign(time = lambda x: x.groupby('id')['time2'].shift(+1).fillna(0).astype(int))
        df = df.assign(time2=lambda x: np.where(x.groupby('id')['mtime'].shift(-1).isnull(), x['mtime'], x['time2']))
        # Make visit == 0 as last visit
        df = df.merge(df.groupby('id').visit.max().reset_index(),'left','id')
        df = df.assign(visit=lambda x: x['visit_x']-x['visit_y']).drop(columns=['visit_x','visit_y'])
        # Status is fixed, set to last observation
        tmp_df = df.loc[df['visit'] == 0,['id','status','visit']].rename(columns={'status':'event'})
        df = df.merge(tmp_df,'left',['id','visit'])
        df['event'] = df['event'].fillna(0).astype(int)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time', 'time2', 'id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class jointCox(baseline):
    pkg_name = 'jointCox'
    # --- (i) dataOvarian1 --- #
    def process_dataOvarian1(self, fn = 'dataOvarian1'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['group','debulk']
        cn_num = list(df.columns[4:])
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 't.event')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class MASS(baseline):
    pkg_name = 'MASS'
    # --- (i) AIDS2 --- #
    def process_aids2(self, fn = 'Aids2'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['state','sex','T.categ']
        cn_num = ['age']
        # (i) Create event, time, and id
        df = df.assign(time=lambda x: x['death']-x['diag'])
        df['status'] = df['status'].map({'D':1, 'A':0}).astype(int)
        # (ii) Subset
        df = df.drop_duplicates()
        # (iii) Feature transform
        # (iv) Define Surv, and rename
        df = self.Surv(df, cn_num, cn_fac, cn_event='status', cn_time='time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


    # --- (ii) MELANOMA --- #
    def process_melanoma(self, fn = 'Melanoma'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex', 'ulcer']
        cn_num = ['age', 'year', 'thickness']
        # (i) Create event, time, and id
        df['status'] = np.where(df['status']==1, 1, 0)
        # (ii) Subset
        # (iii) Feature transform
        di_map = {'sex':{1:'M', 0:'F'}, 'ulcer':{1:'presence', 0:'absense'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='status', cn_time='time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class mlr3proba(baseline):
    pkg_name = 'mlr3proba'
    # --- (i) grace --- #
    def process_grace(self, fn = 'grace'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['revasc', 'stchange']
        cn_num = ['los', 'age', 'sysbp']
        # (iii) Feature transform
        di_map = {k:{1:'Yes',0:'No'} for k in ['revasc','stchange']}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'death', 'days')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (i) actg --- #
    def process_actg(self, fn = 'actg'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['tx', 'txgrp', 'strat2', 'sex', 'raceth', 'ivdrug', 'hemophil']
        cn_num = ['karnof', 'cd4', 'priorzdv', 'age']
        # (iii) Feature transform
        df[cn_fac] = df[cn_fac].astype(int)
        di_map = {'tx':{1:'IDV',0:'Control'}, 'txgrp':{1:'ZDV+3TC',2:'ZDV+3TC+IDV',3:'d4T+3TC',4:'d4T+3TC+IDV'}, 'sex':{0:'M',1:'F'}, 'strat2':{0:'CD4<=50',1:'CD4>50'}, 'raceth':{1:'White Non-Hispanic', 2:'Black Non-Hispanic', 3:'Hispanic', 4:'Asian, Pacific Islander', 5:'American Indian, Alaskan Native', 6:'Other/unknown'}, 'ivdrug':{1:'Never',2:'Currently',3:'Previously'}, 'hemophil':{1:'Y',0:'N'}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'censor', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class NestedCohort(baseline):
    pkg_name = 'NestedCohort'
    # --- (i) zinc --- #
    def process_zinc(self, fn = 'zinc'):
        df = load_rda(self.dir_process, '%s.RData' % fn)
        cn_fac = ['sex', 'agestr','dysp1','dysp2', 'smoke', 'drink', 'basehist','sevdysp','moddysp','mildysp','zincset',]        
        cn_num = ['agepill','stdagepill']
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='ec01', cn_time='futime01')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class pec(baseline):
    pkg_name = 'pec'
    # --- (i) Pbc3 --- #
    def process_Pbc3(self, fn = 'Pbc3'):
        path = os.path.join(self.dir_process, '%s.csv' % fn)
        df = pd.read_csv(path,sep=';')
        cn_fac = ['unit','tment','sex','stage','gibleed']
        cn_num = ['age','crea','alb','bili','alkph','asptr','weight']
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 2, 1, 0)  # Death
        # (iii) Feature transform
        di_map = {'unit':{1: 'Hvidovre', 2: 'London', 3: 'Copenhagen', 4: 'Barcelona', 5: 'Munich', 6: 'Lyon'}, 'tment':{0: 'placebo', 1: 'CyA'}, 'sex':{1:'M',0:'F'}, 'gibleed':{1: 'Y', 0: 'N'}}
        self.df_map(df, di_map)
        
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'days', cn_pid='ptno')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) cost --- #
    def process_cost(self, fn = 'cost'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex','hypTen','ihd','prevStroke','othDisease','alcohol','diabetes','smoke','atrialFib','hemor']
        cn_num = ['age','strokeScore','cholest']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) GBSG2 --- #
    def process_GBSG2(self, fn = 'GBSG2'):
        path = os.path.join(self.dir_process, '%s.csv' % fn)
        df = pd.read_csv(path,sep=';')
        cn_fac = ['horTh', 'menostat', 'tgrade']
        cn_num = ['age', 'tsize', 'pnodes', 'progrec', 'estrec']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'cens', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class penalized(baseline):
    pkg_name = 'penalized'
    # --- (i) nki70 --- #
    def process_nki70(self, fn = 'nki70'):
        df = load_rda(self.dir_process, '%s.RData' % fn)
        cn_fac = ['Diam', 'N', 'ER', 'Grade']
        cn_num = list(df.columns[6:])        
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class plsRcox(baseline):
    pkg_name = 'plsRcox'
    # --- (i) micro.censure --- #
    def process_microcensurei70(self, fn = 'micro.censure'):
        df = load_rda(self.dir_process, '%s.RData' % fn)
        cn_bin = list(df.columns[1:34])
        cn_fac = ['sexe', 'Siege', 'T','N','M','STADE'] + cn_bin
        cn_num = ['Agediag']
        # (iii) Feature transform
        df[cn_bin] = self.fill_fac(df[cn_bin])
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'DC', 'survyear')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class randomForestSRC(baseline):
    pkg_name = 'randomForestSRC'
    # --- (i) follic --- #
    def process_follic(self, fn = 'follic'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['clinstg', 'ch', 'rt']
        cn_num = ['age', 'hgb']
        # (iii) Feature transform
        di_map = {'clinstg':{1:'I',2:'II'}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) vdv --- #
    def process_vdv(self, fn = 'vdv'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = []
        cn_num = list(df.columns[2:])
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'Censoring', 'Time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class RCASPAR(baseline):
    pkg_name = 'RCASPAR'
    # --- (i) Bergamaschi --- #
    def process_Bergamaschi(self, fn = 'Bergamaschi'):
        # Combination of matrix of data and survival events
        dat = load_rda(self.dir_process, '%s.RData' % fn)
        dat = pd.DataFrame(dat.values, columns=dat.dim_1.values)
        df = load_rda(self.dir_process, 'survData.RData')
        df.reset_index(drop=True, inplace=True)
        cn_fac = []
        cn_num = list(dat.columns)
        cn_surv = ['censored', 'True_STs']
        df = pd.concat(objs=[df[cn_surv],dat],axis=1)
        # (i) Create event, time, and id
        df['event'] = np.where(df['censored'] == 0, 1, 0)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'True_STs')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class RcmdrPluginsurvival(baseline):
    pkg_name = 'RcmdrPluginsurvival'
    # --- (i) Dialysis --- #
    def process_Dialysis(self, fn = 'Dialysis'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['center', 'disease']
        cn_num = ['age', 'begin']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) Rossi --- #
    def process_Rossi(self, fn = 'Rossi'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        df = df.rename_axis('pid').reset_index()
        cn_fac = ['fin', 'race', 'wexp', 'mar', 'paro', 'prio', 'educ']
        cn_num = ['age']
        cn_emp = list(str_subset(df.columns,'^emp'))
        # (i) Turn into time-dependent format
        dat_mweek = df.groupby('pid')[['week','arrest']].max().reset_index()
        df_long = df.melt('pid',cn_emp,'week','emp')
        df_long = df_long.assign(week=lambda x: x['week'].str.replace('emp','').astype(int))
        df_long = df_long.assign(emp=lambda x: x['emp'].map({'no':0,'yes':1}))
        df_long = df_long.dropna().astype(int).sort_values(['pid','week']).reset_index(drop=True)
        # Keep first row
        df_long = df_long.assign(demp=lambda x: x.groupby('pid')['emp'].diff().fillna(1).astype(int))
        # Substract -1 since intervals are (start, stop]
        df_long = df_long.query('demp != 0').drop(columns='demp').rename(columns={'week':'start'}).assign(start=lambda x: x['start']-1)
        df_long = df_long.assign(stop=lambda x: x.groupby('pid')['start'].shift(-1))
        df_long = df_long.merge(dat_mweek)
        df_long = df_long.assign(stop=lambda x: np.where(x['stop'].isnull(),x['week'],x['stop']).astype(int))
        # Arrest should only occur on last week (if at all)
        df_long = df_long.assign(arrest=lambda x: np.where(x['stop']==x['week'],x['arrest'],0)).drop(columns='week')
        df = df_long.merge(df[['pid']+cn_fac+cn_num],'left','pid')
        # (iv) Define num, fac, and Surv
        cn_fac += ['emp']
        df = self.Surv(df, cn_num, cn_fac, 'arrest', 'start', 'stop', 'pid')
        df = self.add_suffix(df, cn_num, cn_fac)
        df.query('pid == 2').T
        return fn, df


class relsurv(baseline):
    pkg_name = 'relsurv'
    # --- (i) rdata --- #
    def process_rdata(self, fn = 'rdata'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex','agegr']
        cn_num = ['age','year']
        # (iii) Feature transform
        di_map = {'sex':{2:'F',1:'M'}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'cens', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class RISCA(baseline):
    pkg_name = 'RISCA'
    # --- (i) DIVAT1 --- #
    def process_DIVAT1(self, fn = 'dataDIVAT1'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        di_cn = {'z':'graft', 'trajectory':'traj'}
        self.df_rename(df, di_cn)
        cn_fac = ['sexR', 'graft', 'year.tx']
        cn_num = ['ageR', 'year.tx']
        # (i) Create event, time, and id
        df = df.assign(failure=lambda x: (~x['traj'].isin([1,12])).astype(int))
        df = df.assign(time=lambda x: np.where(x['traj'].isin([1,12,13,14]), x['time1'], x['time1']+x['time2'] ))
        # (iii) Feature transform
        di_map = {'graft':{0:'No',1:'Yes'}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'failure', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) DIVAT2 --- #
    def process_DIVAT2(self, fn = 'dataDIVAT2'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['hla', 'retransplant', 'ecd']
        cn_num = ['age']
        # (iii) Feature transform
        di_map = {'hla':{0:'otherwise',1:'high'}, 'retransplant':{0:'first',1:'>1'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'failures', 'times')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) DIVAT3 --- #
    def process_DIVAT3(self, fn = 'dataDIVAT3'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sexeR','year.tx','ante.diab','pra']
        cn_num = ['ageR','year.tx','ageD']
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        di_map = {'sexeR':{1:'M',0:'F'}, 'ante.diab':{1:'Yes',0:'No'}, 'pra':{1:'Detectable',0:'Undetectable'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'death', 'death.time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class RobustAFT(baseline):
    pkg_name = 'RobustAFT'
    # --- (i) Z243 --- #
    def process_Z243(self, fn = 'Z243'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['Sex', 'Adm', 'Ass', 'BBD', 'Charls']
        cn_num = ['Age', 'CouTot', 'BBD', 'Charls']
        # (iii) Feature transform
        di_map = {'Adm':{0:'Notification',1:'Emergency'},'Sex':{1:'M',0:'F'}, 'Ass':{0:'Usual',1:'Private',2:'Other'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'Death', 'LOS')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class rpart(baseline):
    pkg_name = 'rpart'
    # --- (i) stagec --- #
    def process_stagec(self, fn = 'stagec'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['ploidy', 'eet', 'grade', 'gleason']
        cn_num = ['age', 'g2', 'gleason']
        # (iii) Feature transform
        di_map = {'eet':{1:'No',2:'Yes'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'pgstat', 'pgtime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
    

class smcure(baseline):
    pkg_name = 'smcure'
    # --- (i) e1684 --- #
    def process_e1684(self, fn = 'e1684'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        df = df.dropna().reset_index(drop=True)
        df.columns = df.columns.str.lower()
        cn_fac = ['sex', 'trt']
        cn_num = ['age']
        # (iii) Feature transform
        di_map = {'sex':{0:'M', 1:'F'}, 'trt':{0:'Control',1:'IFN'}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'failcens', 'failtime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class smoothHR(baseline):
    pkg_name = 'smoothHR'
    # --- (i) whas500 --- #
    def process_whas500(self, fn = 'whas500'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['gender', 'cvd','afb','sho','chf','av3','miord','mitype','year']
        cn_num = ['age', 'hr', 'sysbp', 'diasbp', 'bmi','los','week']
        # (ii) Subset
        # Remove patients who died in the hospital (since we are using LOS as a feature)
        df = df[df['dstat'] == 0].reset_index(drop=True)
        # (iii) Feature transform
        di_map = {'gender':{0:'M',1:'F'}, 'year':{1:'1996-7',2:'1998-9',3:'2001'}}
        self.df_map(df, di_map)
        df = df.assign(admitdate = lambda x: pd.to_datetime(x['admitdate'],format='%d-%m-%Y'))
        df = df.assign(week = lambda x: x['admitdate'].dt.isocalendar()['week'])
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'fstat', 'lenfol')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
    

class spBayesSurv(baseline):
    pkg_name = 'spBayesSurv'
    # --- (i) LeukSurv --- #
    def process_LeukSurv(self, fn = 'LeukSurv'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex','district']
        cn_num = ['xcoord', 'ycoord','age','wbc','tpi']
        # (iii) Feature transform
        di_map = {'sex':{1:'M',0:'F'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'cens', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class survival(baseline):
    pkg_name = 'survival'
    # --- (i) cancer --- #
    def process_cancer(self, fn = 'cancer'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['inst', 'ph.ecog', 'sex']
        cn_num = ['wt.loss', 'ph.karno', 'pat.karno', 'meal.cal', 'age']
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 2, 1, 0)
        # (iii) Feature transform
        di_map = {'sex':{1:'M',2:'F'}}
        self.df_map(df, di_map)
        
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
        # (ii) Subset - covariate features do not change: time to first infection (or not)
        df = df.sort_values(['id','status'],ascending=False)
        df = df.groupby('id').head(1).sort_values('id').reset_index(drop=True)
        # (iii) Feature transform
        di_map = {'steroids':{0:'N', 1:'Y'}, 'propylac':{0:'N', 1:'Y'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'tstop')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) colon --- #
    def process_colon(self, fn = 'colon'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_bin = ['obstruct', 'perfor', 'adhere', 'node4']
        cn_fac = ['rx', 'sex', 'differ'] + cn_bin
        cn_num = ['age', 'nodes']
        # (ii) Subset
        df = df[df['etype'] == 2]  # Time to death
        df.drop(columns=['etype','study'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        # (iii) Feature transform
        di_map = {'sex':{1:'M',0:'F'}, 'surg':{1:'long',0:'short'}, 'differ':{1:'well', 2:'moderate', 3:'poor'}, 'extent':{1:'submucosa', 2:'muscle', 3:'serosa', 4:'contiguous structures'}}
        di_map = {**di_map, **{cn:{1:'Y',0:'N'} for cn in cn_bin}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
          # Fill missing factors
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time', cn_pid='id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


    # --- (iv) flchain --- #
    def process_flchain(self, fn = 'flchain'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex', 'chapter', 'sample.yr', 'mgus']
        cn_num = ['age', 'kappa', 'lambda', 'flc.grp', 'creatinine', 'sample.yr']
        # (i) Create event, time, and id
        # (ii) Subset
        # (iii) Feature transform
        di_map = {'mgus':{1:'Y',0:'N'}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
          # Fill missing factors
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'death', 'futime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (v) heart --- #
    def process_heart(self, fn = 'heart'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_num = ['age', 'year']
        cn_fac = ['surgery', 'transplant']
        # (iii) Feature transform
        df['transplant'] = df['transplant'].astype(int)
        di_map = {k:{1:'Y',0:'N'} for k in cn_fac}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'start', 'stop', 'id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


    # --- (vi) mgus --- #
    def process_mgus(self, fn = 'mgus'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_num = ['age', 'dxyr', 'pctime', 'alb', 'creat', 'hgb', 'mspike']
        'death'
        cn_fac = ['sex', 'pcdx']
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
          # Fill missing factors
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'death', 'futime', cn_pid='id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (vii) ovarian --- #
    def process_ovarian(self, fn = 'ovarian'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_num = ['age']
        cn_fac = ['resid.ds', 'rx', 'ecog.ps']
        # (iii) Feature transform
        di_map = {'resid.ds':{1:'N',2:'Y'}, 'rx':{1:'Grp1',2:'Grp2'}, 'ecog.ps':{1:'Better',2:'Worse'}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'fustat', 'futime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (viii) pbs --- #
    def process_pbc(self, fn = 'pbc'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_num = ['age']
        cn_bin = ['ascites', 'hepato', 'spiders']
        cn_fac = ['sex', 'trt'] + cn_bin
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 2, 1, 0)  # Death only
        # (ii) Subset
        df = df[df['trt'].notnull()]  # RCT only
        # (iii) Feature transform
        di_map = {'trt':{1:'D-penicillmain', 2:'Placebo'}, 'edema':{0:'none', 0.5:'successful', 1:'unsuccessful'}}
        tmp = {k:{1:'Y',0:'N'} for k in cn_bin}
        di_map = {**di_map, **tmp}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time', cn_pid='id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ix) retinopathy --- #
    def process_retinopathy(self, fn = 'retinopathy'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_num = ['age', 'risk']
        cn_fac = ['laser', 'eye', 'type', 'trt', 'risk']
        # (iii) Feature transform
        di_map = {'trt':{1:'Treatment',0:'Control'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'futime', cn_pid='id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (x) retinopathy --- #
    def process_veteran(self, fn = 'veteran'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        df.loc['1']
        cn_num = ['karno', 'diagtime', 'age']
        cn_fac = ['trt', 'celltype', 'prior']
        # (iii) Feature transform
        di_map = {'trt':{1:'standard',2:'test'}, 'prior':{0:'N', 10:'Y'}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


    # --- (xi) nwtco --- #
    def process_nwtco(self, fn = 'nwtco'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_num = ['age', 'stage']
        cn_bin = ['instit','histol']
        cn_fac = ['stage', 'study', 'in.subcohort'] + cn_bin
        # (iii) Feature transform
        di_map = {k:{1:'Favourable',2:'Unfavourable'} for k in cn_bin}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'rel', 'edrel', cn_pid='seqno')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class survJamdadata(baseline):
    pkg_name = 'survJamdadata'
    # --- (i) gse4335 --- #
    def process_gse4335(self, fn = 'gse4335'):
        expr = load_rda(self.dir_process, '%s.rda' % fn)
        df = load_rda(self.dir_process, '%spheno.rda' % fn)
        df.reset_index(drop=True, inplace=True)
        # Clean up column names
        cn_old = ['Array_ID','Overall_survival_.months.','X.Status_0.A._1.AWD._2.DOD._3.DOC.','Age_at_diagnosis','X._ER_status_.0.neg._1.pos..','T_.tumor_size.','N_.node_status.','M_.metastasis.','Grade','Histology']
        cn_new = ['pid','time','event','age','er_status','tumor_size','node_status','metastasis','grade', 'histology']
        di_cn = dict(zip(cn_old, cn_new))
        self.df_rename(df, di_cn)
        df = df[cn_new]
        cn_fac = ['er_status', 'node_status', 'metastasis','histology','tumor_size','grade']
        cn_num = ['age','grade'] + list(expr.columns)
        expr = expr.rename_axis('pid').reset_index()
        df = df.merge(expr)
        # (iii) Feature transform
        
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time', cn_pid='pid')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    def process_gse1992(self, fn = 'gse1992'):
        expr = load_rda(self.dir_process, '%s.rda' % fn)
        df = load_rda(self.dir_process, '%spheno.rda' % fn)
        df.reset_index(drop=True, inplace=True)
        # Clean up column names
        cn_old = ['GEO_array_names','Age','ER_.1.positive.0.negative.','Node_status.1.positive.1_or_more_nodes..0.negative.', 'Grade','Size', 'RFS_event.0.no_relapse.1.relapsed_at_any_site_or_died_of_disease.','RFS_months', 'Overall_Survival_Event.0.alive.1.DOD_or_DOC.','Overall_suvival_months']
        cn_new = ['pid','age','er_positive','node_status','grade','size','rfs_event','rfs_months','surv_event','suv_months']
        di_cn = dict(zip(cn_old, cn_new))
        self.df_rename(df, di_cn)
        df = df[cn_new]
        cn_fac = ['er_positive', 'node_status', 'grade','size']
        cn_num = ['age','size'] + list(expr.columns)
        expr = expr.rename_axis('pid').reset_index()
        df = df.merge(expr)
        # (iii) Feature transform
        
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'rfs_event', 'rfs_months', cn_pid='pid')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    def process_gse3143(self, fn = 'gse3143'):
        expr = load_rda(self.dir_process, '%s.rda' % fn)
        df = load_rda(self.dir_process, '%spheno.rda' % fn)
        df.reset_index(drop=True, inplace=True)
        di_cn = {'TTBNO':'pid', 'ERlev':'erlev', 'Status(0=alive or 1=dead)':'status','SurvivalTime(months)':'time'}
        self.df_rename(df, di_cn)
        cn_fac = ['erlev']
        cn_num = ['erlev'] + list(expr.columns)
        expr = expr.rename_axis('pid').reset_index()
        df = df.merge(expr)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time', cn_pid='pid')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class THdata(baseline):
    pkg_name = 'THdata'
    # --- (i) wpbc --- #
    def process_wpbc(self, fn = 'wpbc'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = []
        cn_num = list(df.columns[2:])
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 'R', 1, 0)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


class timereg(baseline):
    pkg_name = 'timereg'
    # --- (i) TRACE --- #
    def process_TRACE(self, fn = 'TRACE'):
        path = os.path.join(self.dir_process, '%s.txt' % fn)
        df = pd.read_csv(path,sep='\\s',engine='python')
        df.columns = df.columns.str.replace('\\"','',regex=True)
        cn_bin = ['chf','diabetes','vf']
        cn_fac = ['sex'] + cn_bin
        cn_num = ['wmi','age']
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 9, 1, 0)
        # (iii) Feature transform
        di_map = {'sex':{1:'F',0:'M'}}
        di_map = {**di_map,**{k:{1:'present',0:'absent'} for k in cn_bin}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) csl --- #
    def process_csl(self, fn = 'csl'):
        path = os.path.join(self.dir_process, '%s.txt' % fn)
        df = pd.read_csv(path,sep='\\s',engine='python')
        df.columns = df.columns.str.replace('\\"','',regex=True)
        cn_fac = ['sex','treat']
        cn_num = ['age','prot','prot.prev','prot.base']
        # (i) Create event, time, and id
        df['visit'] = df.groupby('id').cumcount()+1
        dat_visit = df.groupby('id')[['visit','dc','eventT']].max().reset_index()
        df.drop(columns=['dc','eventT','time'],inplace=True)
        df = dat_visit.merge(df,'right',['id','visit'])
        df['dc'] = df['dc'].fillna(0).astype(int)
        df = df.assign(rt=lambda x: np.where(x['eventT'].notnull(),x['eventT'],x['rt']))
        # (iii) Feature transform
        di_map = {'sex':{0:'F',1:'M'},'treat':{0:'prednisone',1:'placebo'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'dc', 'lt', 'rt', 'id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) diabetes --- #
    def process_diabetes(self, fn = 'diabetes'):
        path = os.path.join(self.dir_process, '%s.txt' % fn)
        df = pd.read_csv(path,sep='\\s',engine='python')
        df.columns = df.columns.str.replace('\\"','',regex=True)
        cn_num = ['agedx']
        cn_fac = ['trteye', 'treat', 'adult']
        # df.reset_index(drop=True, inplace=True)
        # (iii) Feature transform
        di_map = {'trteye':{1:'left',2:'right'},'treat':{1:'treated',0:'untreated'},'adult':{1:'<20',2:'>20'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time', cn_pid='id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
