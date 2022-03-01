# Process JM datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
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

