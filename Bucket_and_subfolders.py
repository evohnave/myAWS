# -*- coding: utf-8 -*-
"""
@author: Eric Vanhove

"""

# Imports
import boto3

# Ensure that your credentials are in place

s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

# Get list of buckets on S3
list_buckets_resp = s3client.list_buckets()
for bucket in list_buckets_resp['Buckets']:
    print('Bucket: {}, created {}'.format(bucket['Name'], bucket['CreationDate']))
    myBucket = s3resource.Bucket(bucket['Name'])
    result = myBucket.meta.client.list_objects(Bucket=myBucket.name,
                                         Delimiter='/')
    print('\tSubfolders:')
    for o in result.get('CommonPrefixes'):
        print('\t{}'.format(o.get('Prefix')))
