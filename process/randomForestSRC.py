# Process randomForestSRC datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
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


