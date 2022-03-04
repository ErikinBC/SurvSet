# Process EHA datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) scania --- #
    def process_scania(self, fn = 'scania'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex', 'parish', 'ses', 'immigrant']
        cn_num = ['birthdate']
        # (i) Create event, time, and id
        df = df.assign(time=lambda x: x['exit']-x['enter'])
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time', cn_pid='id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) oldmort --- #
    def process_oldmort(self, fn = 'oldmort'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex','civ','ses.50','birthplace', 'region']
        cn_num = ['birthdate','imr.birth']
        # (i) Create event, time, and id
        df['event'] = df['event'].astype(int)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'enter', 'exit', 'id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
