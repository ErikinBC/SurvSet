# Baseline class to be used by all package processing scripts
import os

class baseline():
    def __init__(self, pkg, dir_pkgs, dir_output, cn_surv, cn_surv2):
        self.dir_process = os.path.join(dir_pkgs, pkg, 'data')
        self.dir_output = dir_output
        self.cn_surv = cn_surv
        self.cn_surv2 = cn_surv2

