import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

from LaTeX_utils import set_size


df=pd.read_json('../BART/BART-atomic_2020.json', lines=True)

grouped_by_relation=df.groupby(df.relation)
df_new=grouped_by_relation.get_group("xNeed")

