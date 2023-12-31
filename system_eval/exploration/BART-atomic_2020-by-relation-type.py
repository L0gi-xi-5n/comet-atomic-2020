import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

from LaTeX_utils import set_size


df=pd.read_json('../BART/BART-atomic_2020.json', lines=True)

#grouped_by_relation=df.groupby(df.relation)
#df_new=grouped_by_relation.get_group("xNeed")

#plt.style.use(style=seaborn)
width=345

tex_fonts={
    # Use LaTeX to write all text
    "text.usetex": True,
    "font.family": "serif",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 10,
    "font.size": 10,
    # Make the legend/label fonts a little smaller
    #"legend.fontsize": 8,
    #"xtick.labelsize": 8,
    #"ytick.labelsize": 8
}
plt.rcParams.update(tex_fonts)


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
    g.figure.set_size_inches(set_size(width))

fig, ax = plt.subplots()
fig.savefig("relation_dist_latex.svg", format='svg', dpi=1200)
    



#plt.show()