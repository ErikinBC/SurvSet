# Process coin datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i)  --- #
    def process_glioma(self, fn = 'glioma'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex', 'histology', 'group']
        cn_num = ['age']
        # (i) Create event, time, and id
        df['event'] = df['event'].astype(int)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

