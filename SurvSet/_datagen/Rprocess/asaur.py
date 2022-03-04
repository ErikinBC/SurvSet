# Process asaur datasets
import numpy as np
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) hepatoCellular --- #
    def process_hepatoCellular(self, fn = 'hepatoCellular'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = list(df.columns[2:15])
        cn_num = ['Age'] + list(df.columns[19:])
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='Death', cn_time='OS')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) pharmacoSmoking --- #
    def process_pharmacoSmoking(self, fn = 'pharmacoSmoking'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['grp', 'gender', 'race', 'employment', 'levelSmoking', 'ageGroup2', 'ageGroup4']
        cn_num = ['age', 'yearsSmoking', 'priorAttempts', 'longestNoSmoke']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='relapse', cn_time='ttr', cn_pid='id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) prostateSurvival --- #
    def process_prostateSurvival(self, fn = 'prostateSurvival'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['grade', 'stage', 'ageGroup']
        cn_num = []
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 1, 1, 0)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='status', cn_time='survTime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

