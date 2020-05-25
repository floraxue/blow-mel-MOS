import argparse
import boto3
from create_similarity_hit import create_sim_question


sandbox_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'


def post_question(question_html_value):

    mtc = boto3.client('mturk',
                       aws_access_key_id=keyid,
                       aws_secret_access_key=key,
                       region_name='us-east-1',
                       # endpoint_url = sandbox_url
                       )

    response = mtc.create_hit(
        MaxAssignments=500,
        AutoApprovalDelayInSeconds=604800,
        LifetimeInSeconds=604800,
        AssignmentDurationInSeconds=3000,
        Reward='0.10',
        Title='Are these two audios from the same speaker?',
        Keywords='audio, similarity, rating',
        Description='Please listen carefully to each pair of audio samples, and answer whether you think the two samples could have been produced by the same speaker. There are 14 pairs of short audios to rate (no longer than 10 seconds each). Please read the instructions carefully! There will be hidden tests for your work.',
        Question=question_html_value)

    # The response included several fields that will be helpful later
    hit_type_id = response['HIT']['HITGroupId']
    hit_id = response['HIT']['HITId']
    print("Your HIT has been created. You can see it at this link:")
    print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
    print("Your HIT ID is: {}".format(hit_id))
    return hit_id


parser = argparse.ArgumentParser(description='')
parser.add_argument("--expname", type=str, required=True)
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

q = create_sim_question(args.expname)
hit_id = post_question(q)
with open("similarity-flora.txt", "a") as fp:
    fp.write(args.expname + "," + hit_id + "\n")
