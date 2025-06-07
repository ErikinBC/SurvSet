"""
Module to generate the dataset for the SurvSet project.

python3 -m SurvSet._datagen
"""

def main():
    # Internal modules
    from . import di_argpase_defaults
    from .utils.utils import get_args
    from . import dir_custom
    # Script modules
    from .download_pkgs import download_pkgs
    from .download_custom import download_custom
    from .process_datasets import process_datasets
    from .qc_check import qc_check
    # Set up the default arguments
    args = get_args(di_argpase_defaults, description='SurvSet data generation pipeline')

    # (i) Download R package data
    download_pkgs()

    # (ii) Download website specific data
    download_custom(fold_custom = dir_custom,)

    # (iii) Loop through package-specific scripts
    process_datasets(allow_overwrite = args.allow_overwrite,)

    # (iv) Do QC checks on output files
    qc_check(min_num = args.min_num,)

    print('End of the data generation pipeline')


if __name__ == '__main__':
    # Call the main module
    main()
    print('~~~ The SurvSet._datagen module was successfully executed ~~~')