import sys
import os.path as op
from glob import glob
from pathlib import Path
from gofer.ok import grade_notebook
import json

def gofer_wrangle(res):
    # unique-ify the score based on path
    path_to_score = {}
    total_score = 0
    for r in res:
        key = r.paths[0].replace('.py', '')
        if key not in path_to_score:
            total_score += r.grade
        path_to_score[key] = r.grade
    okpy_result = {"total": total_score,
                   "msg": "\n".join(repr(r) for r in res)}
    return okpy_result, path_to_score

def gradeNotebook(nb_path):
    tests = glob(op.join(op.dirname(nb_path), 'tests', 'q*.py'))
    r, s = gofer_wrangle(grade_notebook(nb_path, tests))
    return r, s
