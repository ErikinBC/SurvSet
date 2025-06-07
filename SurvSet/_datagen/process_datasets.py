"""
This script processes datasets by running R and custom processing scripts.

# Call manually (default is to overwrite existing files):
>>> python3 -m SurvSet._datagen.process_datasets
# Prevent overwriting existing files:
>>> python3 -m SurvSet._datagen.process_datasets --allow_overwrite
"""

def process_datasets(
        allow_overwrite: bool,
) -> None:

    # Load internal modules
    from .Rprocess import di_Rprocess
    from .Cprocess import di_Cprocess
    from .utils.funs_support import has_argument
    from . import dir_pickles, dir_custom, dir_pkgs


    ################################
    # --- (1) PARAMETER SET UP --- #

    # (ii) Baseline columns for all datasets
    cn_surv = ['pid', 'event', 'time']
    cn_surv2 = ['pid', 'event', 'time', 'time2']

    # (iii) Default arguments for R processing
    di_Rprocess_defaults = {
        'dir_pickles': dir_pickles,
        'cn_surv': cn_surv,
        'cn_surv2': cn_surv2,
        'pkg': None,  # This will be set in the loop
        'dir_pkgs': dir_pkgs,
        'dir_custom': None,
    }
    
    # (iv) Default arguments for custom processing
    di_Cprocess_defaults = {
        'dir_pickles': dir_pickles,
        'cn_surv': cn_surv,
        'cn_surv2': cn_surv2,
        'dir_custom': dir_custom,
        'pkg': None,  
        'dir_pkgs': None,
    }

    
    ####################################
    # --- (2) PACKAGE PROCESSING --- #
    
    # (i) Combine the processors and efaults
    di_processors = {**di_Rprocess, **di_Cprocess}
    di_processor_defaults = {'Rprocess': di_Rprocess_defaults.copy(),
                   'Cprocess': di_Cprocess_defaults.copy()}

    # (ii) Loop over all the class/methods
    for i, (package_processor, dataset_funs) in enumerate(di_processors.items()):
        source = package_processor.__module__.split('.')[2]
        process_name = package_processor.__name__
        assert source in di_processor_defaults, f'Processor {process_name} must be in Rprocess or Cprocess!'
        print(f'--- Processing package: {process_name} ({i+1} of {len(di_processors)}) ---')
        # Update the default arguments with the current package
        di_defaults = di_processor_defaults[source].copy()
        if source == 'Rprocess':
            di_defaults['pkg'] = package_processor.pkg_name
        constructed_processor = package_processor(**di_defaults)
        # Loop through the process functions
        for process_fn in dataset_funs:
            # Extract the function name and argument name and check if it has the 'fn' argument
            process_fun_name = process_fn[0]
            fn_arg_name = process_fn[1]
            process_method = getattr(constructed_processor, process_fun_name)
            assert has_argument(process_method, 'fn'), \
                f'Function {process_fun_name} does not have a "fn" argument!'
            # Call the processing function
            print(f'Processing dataset: {fn_arg_name}')
            fn, df = process_method(fn = fn_arg_name,)
            # Check that the factors are all categorical and have no missing values
            df = constructed_processor.check_num_fac(df=df)
            # Ensure categorical dtype commonality (default to str if mixed)
            df = constructed_processor.ensure_categorical_commonality(df=df)
            # Force the labels to the expected format
            df = constructed_processor.check_labels(df=df)
            # Save file (potentially)
            constructed_processor.write_pickle(fn=fn, df=df, allow_overwrite=allow_overwrite)


    print('~~~ End of process_datasets.py ~~~')


if __name__ == '__main__':
    # Import the default argument parser
    from . import di_argpase_defaults
    # Set up the default arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--allow_overwrite', help=di_argpase_defaults['allow_overwrite']['help'], default=di_argpase_defaults['allow_overwrite']['val'], action='store_true')
    args = parser.parse_args()

    # Call the main function
    process_datasets(allow_overwrite=args.allow_overwrite,)

