# Process plsRcox datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) micro.censure --- #
    def process_microcensurei70(self, fn = 'micro.censure'):
        df = load_rda(self.dir_process, '%s.RData' % fn)
        cn_bin = list(df.columns[1:34])
        cn_fac = ['sexe', 'Siege', 'T','N','M','STADE'] + cn_bin
        cn_num = ['Agediag']
        # (iii) Feature transform
        df[cn_bin] = self.fill_fac(df[cn_bin])
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'DC', 'survyear')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
