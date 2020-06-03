import argparse
import boto3
import base64
from create_similarity_hit import create_sim_question, create_sim_source_gt_to_target_gt


sandbox_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
max_ass_per_hit = 9


def obfus_keys(key_id, key):
    obfus_key_id = base64.b64encode(key_id.encode('utf-8')).decode('utf-8')
    obfus_key = base64.b64encode(key.encode('utf-8')).decode('utf-8')
    return obfus_key_id, obfus_key


def post_question(question_html_value, qual_id):
    qr = [{'QualificationTypeId': qual_id,
           'Comparator': 'DoesNotExist'}]

    response = mtc.create_hit(
        MaxAssignments=max_ass_per_hit,
        AutoApprovalDelayInSeconds=604800,
        LifetimeInSeconds=604800,
        AssignmentDurationInSeconds=3000,
        Reward='0.10',
        Title='Are these two audios from the same speaker?',
        Keywords='audio, similarity, rating',
        Description='Please listen carefully to each pair of audio samples, and answer whether you think the two samples could have been produced by the same speaker. There are 14 pairs of short audios to rate (no longer than 10 seconds each). Please read the instructions carefully! There will be hidden tests for your work.',
        Question=question_html_value,
        QualificationRequirements=qr
    )

    # The response included several fields that will be helpful later
    hit_type_id = response['HIT']['HITGroupId']
    hit_id = response['HIT']['HITId']
    print("Your HIT has been created. You can see it at this link:")
    print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
    print("Your HIT ID is: {}".format(hit_id))
    return hit_id


parser = argparse.ArgumentParser(description='')
parser.add_argument("--expname", type=str, required=True)
parser.add_argument("--num_assignments", '-n', type=int, required=True)

args = parser.parse_args()

keyid = None
key = None
# with open("../rootkey_flora.csv", "r") as fp:
with open("aws.csv", "r") as fp:
    for i, line in enumerate(fp):
        if i == 0:
            keyid = str(line).split("=")[1].strip()
        else:
            key = str(line).split("=")[1].strip()
print(keyid, key)
obfus_key_id, obfus_key = obfus_keys(keyid, key)


mtc = boto3.client('mturk',
                   aws_access_key_id=keyid,
                   aws_secret_access_key=key,
                   region_name='us-east-1',
                   endpoint_url = sandbox_url
                   )

qual_id = ''
with open('qual-flora.txt', 'r') as fp:
    for line in fp:
        tokens = line.split(',')
        if tokens[0] == args.expname:
            qual_id = tokens[1].strip()

if qual_id == '':
    print('Qualification ID not found')
    exit(1)

question_html = create_sim_source_gt_to_target_gt(args.expname, obfus_key_id, obfus_key, qual_id)

num_loops = args.num_assignments // max_ass_per_hit + 1
for i in range(num_loops):
    hit_id = post_question(question_html, qual_id)
    with open("test-similarity-flora.txt", "a") as fp:
        fp.write(args.expname + "," + hit_id + "\n")
