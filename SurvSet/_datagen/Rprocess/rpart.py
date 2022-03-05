# Process rpart datasets
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) stagec --- #
    def process_stagec(self, fn = 'stagec'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['ploidy', 'eet', 'grade', 'gleason']
        cn_num = ['age', 'g2', 'gleason']
        # (iii) Feature transform
        di_map = {'eet':{1:'No',2:'Yes'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'pgstat', 'pgtime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

# import os
# cn_surv = ['pid', 'time', 'event']
# cn_surv2 = ['pid', 'time', 'time2', 'event']
# dir_base = os.getcwd()
# dir_datagen = os.path.join(dir_base, 'SurvSet', '_datagen')
# dir_output = os.path.join(dir_datagen, 'output')
# dir_pkgs = os.path.join(dir_datagen, 'pkgs')
# self = package(pkg='rpart', dir_pkgs=dir_pkgs, dir_output=dir_output, cn_surv=cn_surv, cn_surv2=cn_surv2)
# self.run_all()