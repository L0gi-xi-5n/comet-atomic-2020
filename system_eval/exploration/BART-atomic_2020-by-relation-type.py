import os
import sys
import pandas as pd
from tabulate import tabulate

sys.path.append("../system_eval")
from system_eval.automatic_eval_exploration import eval_partition

in_file_name = os.path.join("BART", "BART-atomic_2020.json")
out_dir_name = os.path.join("exploration", "partition-by-relation")

def create_dir(dir_name):
    out_dir = os.path.dirname(os.path.join(os.getcwd(), dir_name) + os.path.sep)
    out_dir_exists = os.path.exists(out_dir)
    if not out_dir_exists:
        print("Creating " + out_dir_name)
        os.makedirs(out_dir)
    else:
        print("Output directory already exists")

def empty_dir(dir_name):
    for file_name in os.listdir(dir_name):
        file_path = os.path.join(dir_name, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))

def partition_by_relation(data):
    grouped_by_relation = data.groupby(data.relation) 
    for relation in set(grouped_by_relation.keys):
        outfile_path = os.path.join(out_dir_name, os.path.basename(relation).split('.')[0] + ".json")
        outfile = open(outfile_path, 'w')
        grouped_by_relation.get_group(relation).apply(lambda row: outfile.write(row.to_json() + "\n"), axis=1)


create_dir(out_dir_name)
empty_dir(out_dir_name)

df = pd.read_json(in_file_name, lines=True)
partition_by_relation(df)

scores_per_relation = {}
input_files = os.listdir(out_dir_name)
for file_name in input_files:
    evaluated = os.path.join("exploration", "partition-by-relation", file_name)
    evaluation = eval_partition(evaluated)
    scores_per_relation.update({file_name.split('.')[0] : evaluation[0]['scores']})

all_scores = pd.DataFrame(scores_per_relation)    
print(tabulate(all_scores.T, tablefmt='tsv', floatfmt='#.3f', headers="keys"))