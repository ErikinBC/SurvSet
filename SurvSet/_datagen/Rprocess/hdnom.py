# Process hdnom datasets
import numpy as np
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) smart --- #
    def process_smarto(self, fn = 'smarto'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        df.columns = df.columns.str.lower()
        cn_fac = ['sex', 'diabetes', 'cerebral', 'aaa', 'periph', 'stenosis', 'albumin', 'smoking', 'alcohol']
        cn_num = ['age', 'systbp', 'diastbp', 'systh', 'diasth', 'length', 'weight', 'bmi', 'chol', 'hdl', 'ldl', 'trig', 'homoc', 'glut', 'creat', 'imt', 'packyrs']
        # (ii) Subset
        # (iii) Feature transform
        
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'tevent')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df



