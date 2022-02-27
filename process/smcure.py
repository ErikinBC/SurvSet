# Process smcure datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
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
