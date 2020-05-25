import boto3
from pprint import pprint
from ci import get_ci, get_mos
import xmltodict
import numpy as np
import json

#pprint(mturk.list_hits())
#exit()
# You will need the following library
# to help parse the XML answers supplied from MTurk
# Install it in your local environment with
# pip install xmltodict
# Use the hit_id previously created
#hit_id = '3MVY4USGB6GWVM0U779VQCTHN5XISC'

def get_answers(hit_id):
    paginator = mturk.get_paginator('list_assignments_for_hit')
    response_iterator = paginator.paginate(
        HITId=hit_id,
        AssignmentStatuses=['Submitted', 'Approved'],
        PaginationConfig={
            'MaxItems': 500,
            'PageSize': 75,
            #'StartingToken': ''
        }
    )
    all_results = []
    for r in list(response_iterator):
        all_results += r["Assignments"]
    all_answers = []
    for assignment in all_results:
        xml_doc = xmltodict.parse(assignment['Answer'])

        # Multiple fields in HIT layout
        assert type(xml_doc['QuestionFormAnswers']['Answer']) is list
        answers = {}
        for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
            question = answer_field['QuestionIdentifier']
            answers[question] = answer_field['FreeText']
        assert(experiment in [k[:len(experiment)] for k in answers.keys()])
        all_answers.append(answers)

    return all_answers


def is_valid_answer(answer):
    col_names = list(answer.keys())
    gt_diff_cols = [c for c in col_names if c[:2] == "GT" and "different" in c]
    bad_same_cols = [c for c in col_names if c[:3] == "bad" and "same" in c]

    is_valid = True
    for c in gt_diff_cols + bad_same_cols:
        if answer[c] == 'true':
            is_valid = False
            break

    return is_valid


def filter_valid_answers(all_answers):
    all_answers = np.array(all_answers)
    is_valid = list(map(is_valid_answer, all_answers))
    valid = all_answers[is_valid]
    return valid


def process_valid_answers(experiment, answers):
    audios = {}
    for answer in answers:
        for k in answer.keys():
            if k[:2] == "GT" or k[:3] == "bad":
                continue
            if answer[k] == 'false':
                continue
            exp_fname, rating = k.split('.')[:-1]
            if exp_fname not in audios:
                audios[exp_fname] = {"same_sure": 0,
                                     "same_maybe": 0,
                                     "different_maybe": 0,
                                     "different_sure": 0}
            audios[exp_fname][rating] += 1

    total = 0
    same_sure = 0
    same_maybe = 0
    for exp_fname, ratings in audios.items():
        total += sum(ratings.values())
        same_sure += ratings["same_sure"]
        same_maybe += ratings["same_maybe"]
    audios["overall"] = {"total": total,
                         "same_sure": same_sure,
                         "same_maybe": same_maybe,
                         "same": same_sure + same_maybe,
                         "same_sure_p": same_sure / total,
                         "same_maybe_p": same_maybe / total,
                         "same_p": (same_sure + same_maybe) / total}
    json.dump(audios, open(experiment + "_sim_res.json", "w"))
    pprint(audios['overall'])


if __name__ == '__main__':
    # with open("../rootkey_flora.csv", "r") as fp:
    with open("aws.csv", "r") as fp:
        line = fp.readline()
        keyid = line.split("=")[1].strip()
        line = fp.readline()
        key = line.split("=")[1].strip()
    mturk = boto3.client('mturk',
                         aws_access_key_id = keyid,
                         aws_secret_access_key = key,
                         region_name='us-east-1',
                         # endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
                         )

    hit_ids = {}
    with open("similarity-flora.txt", "r") as hitFile:
        for line in hitFile:
            experiment, hit_id = [c.strip() for c in line.split(",")]
            hit_ids[experiment] = hit_id

    for experiment in hit_ids:
        print("----", experiment, "----")
        answers = get_answers(hit_ids[experiment])
        answers = filter_valid_answers(answers)
        process_valid_answers(experiment, answers)
