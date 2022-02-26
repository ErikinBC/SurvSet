# Process AdapEnetClass datasets
from funs_class import baseline
from funs_support import load_rda, str_subset

class package(baseline):
    # --- (i) MCLcleaned --- #
    def process_MCLcleaned(self, fn = 'MCLcleaned'):
        df = load_rda(self.dir_process, '%s.RData' % fn)
        cn_fac = []
        cn_num = list(str_subset(df.columns,'^X'))
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'cens', 'time', cn_pid='ID')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
