import boto3
import xmltodict
from get_results import is_valid_answer


def get_assignments(hit_id):
    paginator = mturk.get_paginator('list_assignments_for_hit')
    response_iterator = paginator.paginate(
        HITId=hit_id,
        AssignmentStatuses=['Submitted'],
        PaginationConfig={
            'MaxItems': 500,
            'PageSize': 75,
            #'StartingToken': ''
        }
    )
    all_results = []
    for r in list(response_iterator):
        all_results += r["Assignments"]

    all_answers = {}
    for assignment in all_results:
        assign_id = assignment['AssignmentId']

        xml_doc = xmltodict.parse(assignment['Answer'])
        # Multiple fields in HIT layout
        assert type(xml_doc['QuestionFormAnswers']['Answer']) is list
        answers = {}
        for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
            question = answer_field['QuestionIdentifier']
            answers[question] = answer_field['FreeText']
        assert(experiment in [k[:len(experiment)] for k in answers.keys()])
        all_answers[assign_id] = answers

    return all_answers


def split_assign_ids(all_answers):
    invalid_assign_ids = []
    valid_assign_ids = []
    for assign_id, answer in all_answers.items():
        if is_valid_answer(answer):
            valid_assign_ids.append(assign_id)
        else:
            invalid_assign_ids.append(assign_id)

    return valid_assign_ids, invalid_assign_ids


def reject_invalid_ids(invalid_ids):
    feedback = """
You did not pass the quality assurance test because 
you gave a white noise audio a higher naturalness rating than a real human speech recording.
Next time please pay attention to the instructions and listen to example audios if you are not sure.
    """
    for a_id in invalid_ids:
        response = mturk.reject_assignment(
            AssignmentId=a_id,
            RequesterFeedback=feedback
        )


def approve_valid_ids(valid_ids):
    feedback = """Thank you for your ratings!"""
    for a_id in valid_ids:
        response = mturk.approve_assignment(
            AssignmentId=a_id,
            RequesterFeedback=feedback,
            OverrideRejection=False
        )


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

    hit_ids.pop('blow_mel')

    for experiment in hit_ids:
        print("----", experiment, "----")
        answers = get_assignments(hit_ids[experiment])
        valid_ids, invalid_ids = split_assign_ids(answers)
        print("num valid", len(valid_ids), "invalid", len(invalid_ids))
        reject_invalid_ids(invalid_ids)
        approve_valid_ids(valid_ids)

