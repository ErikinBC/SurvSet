# Process MASS data

import os
import rdata
import numpy as np
import pandas as pd

# Set directory
dir_base = os.getcwd()
dir_pkgs = os.path.join(dir_base, 'pkgs')
dir_process = os.path.join(dir_pkgs, 'MASS', 'data')

#####################
# --- (i) AIDS2 --- #

#  Ripley, B.D., Solomon, P.J. (1994). A note on Australian AIDS survival, University of Adelaide Department of Statistics Research Report 94/3

parsed = rdata.parser.parse_file(os.path.join(dir_process, "Aids2.rda"))
converted = rdata.conversion.convert(parsed)
df_aids2 = converted['Aids2']


np.sort(os.listdir(dir_process))
rdata


#########################
# --- (ii) MELANOMA --- #



# Drzewiecki, K.T., Ladefoged, C., and Christensen, H.E. (1980), Biopsy and prognosis for cutaneous malignant melanoma in clinical stage I. Scand. J. Plast. Reconstru. Surg. 14, 141-144. 

# Drzewiecki, K.T., Poulsen, H., Vibe, P., Ladefoged, C., Andersen, P.K.  (1984). Melanoma in Denmark: Experience at the University Hospital in Odense. Pp. 461-468 in Cutaneous Melanoma. Clinical Management and Treatment Results Worldwide. (eds. C.M. Balch, G.W. Milton).  Lippincott, Philadelphia. 

