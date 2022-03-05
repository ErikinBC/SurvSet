# Process the Survival package
import numpy as np
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
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

