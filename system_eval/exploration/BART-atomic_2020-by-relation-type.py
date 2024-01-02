import os
import pandas as pd

os.chdir("partition-by-relation")

df=pd.read_json('../../BART/BART-atomic_2020.json', lines=True)

grouped_by_relation = df.groupby(df.relation) 
for relation in set(grouped_by_relation.keys):
    outfile_path = os.path.join(os.path.basename(relation).split('.')[0] + ".json")
    outfile = open(outfile_path, 'w')
    grouped_by_relation.get_group(relation).apply(lambda row: outfile.write(row.to_json() + "\n"), axis=1)

