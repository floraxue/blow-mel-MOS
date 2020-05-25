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

hid_id = '33Q5P9PUSPF2JV08AP7GX6USO5DZC3'
unique_request_token = '33Q5P9PUSPF2JV08AP7GX6USO5DZC3_addtional_1'
response = mtc.create_additional_assignments_for_hit(
    HITId=hid_id,
    NumberOfAdditionalAssignments=200,
    UniqueRequestToken=unique_request_token
)



