from typing import Iterable, Dict
import gzip
import json
import os

COV_EVAL = os.path.join("dataset", "data")

def read_problems(evalset_file: str = COV_EVAL) -> Dict[str, Dict]:
    problem_dict = {}
    json_files = find_json_files(COV_EVAL)
    for json_file in json_files:
        with open(json_file, 'r') as f:
            task = json.load(f)
            
        problem_dict[task['problem_id']] = task

    return problem_dict


def find_json_files(directory):
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


