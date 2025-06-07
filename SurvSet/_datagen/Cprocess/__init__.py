"""
Contains the name of the classes, and their respective process functions and file names
"""

# Load the processing classes
from .datasets import hosmer, openml, princeton, Reddy, vanderbilt


# Store in a dict
di_Cprocess = {
    hosmer: [
        ('process_uis','uis'),
        ('process_FRTCS','FRTCS')
    ],
    openml: [
        ('process_phpl04K8a','phpl04K8a')
    ],
    princeton: [
        ('process_divorce','divorce')
    ],
    Reddy: [
        ('process_NSBCD','NSBCD'),
        ('process_AMLBull','AML_Bull'),
        ('process_DBCD','DBCD'),
        ('process_DLBCL','DLBCL')
    ],
    vanderbilt: [
        ('process_support2','support2'),
        ('process_prostate','prostate'),
        ('process_Framingham','Framingham'),
        ('process_rhc','rhc'),
        ('process_acath','acath'),
        ('process_vlbw','vlbw')
    ],
}
