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
        AssignmentStatuses=['Submitted'],
        PaginationConfig={
            'MaxItems': 400,
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
    gt_cols = [c for c in col_names if c[:2] == "GT"]
    bad_cols = [c for c in col_names if c[:3] == "bad"]

    gt_scores = [int(answer[c]) for c in gt_cols]
    bad_scores = [int(answer[c]) for c in bad_cols]

    return ((gt_scores[0] > bad_scores[0]) & 
            (gt_scores[1] > bad_scores[0]) &
            (gt_scores[0] > bad_scores[1]) &
            (gt_scores[1] > bad_scores[1]))


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
            if k not in audios:
                audios[k] = []
            audios[k].append(int(answer[k]))

    scores = {key: get_mos(np.array(values)) for key, values in audios.items()}
    overall = [v for sublist in audios.values() for v in sublist]
    scores['overall'] = get_mos(np.array(overall))
    json.dump(scores, open(experiment + "_res.json", "w"))
    print(experiment, 'mu', scores['overall'][0], 'ci', scores['overall'][1], 'N', scores['overall'][2])


if __name__ == '__main__':
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
    with open("posted.txt", "r") as hitFile:
        for line in hitFile:
            experiment, hit_id = [c.strip() for c in line.split(",")]
            hit_ids[experiment] = hit_id

    for experiment in hit_ids:
        print("----", experiment, "----")
        answers = get_answers(hit_ids[experiment])
        answers = filter_valid_answers(answers)
        process_valid_answers(experiment, answers)

        # for audio in sorted(list(answers.keys())):
        #     print(audio, " ".join(list(map(str, get_ci(answers[audio])))))
        # print("overall", " ".join(list(map(str, get_ci([a for a in answers[audio] for audio in answers])))))
    """
            else:
                print("OPTION 2")
                # One field found in HIT layout
                print("For input field: " + xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier'])
                print("Submitted answer: " + xml_doc['QuestionFormAnswers']['Answer']['FreeText'])
    """

