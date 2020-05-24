import boto3


keyid = None
key = None
with open("aws.csv", "r") as fp:
    for i, line in enumerate(fp):
        if i == 0:
            keyid = str(line).split("=")[1].strip()
        else:
            key = str(line).split("=")[1].strip()
print(keyid, key)


mtc = boto3.client('mturk',
	                aws_access_key_id=keyid,
	                aws_secret_access_key=key,
	                region_name='us-east-1',
	                # endpoint_url = sandbox_url
	                )

hid_id = '3EGKVCRQFWLJ40YX03928FF80Q6YB1'
unique_request_token = '3EGKVCRQFWLJ40YX03928FF80Q6YB1_addtional_1'
response = mtc.create_additional_assignments_for_hit(
    HITId=hid_id,
    NumberOfAdditionalAssignments=100,
    UniqueRequestToken=unique_request_token
)



