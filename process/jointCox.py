# Process jointCox datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
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
