# Process CoxRidge datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) ova --- #
    def process_ova(self, fn = 'ova'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['karn', 'diam', 'figo']
        cn_num = ['karn', 'diam']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='death', cn_time='time', cn_pid='x')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df