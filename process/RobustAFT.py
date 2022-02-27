# Process RobustAFT datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) Z243 --- #
    def process_Z243(self, fn = 'Z243'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['Sex', 'Adm', 'Ass', 'BBD', 'Charls']
        cn_num = ['Age', 'CouTot', 'BBD', 'Charls']
        # (iii) Feature transform
        di_map = {'Adm':{0:'Notification',1:'Emergency'},'Sex':{1:'M',0:'F'}, 'Ass':{0:'Usual',1:'Private',2:'Other'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'Death', 'LOS')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


