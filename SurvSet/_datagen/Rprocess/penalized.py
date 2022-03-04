# Process penalized datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
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
