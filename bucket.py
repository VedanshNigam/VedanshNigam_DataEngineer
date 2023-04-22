import boto3
s3 = boto3.client('s3')
response = s3.create_bucket(
    ACL='private',
    Bucket='steeleye-bucket-1',
    CreateBucketConfiguration={
        'LocationConstraint': 'ap-south-1'
    },
   ObjectOwnership='BucketOwnerPreferred'

)

print(response)