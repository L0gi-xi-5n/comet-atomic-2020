import os
import sys
import pandas as pd
from tabulate import tabulate

sys.path.append("../system_eval")
from system_eval.automatic_eval_exploration import eval_partition

in_file_name = os.path.join("BART", "BART-atomic_2020.json")
out_dir_name = os.path.join("exploration", "partition-by-head-token-length")

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

def partition_by_head_token_length(data):
    partition = {
        "onetoken":           data[[1 == len(head.split())  for head in data['head']]], 
        "twothreetokens":     data[[1  < len(head.split()) < 4 for head in data['head']]],
        "fourfivetokens":     data[[3  < len(head.split()) < 6 for head in data['head']]],
        "sixseventokens":     data[[5  < len(head.split()) < 8 for head in data['head']]],
        "eightninetokens":    data[[7  < len(head.split()) < 10 for head in data['head']]],
        "remainder": data[[9  < len(head.split()) for head in data['head']]]
    }
    for part in partition.keys():
        outfile_path = os.path.join(out_dir_name, os.path.basename(part).split('.')[0] + ".json")
        outfile = open(outfile_path, 'w')
        partition[part].apply(lambda row: outfile.write(row.to_json() + "\n"), axis=1)


create_dir(out_dir_name)
empty_dir(out_dir_name)

df = pd.read_json(in_file_name, lines=True)
partition_by_head_token_length(df)

scores_per_head_token_length = {}

order = [
    "onetoken",
    "twothreetokens",
    "fourfivetokens",
    "sixseventokens",
    "eightninetokens",
    "remainder"
]

input_files = os.listdir(out_dir_name)

if not len(input_files) == len(order):
    sys.exit("Mismatch between expected order and available input files!!")

for file_name in order:
    evaluated = os.path.join("exploration", "partition-by-head-token-length", file_name + ".json")
    evaluation = eval_partition(evaluated)
    scores_per_head_token_length.update({file_name.split('.')[0] : evaluation[0]['scores']})

all_scores = pd.DataFrame(scores_per_head_token_length)    
print(tabulate(all_scores.T, tablefmt='tsv', floatfmt='#.3f', headers="keys"))
print(tabulate(all_scores.T, tablefmt='latex', floatfmt='#.3f', headers="keys"))