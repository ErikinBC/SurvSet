# Process survJamda.data datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
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

