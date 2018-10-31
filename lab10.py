import boto3
import json

s3 = boto3.resource('s3')
bucket = s3.Bucket('bucketname')
try:
    response = bucket.create(
    ACL='private',
    CreateBucketConfiguration = {
        'LocationConstraint':'ap-southeast-2'
        }
    )
    print(response)
except Exception as error:
    pass


object = bucket.put_object(Bucket='bucketname', Key='folder1/1' )
object = bucket.put_object(Bucket='bucketname', Key='folder2/2' )
object = bucket.put_object(Bucket='bucketname', Key='folder3/3' )

bucket_policy = s3.BucketPolicy('bucketname')
policy = 'policy.json'
with open(policy) as f:
    contents = f.read()
response = bucket_policy.put(
    ConfirmRemoveSelfBucketAccess = True,
    Policy = contents)
print(response)
