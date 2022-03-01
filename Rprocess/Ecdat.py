# Process Ecdat datasets
from funs_class import baseline
from funs_support import load_rda, str_subset

class package(baseline):
    # --- (i) UnempDur --- #
    def process_UnempDur(self, fn = 'UnempDur'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['ui']
        cn_num = ['age','reprate','disrate','tenure','logwage',]
        # (i) Create event, time, and id
        cn_censor = str_subset(df.columns, '^censor')
        cn_censor3 = str_subset(cn_censor, 'censor[1-3]')
        df['event'] = df[cn_censor3].sum(1)
        # (ii) Subset
        df = df[df[cn_censor].sum(1) == 1]
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'spell')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) Unemployment --- #
    def process_Unemployment(self, fn = 'Unemployment'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        # not using ftp to prevent information leakage
        cn_fac = ['race', 'sex', 'reason', 'search', 'pubemp']
        cn_num = []
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'spell', 'duration')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


