import glob

import pandas as pd


df_ss = pd.read_table("sample.tsv").set_index("sample_name", drop=False)
