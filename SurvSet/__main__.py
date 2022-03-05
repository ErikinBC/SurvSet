# __main__

import pandas as pd
from SurvSet.data import SurvLoader

def main():
    # (i) Check class
    enc = SurvLoader()
    assert hasattr(enc, 'df_ds'), 'SurvLoader() should has a "df_ds" attribute!'
    print('(i) class check complete')
    # (ii) Check dataset loader
    try:
        di = enc.load_dataset('ova')
    except:
        di = None
    assert di is not None, 'This should be a valid dataset!'
    assert isinstance(di, dict), 'di should be a dict!'
    assert 'df' in di, 'df should be a key in di'
    assert 'ref' in di, 'ref should be a key in di'
    assert isinstance(di['df'], pd.DataFrame), 'di["df"] should be a DataFrame!'
    assert isinstance(di['ref'], str), 'di["ref"] should be a string!'
    print('(ii) valid dataset loader complete')
    # (iii) Check non-existent dataset through error
    try:
        di = enc.load_dataset('madeup')
    except:
        di = None
    assert di is None, '"madeup" should not have returned a result!'
    print('(iii) invalid dataset check complete')

if __name__ == '__main__':
    main()
    print('~~~ The SurvSet package was successfully compiled ~~~')
