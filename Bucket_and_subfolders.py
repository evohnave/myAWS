# -*- coding: utf-8 -*-
"""
@author: Eric Vanhove

"""

# Imports
import boto3

# Constants
#Make sure you provide / in the end unless no prefix
prefix = '' 
bucket_name = 'aws-logs-079119988851-us-west-2'
path = '231856634451o.jpg'
fileName = '231856634451o.jpg'

# Ensure that your credentials are in place

s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

# Get list of buckets on S3
listOfBuckets = s3client.list_buckets()
for bucket in listOfBuckets['Buckets']:
    print('Bucket: {},\n\tCreated {}'.format(bucket['Name'], bucket['CreationDate']))

    results = s3client.list_objects(Bucket=bucket['Name'],
                                    Prefix=prefix,
                                    Delimiter='/')
    # CommonPrefixes are the "subfolders"
    #   Yes, I know, S3 has o subfolders...
    for o in results.get('CommonPrefixes'):
        print 'sub folder : ', o.get('Prefix')
    print('Files:')
    for o in results.get('Contents'):
        print('\t{}'.format(o.get('Key')))

#### don't run the below code!

# To create a bucket
s3client.create_bucket(Bucket=bucket_name)

# To upload a file
s3resource.Bucket(name = bucket_name).upload_file(Filename = path,
                                                  Key = fileName,
                                                  ExtraArgs = None,
                                                  Callback = None,
                                                  Config = None)

def renameObject(bucketName, oldObjectName, newObjectName, s3client):
    """ 
         This will rename an object in a bucket to the new name.  
         The old key will be deleted.
         
         bucketName = string
         oldObjectName = string
         newObjectName = string
         s3client = boto3.client('s3')
         
         Returns True on success, False on failure
         
         No error checking for now, no try/catch
    """
    successes = [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
    copySource = {
                 'Bucket' : bucketName,
                 'Key' : oldObjectName
                  }
    copyResponse = s3client.copy_object(
       Bucket = bucketName,
       CopySource = copySource,
       Key = newObjectName)
    if(copyResponse['ResponseMetadata']['HTTPStatusCode'] not in successes):
        return(False)
        # Need to come up with a way to pass back errors
            
    deleteResponse = s3client.delete_object(
       Bucket = bucketName,
       Key = oldObjectName)
    
    return(deleteResponse['ResponseMetadata']['HTTPStatusCode'] in successes)

