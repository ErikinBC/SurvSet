from SurvSet.data import SurvLoader

enc = SurvLoader()
print(enc.df_ds)
print(enc.load_dataset('ova'))
print(enc.load_dataset('jazz'))