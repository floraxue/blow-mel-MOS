import boto3
import numpy as np
import argparse

from create_hit_v2 import creat_quesiton

bad_names = ["bad-LJ001-0015", "bad-LJ001-0051", "bad-LJ001-0063", "bad-LJ001-0072", "bad-LJ001-0079", "bad-LJ001-0094"]
good_names = ["GT-LJ001-0063", "GT-LJ001-0072", "GT-LJ001-0096", "GT-LJ001-0102", "GT-LJ001-0173"]
sandbox_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'


def post_question(question_html_value):

    # Create your connection to MTurk
    mtc = boto3.client('mturk',
                        aws_access_key_id=keyid,
                        aws_secret_access_key=key,
                        region_name='us-east-1',
                        # endpoint_url = sandbox_url
                        )

    # The first parameter is the HTML content
    # The second is the height of the frame it will be shown in
    # Check out the documentation on HTMLQuestion for more details
    # html_question = HTMLQuestion(question_html_value, 0)
    # These parameters define the HIT that will be created
    # question is what we defined above
    # max_assignments is the # of unique Workers you're requesting
    # title, description, and keywords help Workers find your HIT
    # duration is the # of seconds Workers have to complete your HIT
    # reward is what Workers will be paid when you approve their work
    # Check out the documentation on CreateHIT for more details
    response = mtc.create_hit(
                              MaxAssignments=150,
                              AutoApprovalDelayInSeconds=604800,
                            LifetimeInSeconds=604800,
                            AssignmentDurationInSeconds=3000,
                            Reward='0.10',
                            Title='How natural (i.e. human-sounding) is this recording?',
                            Keywords='audio, naturalness, rating',
                            Description='How natural is this recording? A recording is natural if it has minimal artifacts or distortions. Please read the instructions carefully! There will be hidden tests for your work.',
                            Question=question_html_value)

    # The response included several fields that will be helpful later
    hit_type_id = response['HIT']['HITGroupId']
    hit_id = response['HIT']['HITId']
    print("Your HIT has been created. You can see it at this link:")
    print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
    print("Your HIT ID is: {}".format(hit_id))
    return hit_id


if __name__ == '__main__':
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

    q = creat_quesiton(args.expname)
    hit_id = post_question(q)
    # with open("posted-daniel.txt", "a") as fp:
    with open("posted-flora.txt", "a") as fp:
        fp.write(args.expname + "," + hit_id + "\n")
