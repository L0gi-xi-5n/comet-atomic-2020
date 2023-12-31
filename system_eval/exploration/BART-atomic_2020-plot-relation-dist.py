import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_json('../BART/BART-atomic_2020.json', lines=True)

with sns.axes_style('white'):
    g=sns.catplot(y="relation", data=df, aspect=2, kind="count", 
                    color='steelblue', order=df['relation'].value_counts().index)
    g.set_xticklabels()
    g.set_ylabels("")

    ax=g.facet_axis(0,0)
    ax.set_xlim(1,455)
    for c in ax.containers:
        labels = [' {}'.format(round(v.get_width()), '') for v in c]
        ax.bar_label(c, labels=labels, label_type='edge')

plt.savefig("plots/relation_dist_latex.svg", dpi=1200)