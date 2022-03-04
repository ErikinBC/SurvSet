# Process relsurv datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
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
