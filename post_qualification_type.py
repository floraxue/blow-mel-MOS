import boto3
import argparse

sandbox_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

qual_names = {'source_gt_target_gt': 'Participants of Source vs Target Audio Similarity Test',
              'target_gt_target_gt': 'Participants of Target vs Target Audio Similarity Test'}
qual_descps = {'source_gt_target_gt': 'DO NOT REQUEST. This is a qualification automatically granted to workers who took part in the Source vs Target Audio Similarity Test',
               'target_gt_target_gt': 'DO NOT REQUEST. This is a qualification automatically granted to workers who took part in the Target vs Target Audio Similarity Test'}


def create_qual_type(expname):
    mtc = boto3.client('mturk',
                       aws_access_key_id=keyid,
                       aws_secret_access_key=key,
                       region_name='us-east-1',
                       endpoint_url = sandbox_url
                       )

    qual_response = mtc.create_qualification_type(
        Name=qual_names[expname],
        Description=qual_descps[expname],
        QualificationTypeStatus='Active')
    qual_id = qual_response['QualificationType']['QualificationTypeId']
    print('Your Qualification is created. Your Qualification Type ID is:')
    print(qual_id)
    return qual_id


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

qual_id = create_qual_type(args.expname)

with open('qual-flora.txt', 'a') as fp:
    fp.write(args.expname + ',' + qual_id + '\n')
