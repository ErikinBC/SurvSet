import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--fold_custom', help='Name of the folder where the custom datasets will be downloaded to (default="pkgs"', default='custom')
args = parser.parse_args()
fold_custom = args.fold_custom

# fold_custom='custom'

# Load modules
import os
from funs_support import makeifnot, download_csv, download_zip

# Folder to write into
dir_base = os.getcwd()
dir_custom = os.path.join(dir_base, fold_custom)
makeifnot(dir_custom)


# --- (1) Employee Attrition --- #
url = 'https://raw.githubusercontent.com/IBM/employee-attrition-aif360/master/data/emp_attrition.csv'
download_csv(url, dir_custom)

# --- (2) Lung Cancer --- #
# https://www.openml.org/d/1245
url = 'https://www.openml.org/data/get_csv/552598/phpl04K8a'
download_csv(url, dir_custom)

# --- (3) Reddy Datasets --- #
url = 'https://dmkd.cs.vt.edu/projects/survival/data/Gene_expression_data.zip'
download_zip(url, dir_custom)

# AML_Bull
# https://pubmed.ncbi.nlm.nih.gov/15084693/

# DLBCL
# https://pubmed.ncbi.nlm.nih.gov/12075054/

# ------

# The Norway/Stanford breast cancer data (NSBCD) [24]
# contains gene expression measurements of 115 women with
# breast cancer.

# T. Sørlie, R. Tibshirani, J. Parker, T. Hastie,
# J. Marron, A. Nobel, S. Deng, H. Johnsen, R. Pesich,
# S. Geisler, et al. Repeated observation of breast tumor
# subtypes in independent gene expression data sets.
# Proceedings of the National Academy of Sciences,
# 100(14):8418–8423, 2003.

# -------------------

# The Dutch Breast Cancer Data (DBCD) from van Houwelin-
# gen et al.

# H. C. van Houwelingen, T. Bruinsma, A. A. Hart,
# L. J. van’t Veer, and L. F. Wessels. Cross-validated
# cox regression on microarray gene expression data.
# Statistics in medicine, 25(18):3201–3216, 2006

# ----------------------------------

# Van de Vijver’s Microarray Breast Cancer data (VDV)
# [29] contains gene expression profile information which can
# be used for predicting the clinical outcome of breast can-
# cer. I

# L. J. van’t Veer, H. Dai, M. J. Van De Vijver, Y. D.
# He, A. A. Hart, M. Mao, H. L. Peterse, K. van der
# Kooy, M. J. Marton, A. T. Witteveen, et al. Gene
# expression profiling predicts clinical outcome of breast
# cancer. Nature, 415(6871):530–536, 2002
# ----------------



# Note sure where the Chandan Reddy datasets are coming from: https://dmkd.cs.vt.edu/TUTORIAL/Survival/index.htm

