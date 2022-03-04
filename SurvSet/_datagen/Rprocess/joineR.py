# Process joineR datasets
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
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



